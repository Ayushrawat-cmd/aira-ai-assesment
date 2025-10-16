from utils.db_connection import get_vector_db
from utils.embedding_model import get_embedding_model


class VectorDBRepo:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VectorDBRepo, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.vector_db = get_vector_db(get_embedding_model()) 


    async def search_similar(self, query: str, top_k: int = 5):
        try:
            results = self.vector_db.similarity_search(
                query,
                k=top_k
            )
            return results
        except Exception as e:
            raise e