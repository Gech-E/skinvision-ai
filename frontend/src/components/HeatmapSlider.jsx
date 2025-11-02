import React from 'react'

export default function HeatmapSlider({ imageUrl, heatmapUrl }) {
  const [pos, setPos] = React.useState(50)
  const [error, setError] = React.useState(false)
  
  // Fallback for missing images
  const handleImageError = () => {
    setError(true)
  }

  if (error || !imageUrl || !heatmapUrl) {
    return (
      <div className="relative w-full h-64 bg-accent dark:bg-dark-border rounded-2xl border border-secondary dark:border-dark-border flex items-center justify-center">
        <p className="text-text/60 dark:text-dark-text/60">Image not available</p>
      </div>
    )
  }

  return (
    <div className="relative w-full overflow-hidden rounded-2xl border border-accent dark:border-dark-border bg-white dark:bg-dark-card">
      {/* Original Image (Background) */}
      <div className="relative w-full" style={{ paddingBottom: '75%' }}>
        <img 
          src={imageUrl} 
          alt="Original skin image" 
          className="absolute inset-0 w-full h-full object-contain"
          onError={handleImageError}
        />
      </div>
      
      {/* Heatmap Overlay (Foreground with slider control) */}
      <div className="absolute inset-0 pointer-events-none">
        <div 
          className="absolute inset-0 overflow-hidden border-r-4 border-white dark:border-dark-card"
          style={{ width: `${pos}%`, clipPath: `inset(0 ${100 - pos}% 0 0)` }}
        >
          <img 
            src={heatmapUrl} 
            alt="Heatmap overlay" 
            className="w-full h-full object-contain"
            onError={handleImageError}
          />
        </div>
      </div>
      
      {/* Slider Control */}
      <div className="absolute inset-x-0 bottom-0 p-4 bg-gradient-to-t from-black/60 via-black/40 to-transparent">
        <div className="flex items-center gap-3 text-white text-xs mb-2">
          <span className="opacity-80">Original</span>
          <span className="flex-1 text-center font-semibold">Slide to compare</span>
          <span className="opacity-80">Heatmap</span>
        </div>
        <input 
          type="range" 
          min={0} 
          max={100} 
          value={pos} 
          onChange={e => setPos(Number(e.target.value))} 
          className="w-full h-2 bg-white/20 rounded-lg appearance-none cursor-pointer accent-primary"
          style={{
            background: `linear-gradient(to right, #3AAFA9 0%, #3AAFA9 ${pos}%, rgba(255,255,255,0.3) ${pos}%, rgba(255,255,255,0.3) 100%)`
          }}
        />
      </div>
    </div>
  )
}


