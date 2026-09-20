import { apiClient, setAccessToken } from './client'

export interface User {
  id: string
  email: string
  role: string
  is_active: boolean
}

interface TokenResponse {
  access_token: string
  token_type: string
}

export async function login(email: string, password: string): Promise<User> {
  const response = await apiClient.post<TokenResponse>('/api/v1/auth/login', {
    email,
    password,
  })
  setAccessToken(response.data.access_token)
  return me()
}

export async function logout(): Promise<void> {
  await apiClient.post('/api/v1/auth/logout')
  setAccessToken(null)
}

export async function me(): Promise<User> {
  const response = await apiClient.get<User>('/api/v1/auth/me')
  return response.data
}
