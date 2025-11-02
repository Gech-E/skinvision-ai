import React from 'react'
import { Link } from 'react-router-dom'
import Navbar from '../components/Navbar'

export default function Home() {
  return (
    <div className="min-h-screen bg-accent dark:bg-dark-bg">
      <Navbar />
      
      {/* Hero Section */}
      <main className="max-w-7xl mx-auto px-6 py-16 md:py-24">
        <section className="text-center mb-20">
          <div className="text-6xl mb-6 animate-pulse">🧬✨</div>
          <h1 className="text-4xl md:text-6xl font-extrabold text-text dark:text-dark-text leading-tight mb-6">
            AI-Powered Skin Disease Detection
          </h1>
          <p className="text-xl md:text-2xl text-text/80 dark:text-dark-text/80 max-w-3xl mx-auto mb-10">
            Instant, accurate skin analysis powered by deep learning technology. 
            Get dermatologist-assisted insights in seconds.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Link 
              to="/upload" 
              className="rounded-2xl bg-primary text-white px-8 py-4 shadow-card hover:shadow-glow-hover transition-all font-semibold text-lg flex items-center gap-2 group"
            >
              <span>📤</span>
              <span>Upload Your Image for Analysis</span>
              <span className="group-hover:translate-x-1 transition-transform">→</span>
            </Link>
            <Link 
              to="/admin" 
              className="rounded-2xl bg-white dark:bg-dark-card text-text dark:text-dark-text px-6 py-4 border-2 border-secondary dark:border-dark-border hover:shadow-card transition-all font-semibold"
            >
              Admin Dashboard
            </Link>
          </div>
          
          <div className="flex flex-wrap justify-center gap-6 mt-12 text-sm text-text/70 dark:text-dark-text/70">
            <div className="flex items-center gap-2">
              <span className="text-xl">🔒</span>
              <span>100% Private</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xl">📱</span>
              <span>Mobile-Friendly</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xl">🩺</span>
              <span>Dermatologist-Reviewed</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xl">⚡</span>
              <span>Instant Results</span>
            </div>
          </div>
        </section>

        {/* Features Grid */}
        <section className="mt-24">
          <h2 className="text-3xl md:text-4xl font-bold text-text dark:text-dark-text text-center mb-12">
            Why Choose SkinVision AI?
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="bg-white dark:bg-dark-card rounded-2xl shadow-card border border-accent dark:border-dark-border p-6 hover:shadow-glow transition-all">
              <div className="text-4xl mb-4">🧠</div>
              <h3 className="text-xl font-semibold text-text dark:text-dark-text mb-2">AI-Powered Diagnosis</h3>
              <p className="text-sm text-text/70 dark:text-dark-text/70">
                Advanced deep learning algorithms trained on thousands of dermatological images provide instant, accurate analysis.
              </p>
            </div>
            
            <div className="bg-white dark:bg-dark-card rounded-2xl shadow-card border border-accent dark:border-dark-border p-6 hover:shadow-glow transition-all">
              <div className="text-4xl mb-4">👨‍⚕️</div>
              <h3 className="text-xl font-semibold text-text dark:text-dark-text mb-2">Dermatologist-Assisted Insights</h3>
              <p className="text-sm text-text/70 dark:text-dark-text/70">
                Get professional medical explanations and recommendations reviewed by certified dermatologists.
              </p>
            </div>
            
            <div className="bg-white dark:bg-dark-card rounded-2xl shadow-card border border-accent dark:border-dark-border p-6 hover:shadow-glow transition-all">
              <div className="text-4xl mb-4">🔥</div>
              <h3 className="text-xl font-semibold text-text dark:text-dark-text mb-2">Visual Explanations</h3>
              <p className="text-sm text-text/70 dark:text-dark-text/70">
                Grad-CAM heatmaps show exactly what the AI sees, making the analysis transparent and understandable.
              </p>
            </div>
            
            <div className="bg-white dark:bg-dark-card rounded-2xl shadow-card border border-accent dark:border-dark-border p-6 hover:shadow-glow transition-all">
              <div className="text-4xl mb-4">📄</div>
              <h3 className="text-xl font-semibold text-text dark:text-dark-text mb-2">Downloadable Reports</h3>
              <p className="text-sm text-text/70 dark:text-dark-text/70">
                Export detailed PDF reports to share with your healthcare provider.
              </p>
            </div>
            
            <div className="bg-white dark:bg-dark-card rounded-2xl shadow-card border border-accent dark:border-dark-border p-6 hover:shadow-glow transition-all">
              <div className="text-4xl mb-4">⚡</div>
              <h3 className="text-xl font-semibold text-text dark:text-dark-text mb-2">Instant Results</h3>
              <p className="text-sm text-text/70 dark:text-dark-text/70">
                Get analysis results in seconds, not days. Time-sensitive diagnosis made accessible.
              </p>
            </div>
            
            <div className="bg-white dark:bg-dark-card rounded-2xl shadow-card border border-accent dark:border-dark-border p-6 hover:shadow-glow transition-all">
              <div className="text-4xl mb-4">🔐</div>
              <h3 className="text-xl font-semibold text-text dark:text-dark-text mb-2">Secure & Private</h3>
              <p className="text-sm text-text/70 dark:text-dark-text/70">
                Your health data is encrypted and kept completely private. HIPAA-compliant security measures.
              </p>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="mt-24 bg-gradient-to-r from-primary to-secondary rounded-2xl p-12 text-center text-white">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Ready to Get Started?</h2>
          <p className="text-xl mb-8 opacity-90">Upload your skin image and get instant AI-powered analysis</p>
          <Link 
            to="/upload" 
            className="inline-flex items-center gap-2 rounded-2xl bg-white text-primary px-8 py-4 shadow-lg hover:shadow-xl transition-all font-semibold text-lg"
          >
            <span>🚀</span>
            <span>Start Analysis Now</span>
          </Link>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-text dark:bg-dark-card text-white dark:text-dark-text py-8 mt-20">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <p className="mb-2 font-semibold">SkinVision AI - Powered by Deep Learning Technology</p>
          <p className="text-sm opacity-80">
            This tool is for informational purposes only and does not replace professional medical advice.
          </p>
        </div>
      </footer>
    </div>
  )
}


