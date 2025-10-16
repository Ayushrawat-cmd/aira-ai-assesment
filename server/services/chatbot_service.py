from utils.model_handler import ModelHandler
from repository.vector_db_repo import VectorDBRepo  
from langchain_core.prompts import ChatPromptTemplate
from schema.chatbot_schema import ChatbotResSchema
from utils.logger import Logger

logger = Logger.get_logger(__name__)

system_prompt = """
You are an AI assistant that helps people find information.
You should answer the user's query as truthfully as possible.

Context: {context}

Provide a concise answer to the user's query using the context provided only.

Note: If the context provided does not contain the answer, say "I don't know".

"""

user_prompt = """
Query: {query}
"""
class ChatbotService:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChatbotService, cls).__new__(cls)
        return cls._instance
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.model_handler = ModelHandler()
            self.vector_db_repo = VectorDBRepo()

    def __get_prompt(self, ):
        # interval = self.input_field_extractor.extract_input_fields(message, market_types)
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt), 
            ("user",user_prompt)
            ])
        return prompt
    
    async def get_relevant_docs(self, query: str, top_k: int = 5):
        try:
            results = await self.vector_db_repo.search_similar(
                query,
                top_k
            )
            return results
        except Exception as e:
            logger.error(f"{self.__class__.__name__} : get_relevant_docs : {str(e)}")
            raise e
    
    async def get_response(self, query: str):
        logger.info(f"{self.__class__.__name__} : get_response")
        try:
            chain = self.__get_prompt() | self.model_handler.get_gpt_4_1()
            context = await self.get_relevant_docs(query)
            async for token in chain.astream({
                "query": query,
                "context": context,
            }):
                yield ChatbotResSchema(event="data", data=token.content).model_dump_json()

        except Exception as e:
            logger.error(f"{self.__class__.__name__} : get_response : {str(e)}")
            yield ChatbotResSchema(event="error", data="Please try again").model_dump_json()
    