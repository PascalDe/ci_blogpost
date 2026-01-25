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

collection = client.get_or_create_collection(COLLECTION_NAME)

# Beispiel: SAP Note Insert
collection.add(
    documents=[
        "When using the HTTP adapter in SAP CPI, the error '403 Forbidden' "
        "occurs if the OAuth token is missing, expired, or the role assignment "
        "is incomplete. Verify OAuth2 credentials and token endpoint configuration."
    ],
    metadatas=[{
        "source": "SAP_NOTE",
        "note_id": "1234567",
        "title": "HTTP 403 Error in CPI Adapter",
        "component": "BC-CP-INT",
        "url": "https://launchpad.support.sap.com/#/notes/1234567",
        "language": "EN",
        "last_updated": "2024-02-01"
    }],
    ids=["note_1234567_chunk_01"]
)

print("SAP Note inserted successfully")