import React from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'
import PredictionCard from '../components/PredictionCard'
import HeatmapSlider from '../components/HeatmapSlider'
import axios from 'axios'

const API = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export default function Result() {
  const location = useLocation()
  const navigate = useNavigate()
  const [result, setResult] = React.useState(null)

  React.useEffect(() => {
    // Get result from location state or sessionStorage
    const stateResult = location.state
    const storedResult = sessionStorage.getItem('predictionResult')
    
    if (stateResult) {
      setResult(stateResult)
    } else if (storedResult) {
      try {
        setResult(JSON.parse(storedResult))
      } catch (e) {
        console.error('Failed to parse stored result')
      }
    } else {
      // No result available, redirect to upload
      navigate('/upload')
    }
  }, [location.state, navigate])

  if (!result) {
    return (
      <div className="min-h-screen bg-accent dark:bg-dark-bg">
        <Navbar />
        <main className="max-w-6xl mx-auto px-6 py-10">
          <div className="text-center">Loading results...</div>
        </main>
      </div>
    )
  }

  const { predicted_class: disease, confidence, image_url, heatmap_url } = result
  const apiBase = API.replace('/predict', '')
  const imageUrl = image_url?.startsWith('http') ? image_url : `${apiBase}${image_url}`
  const heatmapImageUrl = heatmap_url?.startsWith('http') ? heatmap_url : `${apiBase}${heatmap_url}`

  const severity = confidence >= 0.8 ? 'High' : confidence >= 0.5 ? 'Medium' : 'Low'
  const getAdvice = (severity) => {
    if (severity === 'High') return 'Consult a dermatologist within 3–7 days. This requires immediate medical attention.'
    if (severity === 'Medium') return 'Book an appointment within 2–4 weeks for professional evaluation.'
    return 'Monitor the area and consider rechecking in 8–12 weeks if changes occur.'
  }
  const advice = getAdvice(severity)

  const handleDownloadPDF = () => {
    // Placeholder for PDF generation
    alert('PDF report generation will be implemented with a backend endpoint')
  }

  const handleRequestReview = () => {
    alert('Dermatologist review request feature coming soon')
  }

  return (
    <div className="min-h-screen bg-accent dark:bg-dark-bg">
      <Navbar />
      <main className="max-w-6xl mx-auto px-6 py-10 space-y-6">
        <h2 className="text-3xl font-semibold text-text dark:text-dark-text">Analysis Results</h2>
        <div className="grid lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <PredictionCard disease={disease} confidence={confidence} />
            
            <div className="bg-white dark:bg-dark-card rounded-2xl shadow-card border border-accent dark:border-dark-border p-5">
              <div className="flex items-center gap-2 mb-4">
                <span className="text-lg"></span>
                <h3 className="text-lg font-semibold text-text dark:text-dark-text">Grad-CAM Heatmap Visualization</h3>
              </div>
              <HeatmapSlider imageUrl={imageUrl} heatmapUrl={heatmapImageUrl} />
              <p className="text-xs text-text/60 dark:text-dark-text/60 mt-3">
                Slide to compare original image and AI attention heatmap. Red areas indicate regions the AI focused on for diagnosis.
              </p>
            </div>

            <div className="bg-white dark:bg-dark-card rounded-2xl shadow-card border border-accent dark:border-dark-border p-5">
              <h3 className="text-lg font-semibold text-text dark:text-dark-text mb-3">What This Means</h3>
              <p className="text-sm text-text/80 dark:text-dark-text/80 leading-relaxed">
                The AI has analyzed your skin image and identified it as <strong>{disease}</strong> with {(confidence * 100).toFixed(1)}% confidence. 
                The heatmap visualization shows which areas of the image were most important in making this diagnosis. 
                This tool is for informational purposes only and should not replace professional medical advice.
              </p>
            </div>
          </div>
          
          <div className="space-y-6">
            <div className="bg-white dark:bg-dark-card rounded-2xl shadow-card border border-accent dark:border-dark-border p-5">
              <div className="flex items-center gap-2 mb-4">
                <span className="text-lg"></span>
                <h3 className="text-lg font-semibold text-text dark:text-dark-text">Recommendation</h3>
              </div>
              <div className="space-y-3">
                <div>
                  <div className="text-sm text-text/70 dark:text-dark-text/70 mb-1">Urgency Level</div>
                  <div className={`inline-flex px-3 py-1 rounded-full text-sm font-semibold ${
                    severity === 'High' ? 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400' :
                    severity === 'Medium' ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400' :
                    'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
                  }`}>
                    {severity}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-text/70 dark:text-dark-text/70 mb-1">Next Steps</div>
                  <div className="text-text dark:text-dark-text font-medium">{advice}</div>
                </div>
              </div>
            </div>
            
            <div className="bg-white dark:bg-dark-card rounded-2xl shadow-card border border-accent dark:border-dark-border p-5">
              <h3 className="text-lg font-semibold text-text dark:text-dark-text mb-4">Actions</h3>
              <div className="flex flex-col gap-3">
                <button 
                  onClick={handleDownloadPDF}
                  className="rounded-2xl bg-primary text-white px-4 py-3 shadow-card hover:shadow-glow-hover transition-all font-medium flex items-center justify-center gap-2"
                >
                  <span></span>
                  <span>Download Report (PDF)</span>
                </button>
                <button 
                  onClick={handleRequestReview}
                  className="rounded-2xl bg-white dark:bg-dark-card text-text dark:text-dark-text px-4 py-3 border border-secondary dark:border-dark-border hover:shadow-card transition-all font-medium flex items-center justify-center gap-2"
                >
                  <span></span>
                  <span>Request Dermatologist Review</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}


