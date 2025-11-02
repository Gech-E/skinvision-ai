import React from 'react'
import { Link, useNavigate } from 'react-router-dom'

export default function Navbar() {
  const navigate = useNavigate()
  const [authed, setAuthed] = React.useState(false)
  const [darkMode, setDarkMode] = React.useState(false)

  React.useEffect(() => {
    setAuthed(!!localStorage.getItem('token'))
    const isDark = localStorage.getItem('darkMode') === 'true'
    setDarkMode(isDark)
    if (isDark) {
      document.documentElement.classList.add('dark')
      document.body.classList.add('dark')
    }
  }, [])

  function toggleDarkMode() {
    const newDarkMode = !darkMode
    setDarkMode(newDarkMode)
    localStorage.setItem('darkMode', newDarkMode.toString())
    if (newDarkMode) {
      document.documentElement.classList.add('dark')
      document.body.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
      document.body.classList.remove('dark')
    }
  }

  function logout() {
    localStorage.removeItem('token')
    setAuthed(false)
    navigate('/')
  }
  
  return (
    <header className="sticky top-0 z-50 backdrop-blur-md bg-white/80 dark:bg-dark-bg/80 border-b border-accent dark:border-dark-border">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-3 text-text dark:text-dark-text text-xl font-bold hover:opacity-80 transition-opacity">
          <span className="text-2xl">🧬</span>
          <span className="text-heading-md">SkinVision AI</span>
        </Link>
        <nav className="flex items-center gap-6">
          <Link to="/upload" className="text-text/80 dark:text-dark-text/80 hover:text-primary dark:hover:text-secondary transition-colors font-medium">
            Upload
          </Link>
          {authed && (
            <Link to="/admin" className="text-text/80 dark:text-dark-text/80 hover:text-primary dark:hover:text-secondary transition-colors font-medium">
              Dashboard
            </Link>
          )}
          {!authed && (
            <>
              <Link to="/login" className="text-text/80 dark:text-dark-text/80 hover:text-primary dark:hover:text-secondary transition-colors font-medium">
                Login
              </Link>
              <Link to="/signup" className="btn-secondary text-sm">
                Sign Up
              </Link>
            </>
          )}
          <button 
            onClick={toggleDarkMode}
            className="p-2 rounded-full hover:bg-accent dark:hover:bg-dark-card transition-colors"
            aria-label="Toggle dark mode"
          >
            {darkMode ? '☀️' : '🌙'}
          </button>
          {authed && (
            <button 
              onClick={logout} 
              className="text-text/80 dark:text-dark-text/80 hover:text-red-500 transition-colors font-medium"
            >
              Logout
            </button>
          )}
        </nav>
      </div>
    </header>
  )
}


