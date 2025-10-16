from utils.model_handler import ModelHandler
from repository.vector_db_repo import VectorDBRepo  

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

    def __get_prompt(self, message, context, chat_history =[]):
        # interval = self.input_field_extractor.extract_input_fields(message, market_types)
        prompt = ChatPromptTemplate.from_messages([
            ("system", convo_system_prompt), 
            ("user",convo_user_prompt)
            ]).partial(today=today, context=context, chat_history=chat_history)
        return prompt
    