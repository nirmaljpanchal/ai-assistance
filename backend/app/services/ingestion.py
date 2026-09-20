import logging
import uuid

from app.db import async_session_factory
from app.models.document import Document, DocumentStatus
from app.models.document_chunk import DocumentChunk
from app.services.chunking import semantic_chunk
from app.services.embeddings import embed_texts
from app.services.extraction import extract_text

logger = logging.getLogger(__name__)


async def ingest_document(document_id: uuid.UUID) -> None:
    async with async_session_factory() as db:
        document = await db.get(Document, document_id)
        if document is None:
            logger.error("Document %s not found for ingestion", document_id)
            return

        document.status = DocumentStatus.PROCESSING.value
        await db.commit()

        try:
            text = extract_text(document.storage_path, document.mime_type)
            chunks = semantic_chunk(text)
            if not chunks:
                raise ValueError("Semantic chunking produced no chunks")

            embeddings = embed_texts(chunks)

            for index, (content, embedding) in enumerate(zip(chunks, embeddings, strict=True)):
                db.add(
                    DocumentChunk(
                        document_id=document.id,
                        chunk_index=index,
                        content=content,
                        embedding=embedding,
                        chunk_metadata={"char_count": len(content)},
                    )
                )

            document.status = DocumentStatus.READY.value
            document.error_message = None
            await db.commit()
        except Exception as exc:
            logger.exception("Ingestion failed for document %s", document_id)
            await db.rollback()
            document = await db.get(Document, document_id)
            if document is not None:
                document.status = DocumentStatus.FAILED.value
                document.error_message = str(exc)[:2000]
                await db.commit()
