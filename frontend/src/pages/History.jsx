import { useEffect, useState } from 'react'
import HistoryTable from '../components/HistoryTable'
import { fetchPredictionHistory } from '../utils/api'

export default function HistoryPage() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    let ignore = false

    const load = async () => {
      setLoading(true)
      setError(null)
      try {
        const data = await fetchPredictionHistory(50)
        if (!ignore) setItems(data)
      } catch (err) {
        console.error(err)
        if (!ignore) setError(err?.message || 'Unable to load history')
      } finally {
        if (!ignore) setLoading(false)
      }
    }

    load()
    return () => {
      ignore = true
    }
  }, [])

  return (
    <section className="space-y-6">
      <div>
        <p className="text-sm font-semibold uppercase tracking-wide text-indigo-500">Prediction archive</p>
        <h2 className="text-4xl font-bold text-slate-900">Review saved results</h2>
        <p className="text-slate-500">All saved predictions are persisted in PostgreSQL via the Flask API.</p>
      </div>
      {error && <p className="text-sm text-red-600">{error}</p>}
      <HistoryTable items={items} loading={loading} />
    </section>
  )
}
