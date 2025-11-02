import React from 'react'
import Navbar from '../components/Navbar'
import axios from 'axios'
import { useNavigate, Link } from 'react-router-dom'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'
const API = API_BASE.replace(/\/$/, '') // Remove trailing slash

export default function Login() {
  const [email, setEmail] = React.useState('')
  const [password, setPassword] = React.useState('')
  const [error, setError] = React.useState('')
  const navigate = useNavigate()

  async function submit(e) {
    e.preventDefault()
    setError('')
    
    if (!email || !password) {
      setError('Please enter both email and password')
      return
    }
    
    try {
      const { data } = await axios.post(`${API}/auth/login`, { email, password })
      localStorage.setItem('token', data.access_token)
      navigate('/admin')
    } catch (err) {
      console.error('Login error:', err)
      const errorMessage = err?.response?.data?.detail || err?.response?.status === 401 
        ? 'Invalid email or password. Please try again.' 
        : 'Login failed. Please check your connection and try again.'
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
          
          {error && (
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-3">
              <div className="flex items-center gap-2 text-red-600 dark:text-red-400 text-sm">
                <span>⚠️</span>
                <span>{error}</span>
              </div>
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


