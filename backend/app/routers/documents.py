import re
import uuid
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends, Form, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.db import get_db
from app.deps import require_admin
from app.models.document import Document
from app.models.user import User
from app.schemas.document import DocumentOut, DocumentUploadResponse
from app.services.ingestion import ingest_document

router = APIRouter(prefix="/api/v1/admin/documents", tags=["documents"])
settings = get_settings()

_ALLOWED_TYPES: dict[str, bytes] = {
    "application/pdf": b"%PDF-",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": b"PK\x03\x04",
}
_EXTENSION_TO_MIME = {
    ".pdf": "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


def _sanitize_filename(filename: str) -> str:
    name = Path(filename).name
    return re.sub(r"[^A-Za-z0-9._-]", "_", name) or "document"


def _parse_tags(raw_tags: str) -> list[str]:
    return [tag.strip() for tag in raw_tags.split(",") if tag.strip()]


@router.post("", response_model=DocumentUploadResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile,
    title: str = Form(...),
    tags: str = Form(default=""),
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
) -> Document:
    extension = Path(file.filename or "").suffix.lower()
    mime_type = _EXTENSION_TO_MIME.get(extension)
    if mime_type is None:
        raise HTTPException(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            "Only .pdf and .docx files are supported",
        )

    max_bytes = settings.max_upload_mb * 1024 * 1024
    contents = await file.read(max_bytes + 1)
    if len(contents) > max_bytes:
        raise HTTPException(
            status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            f"File exceeds the {settings.max_upload_mb}MB limit",
        )

    magic = _ALLOWED_TYPES[mime_type]
    if not contents.startswith(magic):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "File content does not match its extension")

    document_id = uuid.uuid4()
    safe_filename = _sanitize_filename(file.filename or "document")
    document_dir = Path(settings.upload_dir) / str(document_id)
    document_dir.mkdir(parents=True, exist_ok=True)
    storage_path = document_dir / safe_filename
    storage_path.write_bytes(contents)

    document = Document(
        id=document_id,
        title=title,
        filename=safe_filename,
        storage_path=str(storage_path),
        mime_type=mime_type,
        tags=_parse_tags(tags),
        uploaded_by_id=admin.id,
    )
    db.add(document)
    await db.commit()
    await db.refresh(document)

    background_tasks.add_task(ingest_document, document.id)

    return document


@router.get("", response_model=list[DocumentOut])
async def list_documents(
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
) -> list[Document]:
    result = await db.execute(
        select(Document).order_by(Document.created_at.desc()).limit(limit).offset(offset)
    )
    return list(result.scalars().all())


@router.get("/{document_id}", response_model=DocumentOut)
async def get_document(
    document_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
) -> Document:
    document = await db.get(Document, document_id)
    if document is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Document not found")
    return document
