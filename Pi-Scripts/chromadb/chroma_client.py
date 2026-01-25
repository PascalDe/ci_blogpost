import chromadb
from chromadb.config import Settings
from config import CHROMA_PATH

def get_chroma_client():
    return chromadb.Client(
        Settings(
            persist_directory=str(CHROMA_PATH),
            is_persistent=True,
            anonymized_telemetry=False
        )
    )
