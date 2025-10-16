from fastapi import Request
from schema.errors import Errors, throw_error
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import status
from fastapi import HTTPException

from utils.logger import Logger
logger = Logger.get_logger(__name__)

def validation_exception_handler(_: Request, exc: RequestValidationError):
    try:
        err = exc.errors()[0]
        # message = 'An error occured during {} handling. Error:{}'.format('.'.join(error['loc']), error['msg'])
        return throw_error(status= status.HTTP_400_BAD_REQUEST, message="Validation Error", error= err['msg'])
    except:
        return throw_error(status= status.HTTP_400_BAD_REQUEST, message="Validation Error", error= exc.args[0])

async def exception_handler(req: Request, exc: Exception):
    func_handler = req.state.func_name
    
    logger.error('An error occured during {} handling. Error: {}'.format(func_handler, exc))
    return throw_error(status= status.HTTP_500_INTERNAL_SERVER_ERROR, message= "An error occured", error_code= 5000, error= str(exc) )

async def http_exception_handler(req: Request, exc: HTTPException):
    if exc.status_code == 401:
        return throw_error(status= exc.status_code, message= exc.detail, error= "Please provide valid API KEY for API Access.")
    else: return throw_error(status= exc.status_code, message= exc.detail, error= "")