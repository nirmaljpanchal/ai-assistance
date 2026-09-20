import { Navigate, Route, BrowserRouter, Routes } from 'react-router-dom'

import './App.css'
import { AuthProvider } from './auth/AuthContext'
import { ProtectedRoute } from './auth/ProtectedRoute'
import { AdminDocumentsPage } from './pages/AdminDocumentsPage'
import { LoginPage } from './pages/LoginPage'

function App(): JSX.Element {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/admin/documents"
            element={
              <ProtectedRoute requireRole="admin">
                <AdminDocumentsPage />
              </ProtectedRoute>
            }
          />
          <Route path="/" element={<Navigate to="/admin/documents" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App
