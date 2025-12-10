import axios from 'axios'

const API_BASE = (import.meta.env.VITE_API_BASE || 'http://localhost:5000').replace(/\/$/, '')

const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 45000,
})

function handleError(error) {
  if (error?.response?.data?.error) {
    throw new Error(error.response.data.error)
  }
  if (error?.message) {
    throw error
  }
  throw new Error('Unexpected error communicating with the backend service')
}

export async function predictSkinLesion(file) {
  try {
    const formData = new FormData()
    formData.append('file', file)
    const { data } = await apiClient.post('/predict', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return data
  } catch (error) {
    handleError(error)
  }
}

export async function savePredictionResult(payload) {
  try {
    const { data } = await apiClient.post('/save-result', payload)
    return data
  } catch (error) {
    handleError(error)
  }
}

export async function fetchPredictionHistory(limit = 25) {
  try {
    const { data } = await apiClient.get('/history', { params: { limit } })
    return data.items ?? []
  } catch (error) {
    handleError(error)
  }
}

export { API_BASE as API }
