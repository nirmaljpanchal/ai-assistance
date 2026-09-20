import type { ReactNode } from 'react'
import { Navigate } from 'react-router-dom'

import { useAuth } from './AuthContext'

export function ProtectedRoute({
  children,
  requireRole,
}: {
  children: ReactNode
  requireRole?: string
}): JSX.Element {
  const { user, isLoading } = useAuth()

  if (isLoading) {
    return <p>Loading...</p>
  }

  if (!user) {
    return <Navigate to="/login" replace />
  }

  if (requireRole && user.role !== requireRole) {
    return <p>You do not have access to this page.</p>
  }

  return <>{children}</>
}
