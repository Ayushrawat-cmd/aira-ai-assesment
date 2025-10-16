from datetime import datetime
import base64
import ast
from utils.logger import Logger


logger = Logger.get_logger(__name__)

def get_current_time_date_day():
    return {
        "date": datetime.now().strftime("%d-%m-%Y"),
        "day": datetime.now().strftime("%A"),
        "time": datetime.now().strftime("%H:%M")
    }

def buffer_to_base64(buffer):
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

def get_json( content:str):
    result = {"prompts": []}
    try:
        result = ast.literal_eval(content)
    except Exception as error:
        logger.error(f"extract json content :: {str(error)}")
    finally:
        return result