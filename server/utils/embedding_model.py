import requests
from langchain_community.embeddings import HuggingFaceEmbeddings

# embeddings = None
async def init_embedding_model(model = "mixedbread-ai/mxbai-embed-large-v1"):
    # # Define the path to the pre-trained model you want to use
    global embeddings
    modelPath = model

    # Create a dictionary with model configuration options, specifying to use the CPU for computations
    model_kwargs = {'device':'cpu'}

    # Create a dictionary with encoding options, specifically setting 'normalize_embeddings' to False
    encode_kwargs = {'normalize_embeddings': False}

    # Initialize an instance of HuggingFaceEmbeddings with the specified parameters
    embeddings = HuggingFaceEmbeddings(
        model_name=modelPath,     # Provide the pre-trained model's path
        model_kwargs=model_kwargs, # Pass the model configuration options
        encode_kwargs=encode_kwargs # Pass the encoding options
    )
    print("initialising embeddings")
    return embeddings


def get_embedding_model():
    # global embeddings
    return embeddings



