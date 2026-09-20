from functools import lru_cache

from langchain_openai import OpenAIEmbeddings

from app.config import get_settings

settings = get_settings()


@lru_cache
def get_embeddings_model() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(
        model=settings.openai_embedding_model,
        openai_api_key=settings.openai_api_key,
        dimensions=settings.embedding_dimensions,
    )


def embed_texts(texts: list[str]) -> list[list[float]]:
    return get_embeddings_model().embed_documents(texts)
