import React, { useState, useEffect } from 'react'
import { Toaster } from 'sonner'
import Login from './components/Login'
import ChatInterface from './components/ChatInterface'

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'))
  const [user, setUser] = useState(null)

  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token)
    } else {
      localStorage.removeItem('token')
    }
  }, [token])

  const handleLogout = () => {
    setToken(null)
    setUser(null)
    localStorage.removeItem('token')
  }

  return (
    <div className="w-full h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <Toaster position="top-right" richColors />
      {!token ? (
        <Login onLogin={setToken} />
      ) : (
        <ChatInterface token={token} onLogout={handleLogout} user={user} setUser={setUser} />
      )}
    </div>
  )
}

export default App
