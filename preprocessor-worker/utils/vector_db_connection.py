from qdrant_client import QdrantClient
from qdrant_client.http import models
from langchain.vectorstores import Qdrant
from utils.constants import VECTOR_DB_COLLECTION_NAME


def init_vector_db(embeddings):
    global vectorstore
    qdrant_client = QdrantClient(url="http://localhost:6333")
    vectorstore = Qdrant(
        client=qdrant_client,
        collection_name=VECTOR_DB_COLLECTION_NAME,
        embeddings=embeddings,
    )

def get_vector_db():
    return vectorstore
