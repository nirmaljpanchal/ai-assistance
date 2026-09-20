import axios, { AxiosError, type InternalAxiosRequestConfig } from 'axios'

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export const apiClient = axios.create({
  baseURL: API_URL,
  withCredentials: true,
})

let accessToken: string | null = null

export function setAccessToken(token: string | null): void {
  accessToken = token
}

type RetryableConfig = InternalAxiosRequestConfig & { _retried?: boolean }

let refreshPromise: Promise<string> | null = null

async function refreshAccessToken(): Promise<string> {
  const response = await axios.post<{ access_token: string }>(
    `${API_URL}/api/v1/auth/refresh`,
    null,
    { withCredentials: true },
  )
  const token = response.data.access_token
  setAccessToken(token)
  return token
}

apiClient.interceptors.request.use((config) => {
  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`
  }
  return config
})

apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const config = error.config as RetryableConfig | undefined
    if (error.response?.status !== 401 || !config || config._retried) {
      throw error
    }

    config._retried = true
    try {
      refreshPromise ??= refreshAccessToken().finally(() => {
        refreshPromise = null
      })
      const token = await refreshPromise
      config.headers.Authorization = `Bearer ${token}`
      return apiClient.request(config)
    } catch (refreshError) {
      setAccessToken(null)
      throw refreshError
    }
  },
)
