import React from 'react'

export default function HistoryTable({ rows = [], onDelete }) {
  return (
    <div className="overflow-x-auto border border-background rounded-2xl">
      <table className="min-w-full text-sm">
        <thead className="bg-background">
          <tr>
            <th className="text-left px-4 py-3 font-semibold text-text">Time</th>
            <th className="text-left px-4 py-3 font-semibold text-text">Image</th>
            <th className="text-left px-4 py-3 font-semibold text-text">Class</th>
            <th className="text-left px-4 py-3 font-semibold text-text">Confidence</th>
            <th className="text-left px-4 py-3 font-semibold text-text">Action</th>
          </tr>
        </thead>
        <tbody>
          {rows.map(r => (
            <tr key={r.id} className="odd:bg-white even:bg-background/50">
              <td className="px-4 py-3 text-text/90">{new Date(r.timestamp).toLocaleString()}</td>
              <td className="px-4 py-3"><img src={r.image_url} alt="thumb" className="w-12 h-12 rounded" /></td>
              <td className="px-4 py-3 text-text">{r.predicted_class}</td>
              <td className="px-4 py-3 text-text">{(r.confidence * 100).toFixed(0)}%</td>
              <td className="px-4 py-3">
                <button onClick={() => onDelete?.(r.id)} className="text-red-600 hover:underline">Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}


