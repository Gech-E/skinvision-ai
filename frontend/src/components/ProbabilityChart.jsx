export default function ProbabilityChart({ probabilities = [] }) {
  if (!probabilities.length) {
    return null
  }

  const maxScore = probabilities[0]?.score ?? 0

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-slate-800">Probability distribution</h3>
        <span className="text-xs uppercase tracking-wide text-slate-500">Model output</span>
      </div>
      <ul className="space-y-2">
        {probabilities.map(({ label, score }) => {
          const pct = Math.round(score * 1000) / 10
          const width = maxScore ? Math.max((score / maxScore) * 100, 5) : 5
          return (
            <li key={label} className="space-y-1">
              <div className="flex items-center justify-between text-sm text-slate-600">
                <span className="font-medium text-slate-700">{label.toUpperCase()}</span>
                <span>{pct.toFixed(1)}%</span>
              </div>
              <div className="h-3 w-full rounded-full bg-slate-200">
                <div
                  className="h-full rounded-full bg-gradient-to-r from-indigo-500 to-cyan-500"
                  style={{ width: `${width}%` }}
                  role="progressbar"
                  aria-valuenow={pct}
                  aria-valuemin={0}
                  aria-valuemax={100}
                />
              </div>
            </li>
          )
        })}
      </ul>
    </div>
  )
}
