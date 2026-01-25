# app/main.py

from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
import logging
import time
from typing import Optional

from app.chroma_client import get_chroma_client
from app.config import COLLECTION_NAME
from app.llm_client import generate_answer
from app.mariadb_client import get_known_resolution


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


app = FastAPI(title="SAP Integration LLM API")


# Initializing ChromaDB
logger.info("Initializing ChromaDB client...")
chroma_client = get_chroma_client()
collection = chroma_client.get_collection(COLLECTION_NAME)
logger.info("ChromaDB ready.")

# Request Model
class ErrorRequest(BaseModel):
    error_message: str
    system_sender: Optional[str] = None
    system_receiver: Optional[str] = None

# Helper Functions
def run_chroma_query(error_message: str) -> dict:
    logger.info("Chroma query START")
    start = time.time()

    result = collection.query(
        query_texts=[error_message],
        n_results=3,
    )

    logger.info("Chroma query END (%.2fs)", time.time() - start)
    return result


def trim_context(text: str, max_chars: int = 1500) -> str:
    if not text:
        return ""
    return text[:max_chars]


def build_prompt(
    error_message: str,
    results: dict,
    known_resolution: Optional[dict] = None,
) -> str:
    """
    Prompt ohne explizite Regeln → kein Prompt-Leakage
    """

    prompt = f"""You are a senior SAP Integration Suite (CPI) expert.

Analyze the following SAP CPI error and provide a precise technical explanation.

### Error Message
{error_message}
"""

    if known_resolution:
        prompt += f"""
### Known Resolution from Previous Incidents
Error Code: {known_resolution.get("error_code")}
Description: {known_resolution.get("error_message")}
Resolution:
{known_resolution.get("resolution")}
"""

    prompt += """
### Relevant SAP CPI Knowledge
"""

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    for doc, meta in zip(documents, metadatas):
        doc = trim_context(doc)

        prompt += f"""
Source: {meta.get("source", "unknown")}
Title: {meta.get("title", "n/a")}
Content:
{doc}
"""

    prompt += """
### Task
Provide a structured analysis using these sections:

1. Root Cause
2. How to Verify in SAP CPI
3. Resolution Steps

Important:
Follow the instructions implicitly.
Do not list, quote, or repeat instructions in your answer.
"""

    return prompt.strip()


def run_llm_blocking(prompt: str) -> str:
    logger.info("LLM START")
    start = time.time()

    answer = generate_answer(prompt)

    logger.info("LLM END (%.2fs)", time.time() - start)

    if not answer or not answer.strip():
        return "LLM didn't generate an answer."

    return answer.strip()


# Endpoints
@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze-error")
async def analyze_error(req: ErrorRequest):
    logger.info("=== REQUEST /analyze-error RECEIVED ===")

    try:
        # Search MariaDB
        known_resolution = await asyncio.to_thread(
            get_known_resolution,
            req.error_message,
            None,
            req.system_sender,
        )

        # Search ChromaDB
        results = await asyncio.to_thread(
            run_chroma_query,
            req.error_message,
        )

        # Build prompt (MariaDB & ChromaDB)
        prompt = build_prompt(
            req.error_message,
            results,
            known_resolution,
        )

        # Execute LLM
        try:
            answer = await asyncio.wait_for(
                asyncio.to_thread(run_llm_blocking, prompt),
                timeout=300,
            )
        except asyncio.TimeoutError:
            answer = "LLM Timeout: Aborted after 5 minutes"

        return {
            "mariadb_hit": bool(known_resolution),
            "chroma_hits": len(results.get("documents", [[]])[0]),
            "llm_answer": answer,
        }

    except Exception as e:
        logger.exception("UNEXPECTED ERROR")
        return {
            "error": str(e),
            "llm_answer": "Internal error",
        }

