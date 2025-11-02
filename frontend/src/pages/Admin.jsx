import React from 'react'
import Navbar from '../components/Navbar'
import HistoryTable from '../components/HistoryTable'
import OTPModal from '../components/OTPModal'
import axios from 'axios'

const API = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

// Simple SVG Bar Chart Component
function BarChart({ data, title }) {
  const maxValue = Math.max(...Object.values(data), 1)
  const entries = Object.entries(data)
  const barWidth = 280 / entries.length - 5

  return (
    <div className="space-y-2">
      <h3 className="text-sm font-semibold text-text dark:text-dark-text mb-3">{title}</h3>
      <svg width="100%" height="200" viewBox="0 0 300 200" className="overflow-visible">
        {entries.map(([label, value], i) => {
          const height = (value / maxValue) * 160
          const x = i * (barWidth + 5) + 10
          const y = 180 - height
          return (
            <g key={label}>
              <rect
                x={x}
                y={y}
                width={barWidth}
                height={height}
                fill="url(#gradient)"
                rx="4"
                className="hover:opacity-80 transition-opacity"
              />
              <text
                x={x + barWidth / 2}
                y={195}
                textAnchor="middle"
                className="text-[8px] fill-text dark:fill-dark-text"
              >
                {label.substring(0, 6)}
              </text>
              <text
                x={x + barWidth / 2}
                y={y - 5}
                textAnchor="middle"
                className="text-[9px] font-semibold fill-primary"
              >
                {value}
              </text>
            </g>
          )
        })}
        <defs>
          <linearGradient id="gradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#3AAFA9" />
            <stop offset="100%" stopColor="#2B7A78" />
          </linearGradient>
        </defs>
      </svg>
    </div>
  )
}

// Simple SVG Line Chart Component
function LineChart({ data, title }) {
  const points = data.map((val, i) => ({
    x: 20 + (i * 260) / (data.length - 1 || 1),
    y: 160 - (val / Math.max(...data, 1)) * 140
  }))

  const pathData = points.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ')

  return (
    <div className="space-y-2">
      <h3 className="text-sm font-semibold text-text dark:text-dark-text mb-3">{title}</h3>
      <svg width="100%" height="200" viewBox="0 0 300 200" className="overflow-visible">
        <path
          d={pathData}
          fill="none"
          stroke="#2B7A78"
          strokeWidth="2"
          className="drop-shadow-sm"
        />
        {points.map((p, i) => (
          <circle
            key={i}
            cx={p.x}
            cy={p.y}
            r="4"
            fill="#2B7A78"
            className="hover:r-6 transition-all"
          />
        ))}
        <line x1="20" y1="160" x2="280" y2="160" stroke="#DEF2F1" strokeWidth="1" />
        <text x="150" y="195" textAnchor="middle" className="text-[8px] fill-text/60 dark:fill-dark-text/60">
          Time
        </text>
      </svg>
    </div>
  )
}

export default function Admin() {
  const [rows, setRows] = React.useState([])
  const [loading, setLoading] = React.useState(true)
  const [showOTPModal, setShowOTPModal] = React.useState(false)
  const [userEmail, setUserEmail] = React.useState('')
  const [otpSessionToken, setOtpSessionToken] = React.useState(null)

  async function load(requireOTP = false) {
    try {
      const token = localStorage.getItem('token')
      const otpSession = localStorage.getItem('otp_session')
      
      if (!token) {
        alert('Please login to access admin dashboard')
        window.location.href = '/login'
        return
      }

      // Use OTP session token if available, otherwise regular token
      const authToken = otpSession || token
      const headers = { Authorization: `Bearer ${authToken}` }
      
      // If OTP is required but we don't have a session, show modal
      if (requireOTP && !otpSession) {
        // Fetch user email first
        try {
          const userResponse = await axios.get(`${API}/notifications/settings`, { headers: { Authorization: `Bearer ${token}` } })
          setUserEmail(userResponse.data.email)
          setShowOTPModal(true)
          return
        } catch (e) {
          console.error('Failed to get user info:', e)
        }
      }

      const { data } = await axios.get(`${API}/history/?all=true${requireOTP ? '&require_otp=true' : ''}`, { 
        headers 
      })
      setRows(data)
    } catch (error) {
      console.error('Failed to load history:', error)
      if (error.response?.status === 401 || error.response?.status === 403) {
        if (error.response?.status === 403 && error.response?.data?.detail?.includes('OTP')) {
          // OTP required
          const token = localStorage.getItem('token')
          try {
            const userResponse = await axios.get(`${API}/notifications/settings`, { headers: { Authorization: `Bearer ${token}` } })
            setUserEmail(userResponse.data.email)
            setShowOTPModal(true)
            return
          } catch (e) {
            console.error('Failed to get user info:', e)
          }
        } else {
          localStorage.removeItem('token')
          localStorage.removeItem('otp_session')
          window.location.href = '/login'
        }
      }
    } finally {
      setLoading(false)
    }
  }

  function handleOTPVerify(sessionToken) {
    setOtpSessionToken(sessionToken)
    localStorage.setItem('otp_session', sessionToken)
    // Reload with OTP session
    load(true)
  }

  async function remove(id) {
    const token = localStorage.getItem('token')
    try {
      await axios.delete(`${API}/history/${id}`, { headers: { Authorization: `Bearer ${token}` } })
      load()
    } catch (error) {
      alert('Failed to delete record')
    }
  }

  React.useEffect(() => { 
    // Try to load without OTP first, but will prompt if required
    load(false) 
  }, [])

  // Calculate chart data
  const diseaseCount = rows.reduce((acc, row) => {
    acc[row.predicted_class] = (acc[row.predicted_class] || 0) + 1
    return acc
  }, {})

  // Group by week
  const weeklyData = React.useMemo(() => {
    const weeks = {}
    rows.forEach(row => {
      const date = new Date(row.timestamp)
      const week = `${date.getFullYear()}-W${Math.ceil(date.getDate() / 7)}`
      weeks[week] = (weeks[week] || 0) + 1
    })
    return Object.values(weeks).slice(-8) // Last 8 weeks
  }, [rows])

  if (loading) {
    return (
      <div className="min-h-screen bg-accent dark:bg-dark-bg">
        <Navbar />
        <main className="max-w-7xl mx-auto px-6 py-10">
          <div className="text-center">Loading dashboard...</div>
        </main>
      </div>
    )
  }

      return (
        <div className="min-h-screen bg-accent dark:bg-dark-bg">
          <Navbar />
          <OTPModal
            isOpen={showOTPModal}
            onClose={() => setShowOTPModal(false)}
            onVerify={handleOTPVerify}
            identifier={userEmail}
            method="email"
          />
          <main className="max-w-7xl mx-auto px-6 py-10 space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-3xl font-bold text-text dark:text-dark-text">Admin Dashboard</h2>
              <div className="flex gap-2">
                <button
                  onClick={() => load(true)}
                  className="rounded-2xl bg-secondary text-white px-4 py-2 shadow-card hover:shadow-glow transition-all text-sm font-medium"
                  title="Reload with OTP verification"
                >
                  🔐 Secure Reload
                </button>
                <button
                  onClick={() => load(false)}
                  className="rounded-2xl bg-primary text-white px-4 py-2 shadow-card hover:shadow-glow transition-all text-sm font-medium"
                >
                  🔄 Refresh
                </button>
              </div>
            </div>

        {/* Stats Cards */}
        <div className="grid md:grid-cols-4 gap-4">
          <div className="bg-white dark:bg-dark-card rounded-2xl shadow-card border border-accent dark:border-dark-border p-4">
            <div className="text-sm text-text/70 dark:text-dark-text/70 mb-1">Total Predictions</div>
            <div className="text-2xl font-bold text-primary">{rows.length}</div>
          </div>
          <div className="bg-white dark:bg-dark-card rounded-2xl shadow-card border border-accent dark:border-dark-border p-4">
            <div className="text-sm text-text/70 dark:text-dark-text/70 mb-1">Disease Classes</div>
            <div className="text-2xl font-bold text-secondary">{Object.keys(diseaseCount).length}</div>
          </div>
          <div className="bg-white dark:bg-dark-card rounded-2xl shadow-card border border-accent dark:border-dark-border p-4">
            <div className="text-sm text-text/70 dark:text-dark-text/70 mb-1">Avg Confidence</div>
            <div className="text-2xl font-bold text-primary">
              {rows.length > 0 
                ? ((rows.reduce((sum, r) => sum + r.confidence, 0) / rows.length) * 100).toFixed(1)
                : 0}%
            </div>
          </div>
          <div className="bg-white dark:bg-dark-card rounded-2xl shadow-card border border-accent dark:border-dark-border p-4">
            <div className="text-sm text-text/70 dark:text-dark-text/70 mb-1">This Week</div>
            <div className="text-2xl font-bold text-secondary">
              {weeklyData.slice(-1)[0] || 0}
            </div>
          </div>
        </div>

        <div className="grid lg:grid-cols-2 gap-6">
          {/* Prediction History Table */}
          <div className="bg-white dark:bg-dark-card rounded-2xl shadow-card border border-accent dark:border-dark-border p-5">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-text dark:text-dark-text">Prediction History</h3>
              <span className="text-sm text-text/60 dark:text-dark-text/60">{rows.length} records</span>
            </div>
            <div className="overflow-x-auto max-h-96">
              <HistoryTable rows={rows} onDelete={remove} />
            </div>
          </div>

          {/* Charts */}
          <div className="space-y-6">
            <div className="bg-white dark:bg-dark-card rounded-2xl shadow-card border border-accent dark:border-dark-border p-5">
              <BarChart 
                data={diseaseCount} 
                title="Disease Distribution"
              />
            </div>
            <div className="bg-white dark:bg-dark-card rounded-2xl shadow-card border border-accent dark:border-dark-border p-5">
              <LineChart 
                data={weeklyData.length > 0 ? weeklyData : [0, 0, 0, 0, 0, 0, 0, 0]} 
                title="Predictions Per Week (Last 8 Weeks)"
              />
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}


