import { apiClient } from './client'

export interface DocumentItem {
  id: string
  title: string
  filename: string
  mime_type: string
  tags: string[]
  status: 'pending' | 'processing' | 'ready' | 'failed'
  error_message: string | null
  created_at: string
  updated_at: string
}

export async function uploadDocument(
  file: File,
  title: string,
  tags: string[],
): Promise<{ id: string; status: string }> {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('title', title)
  formData.append('tags', tags.join(','))

  const response = await apiClient.post<{ id: string; status: string }>(
    '/api/v1/admin/documents',
    formData,
  )
  return response.data
}

export async function listDocuments(): Promise<DocumentItem[]> {
  const response = await apiClient.get<DocumentItem[]>('/api/v1/admin/documents')
  return response.data
}
