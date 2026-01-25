import chromadb
from chromadb.config import Settings
from config import CHROMA_PATH, COLLECTION_NAME
import os

client = chromadb.Client(
    Settings(
        persist_directory=str(CHROMA_PATH),
        is_persistent=True,
        anonymized_telemetry=False
    )
)

# Create Collection
collection = client.get_or_create_collection(COLLECTION_NAME)
print(f"Collection '{COLLECTION_NAME}' created")

#Add test collection
collection.add(
    documents=["Persistent test document for SAP_solutions."],
    metadatas=[{"source": "TEST"}],
    ids=["test_persist_001"]
)

print("Inserted test entry")

# Debug-Output
print("Collections:", [c.name for c in client.list_collections()])
print("Count:", collection.count())
print("Files:", os.listdir(CHROMA_PATH))