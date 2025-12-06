import React from 'react'
import { useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'
import UploadCard from '../components/UploadCard'
import axios from 'axios'

const API = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export default function Upload() {
  const navigate = useNavigate()
  const [preview, setPreview] = React.useState(null)
  const [file, setFile] = React.useState(null)
  const [loading, setLoading] = React.useState(false)
  const [progress, setProgress] = React.useState(0)

  function onFiles(files) {
    const f = files[0]
    if (!f) return
    setFile(f)
    setPreview(URL.createObjectURL(f))
    setProgress(0)
  }

  async function submit() {
    if (!file) return
    setLoading(true)
    setProgress(0)
    
    try {
      const fd = new FormData()
      fd.append('file', file)
      const token = localStorage.getItem('token')
      
      // Simulate progress
      const progressInterval = setInterval(() => {
        setProgress(prev => Math.min(prev + 10, 90))
      }, 200)
      
      const { data } = await axios.post(`${API}/predict`, fd, { 
        headers: token ? { Authorization: `Bearer ${token}` } : {},
        onUploadProgress: (progressEvent) => {
          const percent = Math.round((progressEvent.loaded * 0.5) / progressEvent.total * 100)
          setProgress(percent)
        }
      })
      
      clearInterval(progressInterval)
      setProgress(100)
      
      // Store result in sessionStorage and navigate to results page
      sessionStorage.setItem('predictionResult', JSON.stringify(data))
      setTimeout(() => {
        navigate('/result', { state: data })
      }, 500)
    } catch (error) {
      console.error('Prediction error:', error)
      alert('Failed to analyze image. Please try again.')
      setProgress(0)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-accent dark:bg-dark-bg">
      <Navbar />
      <main className="max-w-4xl mx-auto px-6 py-10">
        <h2 className="text-3xl font-semibold text-text dark:text-dark-text mb-6 text-center">
          Upload Your Skin Image
        </h2>
        <div className="bg-white dark:bg-dark-card rounded-2xl shadow-card border border-accent dark:border-dark-border p-6 space-y-6">
          <UploadCard onFiles={onFiles} previewUrl={preview} />
          
          {/* Progress Bar */}
          {loading && (
            <div className="space-y-2">
              <div className="flex justify-between text-sm text-text/70 dark:text-dark-text/70">
                <span>Analyzing image...</span>
                <span>{progress}%</span>
              </div>
              <div className="w-full h-2.5 bg-accent dark:bg-dark-border rounded-full overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-primary to-secondary transition-all duration-300"
                  style={{ width: `${progress}%` }}
                />
              </div>
            </div>
          )}
          
          <div className="pt-4 flex gap-3 justify-center">
            <button 
              onClick={submit} 
              className="rounded-2xl bg-primary text-white px-8 py-3 shadow-card hover:shadow-glow-hover transition-all disabled:opacity-60 disabled:cursor-not-allowed font-semibold flex items-center gap-2"
              disabled={!file || loading}
            >
              {loading ? (
                <>
                  <span className="animate-spin">⚙️</span>
                  <span>Analyzing...</span>
                </>
              ) : (
                <>
                  <span></span>
                  <span>Analyze Image</span>
                </>
              )}
            </button>
            <button 
              onClick={() => { 
                setFile(null)
                setPreview(null)
                setProgress(0)
                if (preview) URL.revokeObjectURL(preview)
              }} 
              className="rounded-2xl bg-white dark:bg-dark-card text-text dark:text-dark-text px-6 py-3 border border-secondary dark:border-dark-border hover:shadow-card transition-all"
              disabled={loading}
            >
              Reset
            </button>
          </div>
        </div>
      </main>
    </div>
  )
}


