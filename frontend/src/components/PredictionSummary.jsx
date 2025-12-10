import ProbabilityChart from './ProbabilityChart'

export default function PredictionSummary({ result, onSave, saving, onReset }) {
  if (!result) return null

  const confidencePercent = (result.confidence * 100).toFixed(2)

  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <p className="text-sm uppercase tracking-wide text-slate-500">Predicted class</p>
          <p className="text-3xl font-bold text-slate-900">{result.predicted_class.toUpperCase()}</p>
        </div>
        <div className="text-right">
          <p className="text-sm uppercase tracking-wide text-slate-500">Confidence</p>
          <p className="text-3xl font-semibold text-indigo-600">{confidencePercent}%</p>
        </div>
      </div>
      <div className="my-6 border-t border-slate-100" />
      <ProbabilityChart probabilities={result.probabilities} />
      <div className="mt-8 flex flex-wrap gap-4">
        <button
          onClick={onSave}
          disabled={saving}
          className="inline-flex items-center justify-center rounded-full bg-indigo-600 px-6 py-3 text-sm font-semibold text-white transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {saving ? 'Saving...' : 'Save Result'}
        </button>
        <button
          onClick={onReset}
          className="inline-flex items-center justify-center rounded-full border border-slate-300 px-5 py-3 text-sm font-semibold text-slate-600 transition hover:border-slate-400"
        >
          Start Over
        </button>
      </div>
    </section>
  )
}
