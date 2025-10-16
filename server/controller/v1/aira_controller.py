from fastapi_router_controller import Controller
from fastapi.responses import StreamingResponse, ORJSONResponse
from sse_starlette import EventSourceResponse
from fastapi import APIRouter, Body, Depends, status as _status, Request, Query
from utils.logger import Logger
from utils.constants import ResStatus
from schema.errors import throw_error
from environment.router.urls import URLs
from fastapi.responses import Response
from fastapi.exceptions import HTTPException, RequestValidationError
from services.chatbot_service import ChatbotService
from services.ingest_url_service import IngestUrlService
from schema.ingest_url_schema import IngestUrlReqSchema
from schema.chatbot_schema import ChatbotReqSchema, ChatbotResSchema

# Logger Instance
logger = Logger.get_logger(__name__)

# Initialize the router
chatbot_router = APIRouter(prefix= URLs.base_v1)

# Initialize the controller
controller = Controller(chatbot_router, openapi_tag={
    'name': 'chatbot_controller',
})


# MARK: - Virtual Consultation Controller Class to use it automatically
@controller.use()

# MARK: - Virtual Consultation Controller Class as a resource of the given Controller router
@controller.resource()
class ChatbotController():

    def __init__(self, ingest_url_service: IngestUrlService = Depends(),chatbot_service: ChatbotService = Depends() ) -> None:
        self.chatbot_service = chatbot_service
        self.ingest_url_service = ingest_url_service  


    # MARK:- Ingest URL in the RAG system
    @controller.route.post(
        '/ingest-url',
        tags=['chatbot_router'],
        summary= 'Ingest URL in the RAG system',
        status_code= 202,
    )
    async def ingest_url(self, request: Request, req: IngestUrlReqSchema = Body()):
        logger.debug(f"{self.__class__.__name__} : ingest_url")
        try:
            response = await self.ingest_url_service.ingest_url(req.url, req.email)
            return ORJSONResponse(content=response.model_dump(exclude_none=True), status_code=_status.HTTP_202_ACCEPTED)
        except Exception as e:
            logger.error(f"{self.__class__.__name__} : ingest_url : {str(e)}")
            return throw_error(status=500, message="Failed to ingest URL", error_code="INTERNAL_SERVER_ERROR", error=str(e))

    @controller.route.get(
        '/relevant-docs',
        tags=['chatbot_router'],
        summary= 'Get Relevant Docs from the RAG system',
        status_code= 200,
    )
    async def get_relevant_docs(self, request: Request, query:str= Query()):
        logger.debug(f"{self.__class__.__name__} : get_relevant_docs")
        try:
            # user_id = request.headers.get("x-user-id", "")
            response = await self.chatbot_service.get_relevant_docs( query)
            return ORJSONResponse(content=response.model_dump(exclude_none=True), status_code=_status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"{self.__class__.__name__} : get_relevant_docs : {str(e)}")
            return throw_error(status=500, message="Failed to get relevant docs", error_code="INTERNAL_SERVER_ERROR", error=str(e))

    # MARK: - Query Processing Request Handler
    @controller.route.get(
        '/chat',
        tags=['chatbot_router'],
        summary= 'Chatbot Streaming',
        status_code= 200,
        response_class=StreamingResponse
    )
    async def stream_query(self, request: Request, req: ChatbotReqSchema = Query()):
        logger.debug(f"{self.__class__.__name__} : stream_query")
        try:
            
            return EventSourceResponse(self.chatbot_service.get_response(   req.query),status_code=200)

        except Exception as e:
            logger.error(f"{self.__class__.__name__} : stream_query : {str(e)}")
            self.__exception_handler(e)

    @controller.route.get(
        '/health-check',
        tags=['chatbot_router'],
        summary= 'Health checker',
        status_code= 200,
    )
    def health_checker(self,):
        return "Chatbot service is working."