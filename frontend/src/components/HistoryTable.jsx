function formatDate(value) {
  if (!value) return '—'
  try {
    return new Date(value).toLocaleString()
  } catch {
    return value
  }
}

export default function HistoryTable({ items = [], loading }) {
  if (loading) {
    return <p className="text-slate-500">Loading history...</p>
  }

  if (!items.length) {
    return <p className="text-slate-500">No predictions saved yet.</p>
  }

  return (
    <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
      <table className="min-w-full divide-y divide-slate-100">
        <thead className="bg-slate-50">
          <tr>
            <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">ID</th>
            <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">Class</th>
            <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">Confidence</th>
            <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">Image Path</th>
            <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">Timestamp</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {items.map((item) => {
            const confidenceValue =
              typeof item.confidence === 'number' ? `${(item.confidence * 100).toFixed(2)}%` : '—'
            return (
              <tr key={item.id} className="hover:bg-slate-50">
                <td className="px-4 py-3 text-sm text-slate-600">#{item.id}</td>
                <td className="px-4 py-3 text-sm font-semibold text-slate-800">{item.predicted_class?.toUpperCase()}</td>
                <td className="px-4 py-3 text-sm text-slate-600">{confidenceValue}</td>
                <td className="px-4 py-3 text-sm text-indigo-600">{item.image_path || '—'}</td>
                <td className="px-4 py-3 text-sm text-slate-500">{formatDate(item.timestamp)}</td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}
