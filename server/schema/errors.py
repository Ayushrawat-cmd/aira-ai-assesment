from fastapi import status
from dataclasses import dataclass
from pydantic import BaseModel, Field
from fastapi.responses import ORJSONResponse

class ErrorModel(BaseModel):
    error: str = Field(..., description='The error message description')

@dataclass
class ErrorResponse():
    def __init__(self, message):
        self.error = message

@dataclass
class GenericError:
    status: int
    message: str
    error_code: str
    error: str

@dataclass
class GenericValidationError:
    status: int
    message: str
    error: str

class Errors():
    HTTP_500_INTERNAL_SERVER_ERROR = ORJSONResponse(ErrorResponse('Internal Server Error'), status.HTTP_500_INTERNAL_SERVER_ERROR)
    HTTP_400_BAD_REQUEST = lambda message   : ORJSONResponse(ErrorResponse(message), status.HTTP_400_BAD_REQUEST)

def throw_error(status, message: str, error_code: int = None, error: any = None):
    if error_code != None:
        error_res = GenericError(status = int(status), message = message, error_code = error_code, error = str(error))
        return ORJSONResponse(error_res, status)
    else:
        validation_error_res = GenericValidationError(status = int(status), message = message, error = str(error))
        return ORJSONResponse(validation_error_res, status)