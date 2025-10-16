from qdrant_client import QdrantClient
from qdrant_client.http import models
from langchain.vectorstores import Qdrant
from utils.constants import VECTOR_DB_COLLECTION_NAME


def init_vector_db(embeddings):
    global vectorstore
    qdrant_client = QdrantClient(url="http://localhost:6333")
    existing_collections = [col.name for col in qdrant_client.get_collections().collections]
    
    if VECTOR_DB_COLLECTION_NAME not in existing_collections:
        print(f"🆕 Creating new Qdrant collection: {VECTOR_DB_COLLECTION_NAME}")
        qdrant_client.recreate_collection(
            collection_name=VECTOR_DB_COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=1024,  # auto from model
                distance=models.Distance.COSINE
            ),
        )
    else:
        print(f"✅ Using existing Qdrant collection: {VECTOR_DB_COLLECTION_NAME}")
    vectorstore = Qdrant(
        client=qdrant_client,
        collection_name=VECTOR_DB_COLLECTION_NAME,
        embeddings=embeddings,
    )

def get_vector_db():
    return vectorstore
