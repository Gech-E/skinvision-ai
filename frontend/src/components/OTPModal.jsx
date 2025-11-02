import React from 'react'
import axios from 'axios'

const API = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export default function OTPModal({ isOpen, onClose, onVerify, identifier, method }) {
  const [otp, setOtp] = React.useState('')
  const [loading, setLoading] = React.useState(false)
  const [error, setError] = React.useState('')
  const [requesting, setRequesting] = React.useState(false)

  const handleRequestOTP = async () => {
    setRequesting(true)
    setError('')
    
    try {
      const token = localStorage.getItem('token')
      const response = await axios.post(
        `${API}/otp/request`,
        { email: identifier },
        { headers: { Authorization: `Bearer ${token}` } }
      )
      alert(`OTP sent to your ${response.data.method}!`)
    } catch (err) {
      setError(err?.response?.data?.detail || 'Failed to send OTP')
    } finally {
      setRequesting(false)
    }
  }

  const handleVerify = async () => {
    if (otp.length !== 6) {
      setError('Please enter a 6-digit OTP code')
      return
    }

    setLoading(true)
    setError('')

    try {
      const token = localStorage.getItem('token')
      const response = await axios.post(
        `${API}/otp/verify`,
        { email: identifier, otp },
        { headers: { Authorization: `Bearer ${token}` } }
      )

      // Store OTP session token
      localStorage.setItem('otp_session', response.data.session_token)
      
      // Call parent callback
      if (onVerify) {
        onVerify(response.data.session_token)
      }
      
      onClose()
    } catch (err) {
      setError(err?.response?.data?.detail || 'Invalid OTP. Please try again.')
      setOtp('')
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleVerify()
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-dark-card rounded-2xl shadow-card border border-accent dark:border-dark-border p-6 sm:p-8 max-w-md w-full">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-2xl font-bold text-text dark:text-dark-text">OTP Verification</h3>
          <button
            onClick={onClose}
            className="text-text/60 dark:text-dark-text/60 hover:text-text dark:hover:text-dark-text text-2xl"
          >
            ×
          </button>
        </div>

        <div className="space-y-4">
          <p className="text-sm text-text/70 dark:text-dark-text/70">
            For security, please enter the 6-digit OTP code sent to your {method} to access your prediction history.
          </p>

          {error && (
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-3">
              <div className="flex items-center gap-2 text-red-600 dark:text-red-400 text-sm">
                <span>⚠️</span>
                <span>{error}</span>
              </div>
            </div>
          )}

          <div>
            <label className="block mb-2 text-sm font-medium text-text dark:text-dark-text">
              Enter OTP Code
            </label>
            <input
              type="text"
              value={otp}
              onChange={(e) => {
                const val = e.target.value.replace(/\D/g, '').slice(0, 6)
                setOtp(val)
                setError('')
              }}
              onKeyPress={handleKeyPress}
              placeholder="000000"
              className="w-full rounded-xl border border-secondary dark:border-dark-border px-4 py-3 bg-white dark:bg-dark-card text-text dark:text-dark-text focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all text-center text-2xl tracking-widest font-mono"
              maxLength={6}
              autoFocus
            />
            <p className="text-xs text-text/60 dark:text-dark-text/60 mt-2 text-center">
              OTP code expires in 10 minutes
            </p>
          </div>

          <div className="flex gap-3 pt-2">
            <button
              onClick={handleVerify}
              disabled={otp.length !== 6 || loading}
              className="flex-1 rounded-xl bg-primary text-white px-4 py-3 shadow-card hover:shadow-glow-hover transition-all font-semibold disabled:opacity-60 disabled:cursor-not-allowed"
            >
              {loading ? 'Verifying...' : 'Verify OTP'}
            </button>
            <button
              onClick={handleRequestOTP}
              disabled={requesting}
              className="rounded-xl bg-white dark:bg-dark-card text-text dark:text-dark-text px-4 py-3 border border-secondary dark:border-dark-border hover:shadow-card transition-all font-medium disabled:opacity-60 disabled:cursor-not-allowed text-sm"
            >
              {requesting ? 'Sending...' : 'Resend'}
            </button>
          </div>

          <div className="pt-2 text-center">
            <button
              onClick={onClose}
              className="text-sm text-text/60 dark:text-dark-text/60 hover:text-primary transition-colors"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

