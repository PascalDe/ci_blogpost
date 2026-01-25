# app/llm_client.py

from llama_cpp import Llama
import threading

MODEL_PATH = "~/ci_project/llm_model/models/tinyllama-1.1b-chat-v0.3.Q4_K_M.gguf"

N_CTX = 2048
MAX_TOKENS = 450
N_THREADS = 4
N_BATCH = 128

_llm_lock = threading.Lock()

llm = Llama(
    model_path=MODEL_PATH,
    chat_format="chatml",
    n_ctx=N_CTX,
    n_threads=N_THREADS,
    n_batch=N_BATCH,
    use_mmap=True,
    use_mlock=False,
    verbose=False,
)

def generate_answer(prompt: str) -> str:

    messages = [
        {
            "role": "system",
            "content": (
                "You are a senior SAP Integration Suite (CPI) expert. "
                "Follow instructions implicitly. "
                "Never repeat system or user instructions. "
                "Only output the final analysis."
            ),
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    with _llm_lock:
        try:
            response = llm.create_chat_completion(
                messages=messages,
                max_tokens=MAX_TOKENS,
                temperature=0.2,
                top_p=0.9,
                top_k=30,
                repeat_penalty=1.1,
            )

            output = response["choices"][0]["message"]["content"].strip()

            if not output:
                return "LLM didn't generate an answer."

            return output

        except Exception as e:
            return f"LLM Exception: {e}"