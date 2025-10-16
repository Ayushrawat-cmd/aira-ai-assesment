from langchain_openai import ChatOpenAI
import os
from utils.constant import GPT_API_KEY, GPT_ORG_ID

class ModelHandler:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls.instance = super(ModelHandler, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True

    def get_gpt_4o_mini(self):
        return ChatOpenAI(model="gpt-4o-mini", openai_api_key=os.environ.get(GPT_API_KEY),  temperature=0.7,seed=42)

    def get_gpt_4o(self, temperature=0.7):
        return ChatOpenAI(model="gpt-4o", openai_api_key=os.environ.get(GPT_API_KEY),  temperature=temperature,seed=42)
    
    def get_gpt_4_1(self, temperature=0.7):
        return ChatOpenAI(model="gpt-4.1", openai_api_key=os.environ.get(GPT_API_KEY),  temperature=temperature,seed=42)