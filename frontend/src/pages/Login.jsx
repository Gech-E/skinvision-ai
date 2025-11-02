import React from 'react'
import Navbar from '../components/Navbar'
import apiClient, { API, testBackendConnection } from '../utils/api'
import { useNavigate, Link } from 'react-router-dom'

export default function Login() {
  const [email, setEmail] = React.useState('')
  const [password, setPassword] = React.useState('')
  const [error, setError] = React.useState('')
  const [checkingConnection, setCheckingConnection] = React.useState(false)
  const navigate = useNavigate()

  // Check backend connection on component mount
  React.useEffect(() => {
    async function checkConnection() {
      setCheckingConnection(true)
      const result = await testBackendConnection()
      if (!result.success) {
        setError(`⚠️ ${result.message}`)
      }
      setCheckingConnection(false)
    }
    checkConnection()
  }, [])

  async function submit(e) {
    e.preventDefault()
    setError('')
    
    if (!email || !password) {
      setError('Please enter both email and password')
      return
    }
    
    try {
      const { data } = await apiClient.post('/auth/login', { email, password })
      localStorage.setItem('token', data.access_token)
      navigate('/admin')
    } catch (err) {
      console.error('Login error:', err)
      const errorMessage = err?.response?.data?.detail || err.message || 
        (err?.response?.status === 401 
          ? 'Invalid email or password. Please try again.' 
          : 'Login failed. Please check your connection and try again.')
      setError(errorMessage)
    }
  }

  return (
    <div className="min-h-screen bg-accent dark:bg-dark-bg">
      <Navbar />
      <main className="max-w-md mx-auto px-4 sm:px-6 py-8 sm:py-12 md:py-16">
        <form onSubmit={submit} className="bg-white dark:bg-dark-card rounded-2xl shadow-card border border-accent dark:border-dark-border p-5 sm:p-6 md:p-8 space-y-4 sm:space-y-5">
          <div className="text-center mb-4 sm:mb-6">
            <h2 className="text-xl sm:text-2xl md:text-3xl font-semibold text-text dark:text-dark-text">Login</h2>
            <p className="text-xs sm:text-sm text-text/70 dark:text-dark-text/70 mt-1 sm:mt-2">Sign in to access admin dashboard</p>
          </div>
          
          {checkingConnection && (
            <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-3">
              <div className="flex items-center gap-2 text-blue-600 dark:text-blue-400 text-sm">
                <span>🔄</span>
                <span>Checking backend connection...</span>
              </div>
            </div>
          )}
          
          {error && (
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-3">
              <div className="flex items-center gap-2 text-red-600 dark:text-red-400 text-sm">
                <span>⚠️</span>
                <span>{error}</span>
              </div>
              {error.includes('localhost:8000') && (
                <div className="mt-2 text-xs text-red-500 dark:text-red-400">
                  <p>💡 <strong>Solution:</strong></p>
                  <ol className="list-decimal list-inside ml-2 mt-1 space-y-1">
                    <li>Open a new terminal and navigate to: <code className="bg-red-100 dark:bg-red-900 px-1 rounded">backend</code></li>
                    <li>Run: <code className="bg-red-100 dark:bg-red-900 px-1 rounded">python -m uvicorn app.main:app --reload --port 8000</code></li>
                    <li>Wait for "Application startup complete" message</li>
                    <li>Refresh this page and try again</li>
                  </ol>
                </div>
              )}
            </div>
          )}
          
          <label className="block">
            <span className="block mb-1.5 sm:mb-2 text-xs sm:text-sm font-medium text-text dark:text-dark-text">Email</span>
            <input 
              type="email"
              value={email} 
              onChange={e => setEmail(e.target.value)} 
              className="w-full rounded-xl sm:rounded-2xl border border-secondary dark:border-dark-border px-3 sm:px-4 py-2.5 sm:py-3 bg-white dark:bg-dark-card text-text dark:text-dark-text focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all text-sm sm:text-base" 
              placeholder="you@example.com"
              required
            />
          </label>
          
          <label className="block">
            <span className="block mb-1.5 sm:mb-2 text-xs sm:text-sm font-medium text-text dark:text-dark-text">Password</span>
            <input 
              type="password" 
              value={password} 
              onChange={e => setPassword(e.target.value)} 
              className="w-full rounded-xl sm:rounded-2xl border border-secondary dark:border-dark-border px-3 sm:px-4 py-2.5 sm:py-3 bg-white dark:bg-dark-card text-text dark:text-dark-text focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all text-sm sm:text-base"
              placeholder="Enter your password"
              required
            />
          </label>
          
          <button 
            type="submit"
            className="w-full rounded-xl sm:rounded-2xl bg-primary text-white px-4 sm:px-5 py-2.5 sm:py-3 shadow-card hover:shadow-glow-hover transition-all font-semibold text-sm sm:text-base disabled:opacity-60 disabled:cursor-not-allowed"
            disabled={!email || !password}
          >
            Sign In
          </button>
          
          <div className="text-xs sm:text-sm text-center text-text/70 dark:text-dark-text/70 pt-2">
            Don't have an account?{' '}
            <Link to="/signup" className="text-primary hover:underline font-medium">
              Sign up
            </Link>
          </div>
        </form>
      </main>
    </div>
  )
}


