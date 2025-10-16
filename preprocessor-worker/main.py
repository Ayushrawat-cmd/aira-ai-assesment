from celery_config import celery_app
from celery import signals
from utils.constants import IngestUrlStatus
from utils.embedding_model import get_embedding_model, init_embedding_model
from utils.vector_db_connection import get_vector_db_client, init_vector_db
from langchain_experimental.text_splitter import SemanticChunker


def semantic_preprocess_wikipedia_data(data: dict,embeddings):
    """
    Preprocess Wikipedia scraped data into semantically coherent chunks using LangChain SemanticChunker.
    
    Args:
        data (dict): Dictionary containing 'title', 'url', and 'content'.
    
    Returns:
        list[dict]: List of semantically grouped chunks with metadata.
    """
    text = data.get("content", "")
    title = data.get("title", "Untitled")
    url = data.get("url", "")
    
    # Initialize embedding model
    # embeddings = get_embedding_model()
    # Create semantic chunker (based on meaning change)
    semantic_splitter = SemanticChunker(embeddings, breakpoint_threshold_type="percentile",number_of_chunks=(len(text)/1000))
    # Perform semantic splitting
    chunks = semantic_splitter.split_text(text)
    
    processed_chunks = [
        {
            "title": title,
            "url": url,
            "chunk_id": i + 1,
            "content": chunk
        }
        for i, chunk in enumerate(chunks)
    ]
    
    return processed_chunks




@signals.worker_process_init.connect
def setup_embedding_model(sender, **kwargs):
    # global embeddings
    """Initialize embedding model once when Celery worker starts."""
    init_embedding_model()
    print("Embedding model initialized at worker startup")
    init_vector_db()
    print("Vector DB client initialized at worker startup")



@celery_app.task(name="tasks.preprocess_task")
def preprocess_task(task_id, url, email, data):
    try:
        print(f"Scraping URL: {url}, email: {email}, data: {data}")
        embeddings = get_embedding_model()
        processed_chunks = semantic_preprocess_wikipedia_data(data,embeddings)
        result = {"url": url, "status": IngestUrlStatus.INGESTED.value, "email": email, "data":data }
        print(preprocess_task.request.id)
        return {"url": url, "status": IngestUrlStatus.INGESTED.value, "email": email, "processed_chunks": processed_chunks} 

    except Exception as e:
        print(e)
        return {"url":url, "status": IngestUrlStatus.PREPROCESSING_FAILED.value, "email":email}
