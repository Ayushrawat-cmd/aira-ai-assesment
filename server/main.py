# just load all the controllers
import controller
import uvicorn
from utils.config import Config
from utils.middleware import LogIncomingRequest, exception_handler, validation_exception_handler
from utils.middleware.exception_handlers import http_exception_handler
from utils.db_connection import init_celery_connection, init_vector_db
from utils.embedding_model import init_embedding_model
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
from fastapi_router_controller import Controller, ControllersTags


#########################################
#### Configure the main application #####
#########################################
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_celery_connection()
    await init_vector_db()
    await init_embedding_model()
    yield
    # await close_mongo_connection()

app = FastAPI(
    title='{}'.format(Config.read('app', 'name')),
    version='0.0.1',
    docs_url=Config.read('app', 'api-docs.path'),
    openapi_tags=ControllersTags,lifespan=lifespan)


# configuring handler for validation error in order to format the response
app.exception_handler(RequestValidationError)(validation_exception_handler)

# configuring handler for generic error in order to format the response
app.exception_handler(Exception)(exception_handler)

# configuring handler for generic error in order to format the response
app.exception_handler(HTTPException)(http_exception_handler)

# add middleware to process the request before it is taken by the router func
app.add_middleware(LogIncomingRequest)
#########################################
#### Configure all the implemented  #####
####  controllers in the main app   #####
#########################################
for router in Controller.routers():
    app.include_router(router)

# Server configuration
if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=5001, reload= True, workers= 2)