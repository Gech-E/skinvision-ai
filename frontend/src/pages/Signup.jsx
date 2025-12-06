import React from 'react'
import Navbar from '../components/Navbar'
import axios from 'axios'
import { useNavigate, Link } from 'react-router-dom'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'
const API = API_BASE.replace(/\/$/, '') // Remove trailing slash

export default function Signup() {
  const [email, setEmail] = React.useState('')
  const [password, setPassword] = React.useState('')
  const [error, setError] = React.useState('')
  const [success, setSuccess] = React.useState('')
  const navigate = useNavigate()

  async function submit(e) {
    e.preventDefault()
    setError('')
    setSuccess('')
    
    // Basic validation
    if (!email || !email.includes('@')) {
      setError('Please enter a valid email address')
      return
    }
    
    if (!password || password.length < 6) {
      setError('Password must be at least 6 characters')
      return
    }
    
    try {
      const response = await axios.post(`${API}/auth/signup`, { email, password })
      setSuccess(`Account created successfully! ${response.data.role === 'admin' ? 'You are an admin.' : ''} Redirecting to login...`)
      setTimeout(() => navigate('/login'), 1500)
    } catch (err) {
      console.error('Signup error:', err)
      console.error('Error response:', err?.response)
      
      // Better error message extraction
      let errorMessage = 'Signup failed. Please try again.'
      
      if (err?.response?.data) {
        if (typeof err.response.data === 'string') {
          errorMessage = err.response.data
        } else if (err.response.data.detail) {
          errorMessage = err.response.data.detail
        } else if (err.response.data.message) {
          errorMessage = err.response.data.message
        }
      } else if (err?.message) {
        if (err.message.includes('Network Error') || err.message.includes('Failed to fetch')) {
          errorMessage = 'Cannot connect to server. Please make sure the backend is running on http://localhost:8000'
        } else {
          errorMessage = err.message
        }
      }
      
      setError(errorMessage)
    }
  }

  return (
    <div className="min-h-screen bg-accent dark:bg-dark-bg">
      <Navbar />
      <main className="max-w-md mx-auto px-4 sm:px-6 py-8 sm:py-12 md:py-16">
        <form onSubmit={submit} className="bg-white dark:bg-dark-card rounded-2xl shadow-card border border-accent dark:border-dark-border p-5 sm:p-6 md:p-8 space-y-4 sm:space-y-5">
          <div className="text-center mb-4 sm:mb-6">
            <h2 className="text-xl sm:text-2xl md:text-3xl font-semibold text-text dark:text-dark-text">Create account</h2>
            <p className="text-xs sm:text-sm text-text/70 dark:text-dark-text/70 mt-1 sm:mt-2">First user becomes admin automatically</p>
          </div>
          
          {error && (
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-3">
              <div className="flex items-center gap-2 text-red-600 dark:text-red-400 text-sm">
                <span></span>
                <span>{error}</span>
              </div>
            </div>
          )}
          
          {success && (
            <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-3">
              <div className="flex items-center gap-2 text-green-600 dark:text-green-400 text-sm">
                <span></span>
                <span>{success}</span>
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
              placeholder="Minimum 6 characters"
              minLength={6}
              required
            />
            <p className="text-xs text-text/60 dark:text-dark-text/60 mt-1">Password must be at least 6 characters</p>
          </label>
          
          <button 
            type="submit"
            className="w-full rounded-xl sm:rounded-2xl bg-primary text-white px-4 sm:px-5 py-2.5 sm:py-3 shadow-card hover:shadow-glow-hover transition-all font-semibold text-sm sm:text-base disabled:opacity-60 disabled:cursor-not-allowed"
            disabled={!email || !password || password.length < 6}
          >
            Sign Up
          </button>
          
          <div className="text-xs sm:text-sm text-center text-text/70 dark:text-dark-text/70 pt-2">
            Already have an account?{' '}
            <Link to="/login" className="text-primary hover:underline font-medium">
              Log in
            </Link>
          </div>
        </form>
      </main>
    </div>
  )
}


