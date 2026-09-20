from langchain_experimental.text_splitter import SemanticChunker

from app.services.embeddings import get_embeddings_model


def semantic_chunk(text: str) -> list[str]:
    splitter = SemanticChunker(get_embeddings_model())
    chunks = [chunk.strip() for chunk in splitter.split_text(text)]
    return [chunk for chunk in chunks if chunk]
