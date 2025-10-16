from utils.db_connection import get_vector_db
from utils.embedding_model import get_embedding_model
from utils.logger import Logger
from schema.chatbot_schema import RelevantDocsResSchema, Document

logger = Logger.get_logger(__name__)

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
        logger.debug(f"{self.__class__.__name__} : search_similar")
        try:
            results = self.vector_db.similarity_search(
                query,
                k=top_k
            )
            results = RelevantDocsResSchema(documents=[Document(page_content=result.page_content , metadata=result.metadata) for result in results])
            return results
        except Exception as e:
            raise e