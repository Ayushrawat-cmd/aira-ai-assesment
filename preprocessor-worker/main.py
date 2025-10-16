from celery_config import celery_app
from celery import signals
from utils.constants import IngestUrlStatus, VECTOR_DB_COLLECTION_NAME, Collections, DATABASE_NAME
from utils.embedding_model import get_embedding_model, init_embedding_model
from utils.vector_db_connection import get_vector_db, init_vector_db
from utils.mongodb_connection import get_mongo_client, init_mongo_connnection
from langchain.vectorstores import Qdrant
from langchain_experimental.text_splitter import SemanticChunker
from dotenv import load_dotenv
import os
from datetime import datetime, timezone

load_dotenv("./dev.env")  # Load environment variables from .env file

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
def setup_connections(sender, **kwargs):
    # global embeddings
    """Initialize embedding model once when Celery worker starts."""
    init_embedding_model()
    print("Embedding model initialized at worker startup")
    init_vector_db(get_embedding_model())
    print("Vector DB client initialized at worker startup")
    init_mongo_connnection()
    print("MongoDB client initialized at worker startup")


def save_to_vector_db(processed_chunks):
    vectorstore = get_vector_db()
    
    for chunk in processed_chunks:
        vectorstore.add_texts(
            texts=[chunk["content"]],
            metadatas=[{
                "title": chunk["title"],
                "url": chunk["url"],
            }]
        )
 


@celery_app.task(name="tasks.preprocess_task")
def preprocess_task(task_id, url, email, data):
    client = get_mongo_client()
    db = client[DATABASE_NAME]
    collection = db.get_collection(Collections.JOB_TRACKERS.value)
    try:
        print(f"Scraping URL: {url}, email: {email}, data: {data}")
        embeddings = get_embedding_model()
        processed_chunks = semantic_preprocess_wikipedia_data(data,embeddings)
        save_to_vector_db(processed_chunks)
        result = {"url": url, "status": IngestUrlStatus.INGESTED.value, "email": email, "data":data }
        
        print(preprocess_task.request.id)

        
        
        collection.update_one(
            {"_id": task_id},
            {"$set": {"status": IngestUrlStatus.INGESTED.value,"updated_at": datetime.now(timezone.utc), }})
        return {"url": url, "status": IngestUrlStatus.INGESTED.value, "email": email, "processed_chunks": processed_chunks} 

    except Exception as e:
        print(e)
        try:
            collection.update_one(
                {"_id": task_id},
                {"$set": {"status": IngestUrlStatus.PREPROCESSING_FAILED.value, "error": str(e), "updated_at": datetime.now(timezone.utc)}}
            )
        except Exception as me:
            print("Failed to update MongoDB with error:", me)

        return {"url":url, "status": IngestUrlStatus.PREPROCESSING_FAILED.value, "email":email}
