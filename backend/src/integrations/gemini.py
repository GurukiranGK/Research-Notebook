from functools import lru_cache

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

from src.core.config import get_settings


settings = get_settings()

if not settings.gemini_api_key:
    raise RuntimeError("GEMINI_API_KEY is missing")


@lru_cache
def get_embeddings() -> GoogleGenerativeAIEmbeddings:
    return GoogleGenerativeAIEmbeddings(
        google_api_key=settings.gemini_api_key,
        model="models/gemini-embedding-001",
    )


@lru_cache
def get_llm() -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        google_api_key=settings.gemini_api_key,
        model="models/gemini-2.5-flash",
        temperature=0.2,
    )
