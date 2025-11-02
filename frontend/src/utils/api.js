// Centralized API configuration
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'
export const API = API_BASE.replace(/\/$/, '') // Remove trailing slash

// Helper function to test backend connection
export async function testBackendConnection() {
  try {
    const response = await fetch(`${API}/`)
    const data = await response.json()
    return { success: true, data }
  } catch (error) {
    return { 
      success: false, 
      error: error.message,
      message: `Cannot connect to backend at ${API}. Make sure the backend server is running.`
    }
  }
}

// Enhanced axios instance with better error handling
import axios from 'axios'

const apiClient = axios.create({
  baseURL: API,
  timeout: 30000, // 30 second timeout
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for better error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Enhanced error handling
    if (error.code === 'ECONNABORTED') {
      error.message = 'Request timed out. The server may be slow or unreachable.'
    } else if (error.code === 'ERR_NETWORK' || error.message.includes('Network Error')) {
      error.message = `Cannot connect to backend server at ${API}. Please ensure the backend is running on http://localhost:8000`
    } else if (error.response) {
      // Server responded with error status
      const status = error.response.status
      if (status === 401) {
        error.message = 'Invalid email or password. Please try again.'
      } else if (status === 500) {
        error.message = 'Server error. Please try again later.'
      } else if (status === 404) {
        error.message = 'Endpoint not found. Please check the API configuration.'
      }
    }
    return Promise.reject(error)
  }
)

export default apiClient
