from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings

def EmbeddingWrapper(model_name="openai"):
    """
    EmbeddingWrapper: Automatically selects embedding backend based on model_name.
    
    Args:
        model_name (str): Model name to determine backend (e.g., "openai", "gemini").
    """
    model_name = model_name.lower()
    if "openai" in model_name:
        embedding = OpenAIEmbeddings()
    elif "gemini" in model_name:
        embedding = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    else:
        raise ValueError(f"Unsupported model_name for embeddings: {model_name}")
    return embedding