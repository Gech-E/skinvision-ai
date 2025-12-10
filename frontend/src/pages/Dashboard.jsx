import { useCallback, useEffect, useMemo, useState } from 'react'
import ImageUploader from '../components/ImageUploader'
import PredictionSummary from '../components/PredictionSummary'
import { predictSkinLesion, savePredictionResult } from '../utils/api'

export default function DashboardPage() {
  const [file, setFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState(null)
  const [saveMessage, setSaveMessage] = useState(null)

  const handleSelect = useCallback((selectedFile) => {
    if (previewUrl) URL.revokeObjectURL(previewUrl)
    setFile(selectedFile)
    setPreviewUrl(URL.createObjectURL(selectedFile))
    setResult(null)
    setError(null)
    setSaveMessage(null)
  }, [previewUrl])

  const handlePredict = async () => {
    if (!file) {
      setError('Please select an image first.')
      return
    }
    setLoading(true)
    setError(null)
    setSaveMessage(null)
    try {
      const prediction = await predictSkinLesion(file)
      setResult(prediction)
    } catch (err) {
      console.error(err)
      setError(err?.message || 'Prediction failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async () => {
    if (!result) return
    setSaving(true)
    setSaveMessage(null)
    try {
      const saved = await savePredictionResult({
        predicted_class: result.predicted_class,
        confidence: result.confidence,
        image_path: result.image_path,
      })
      setSaveMessage(`Saved prediction #${saved.id}`)
    } catch (err) {
      console.error(err)
      setError(err?.message || 'Could not save the prediction.')
    } finally {
      setSaving(false)
    }
  }

  const handleReset = () => {
    if (previewUrl) URL.revokeObjectURL(previewUrl)
    setFile(null)
    setPreviewUrl(null)
    setResult(null)
    setError(null)
    setSaveMessage(null)
  }

  const helperText = useMemo(() => {
    if (loading) return 'Analyzing image, please wait...'
    if (saveMessage) return saveMessage
    if (error) return error
    return 'Upload high-resolution dermatoscopic imagery for best results.'
  }, [loading, saveMessage, error])

  useEffect(() => {
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl)
      }
    }
  }, [previewUrl])

  return (
    <div className="space-y-8">
      <section className="rounded-3xl border border-slate-200 bg-white/90 p-8 shadow-sm backdrop-blur">
        <div className="space-y-2">
          <p className="text-sm font-semibold uppercase tracking-wide text-indigo-500">Skin Cancer Screening</p>
          <h2 className="text-4xl font-bold text-slate-900">Upload & Analyze</h2>
          <p className="text-slate-500">{helperText}</p>
        </div>
        <div className="mt-8 space-y-6">
          <ImageUploader onSelect={handleSelect} previewUrl={previewUrl} disabled={loading} error={error} />
          <div className="flex flex-wrap gap-4">
            <button
              onClick={handlePredict}
              disabled={!file || loading}
              className="inline-flex items-center justify-center rounded-full bg-indigo-600 px-8 py-3 text-base font-semibold text-white transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading ? 'Analyzing...' : 'Predict'}
            </button>
            {file && !loading && (
              <button
                onClick={handleReset}
                className="inline-flex items-center justify-center rounded-full border border-slate-300 px-6 py-3 text-base font-semibold text-slate-600 transition hover:border-slate-400"
              >
                Clear Selection
              </button>
            )}
          </div>
        </div>
      </section>

      <PredictionSummary result={result} onSave={handleSave} saving={saving} onReset={handleReset} />
    </div>
  )
}
