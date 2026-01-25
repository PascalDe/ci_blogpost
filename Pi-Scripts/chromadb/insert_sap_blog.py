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

# Beispiel: Blog Insert
collection.add(
    documents=[
        "This blog explains common authentication issues in SAP Integration Suite. "
        "HTTP 403 errors are often caused by missing scopes in the OAuth client "
        "or expired client secrets. Always re-deploy the iFlow after credential changes."
    ],
    metadatas=[{
        "source": "SAP_BLOG",
        "title": "Troubleshooting Authentication Errors in SAP CPI",
        "component": "BC-CP-INT",
        "author": "SAP Community",
        "language": "EN",
        "last_updated": "2023-11-12"
    }],
    ids=["blog_auth_cpi_01"]
)

print("SAP Blog inserted successfully")