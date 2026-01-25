import chromadb
from chromadb.config import Settings
from config import CHROMA_PATH, COLLECTION_NAME

client = chromadb.Client(
    Settings(
        persist_directory=str(CHROMA_PATH),
        is_persistent=True,
        anonymized_telemetry=False
    )
)

print("Collections:", [c.name for c in client.list_collections()])

collection = client.get_collection(COLLECTION_NAME)
print("Collection found")
print("Count:", collection.count())