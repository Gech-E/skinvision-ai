import React from 'react'

export default function PredictionCard({ disease, confidence }) {
  const pct = Math.round((confidence ?? 0) * 100)
  const confidenceColor = pct >= 80 ? 'from-red-500 to-red-600' : 
                          pct >= 50 ? 'from-yellow-500 to-yellow-600' : 
                          'from-green-500 to-green-600'
  
  return (
    <div className="bg-white dark:bg-dark-card rounded-2xl shadow-card border border-accent dark:border-dark-border p-6">
      <div className="flex items-center gap-3 mb-4">
        <div className="text-3xl">🔬</div>
        <div>
          <div className="text-text/70 dark:text-dark-text/70 text-sm font-medium">Predicted Disease</div>
          <div className="text-3xl font-bold text-text dark:text-dark-text mt-1">{disease}</div>
        </div>
      </div>
      
      <div className="space-y-2">
        <div className="flex justify-between items-center text-sm">
          <span className="text-text/70 dark:text-dark-text/70 font-medium">AI Confidence Score</span>
          <span className="text-2xl font-bold text-primary">{pct}%</span>
        </div>
        <div className="w-full h-4 bg-accent dark:bg-dark-border rounded-full overflow-hidden">
          <div 
            className={`h-full bg-gradient-to-r ${confidenceColor} transition-all duration-500 rounded-full flex items-center justify-end pr-2`}
            style={{ width: `${pct}%` }}
          >
            {pct >= 15 && (
              <span className="text-[10px] font-bold text-white">{pct}%</span>
            )}
          </div>
        </div>
        <div className="text-xs text-text/60 dark:text-dark-text/60 mt-2">
          {pct >= 80 && "High confidence - Consider professional medical consultation"}
          {pct >= 50 && pct < 80 && "Moderate confidence - Monitor and seek advice if concerned"}
          {pct < 50 && "Lower confidence - Additional imaging may be beneficial"}
        </div>
      </div>
    </div>
  )
}


