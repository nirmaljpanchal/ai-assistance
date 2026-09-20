import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from './App'

vi.mock('./api/auth', () => ({
  me: vi.fn().mockRejectedValue(new Error('not authenticated')),
  login: vi.fn(),
  logout: vi.fn(),
}))

describe('App', () => {
  it('redirects unauthenticated users to the login page', async () => {
    render(<App />)
    expect(await screen.findByRole('heading', { name: /sign in/i })).toBeInTheDocument()
  })
})
