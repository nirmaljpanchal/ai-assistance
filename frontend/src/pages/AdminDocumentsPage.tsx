import { useCallback, useEffect, useRef, useState } from 'react'
import type { ChangeEvent, FormEvent } from 'react'

import { listDocuments, uploadDocument, type DocumentItem } from '../api/documents'
import { useAuth } from '../auth/AuthContext'

const ACTIVE_STATUSES = new Set(['pending', 'processing'])

export function AdminDocumentsPage(): JSX.Element {
  const { user, logout } = useAuth()
  const [documents, setDocuments] = useState<DocumentItem[]>([])
  const [file, setFile] = useState<File | null>(null)
  const [title, setTitle] = useState('')
  const [tagsInput, setTagsInput] = useState('')
  const [isUploading, setIsUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const refresh = useCallback(async () => {
    const docs = await listDocuments()
    setDocuments(docs)
  }, [])

  useEffect(() => {
    refresh().catch(() => setError('Failed to load documents'))
  }, [refresh])

  useEffect(() => {
    const hasActiveDocument = documents.some((doc) => ACTIVE_STATUSES.has(doc.status))
    if (!hasActiveDocument) {
      return
    }
    const interval = setInterval(() => {
      refresh().catch(() => undefined)
    }, 3000)
    return () => clearInterval(interval)
  }, [documents, refresh])

  function handleFileChange(event: ChangeEvent<HTMLInputElement>): void {
    setFile(event.target.files?.[0] ?? null)
  }

  async function handleSubmit(event: FormEvent): Promise<void> {
    event.preventDefault()
    if (!file) {
      setError('Please choose a PDF or DOCX file')
      return
    }

    setError(null)
    setIsUploading(true)
    try {
      const tags = tagsInput
        .split(',')
        .map((tag) => tag.trim())
        .filter(Boolean)
      await uploadDocument(file, title || file.name, tags)
      setTitle('')
      setTagsInput('')
      setFile(null)
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
      await refresh()
    } catch {
      setError('Upload failed. Only PDF and DOCX files up to the configured size limit are accepted.')
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className="admin-documents-page">
      <header>
        <h1>Documents</h1>
        <div>
          <span>{user?.email}</span>
          <button type="button" onClick={() => void logout()}>
            Log out
          </button>
        </div>
      </header>

      <form onSubmit={(e) => void handleSubmit(e)}>
        <label htmlFor="file">Document (PDF or DOCX)</label>
        <input
          id="file"
          ref={fileInputRef}
          type="file"
          accept=".pdf,.docx"
          onChange={handleFileChange}
        />

        <label htmlFor="title">Title</label>
        <input
          id="title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder={file?.name ?? 'Document title'}
        />

        <label htmlFor="tags">Tags (comma-separated)</label>
        <input
          id="tags"
          type="text"
          value={tagsInput}
          onChange={(e) => setTagsInput(e.target.value)}
          placeholder="policy, hr, 2026"
        />

        {error && <p role="alert">{error}</p>}

        <button type="submit" disabled={isUploading}>
          {isUploading ? 'Uploading...' : 'Upload'}
        </button>
      </form>

      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th>Tags</th>
            <th>Status</th>
            <th>Uploaded</th>
          </tr>
        </thead>
        <tbody>
          {documents.map((doc) => (
            <tr key={doc.id}>
              <td>{doc.title}</td>
              <td>{doc.tags.join(', ')}</td>
              <td title={doc.error_message ?? undefined}>{doc.status}</td>
              <td>{new Date(doc.created_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
