from qdrant_client import QdrantClient
from qdrant_client.http import models


def init_vector_db():
    global qdrant_client
    qdrant_client = QdrantClient(url="http://localhost:6333")

def get_vector_db_client():
    return qdrant_client
