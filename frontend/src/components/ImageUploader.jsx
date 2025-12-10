import { useCallback } from 'react'

export default function ImageUploader({ onSelect, previewUrl, disabled, error }) {
  const handleFileChange = useCallback(
    (event) => {
      const file = event.target.files?.[0]
      if (file) {
        onSelect(file)
      }
    },
    [onSelect]
  )

  return (
    <div className="space-y-4">
      <label
        htmlFor="image-upload"
        className={`relative flex flex-col items-center justify-center rounded-2xl border-2 border-dashed px-6 py-12 text-center transition-colors ${
          disabled ? 'bg-slate-100 text-slate-400' : 'cursor-pointer border-slate-300 hover:border-indigo-500'
        }`}
      >
        <input
          id="image-upload"
          type="file"
          accept="image/*"
          className="absolute inset-0 h-full w-full cursor-pointer opacity-0"
          onChange={handleFileChange}
          disabled={disabled}
        />
        <span className="text-lg font-semibold text-slate-700">Drop a dermatoscopic image or click to browse</span>
        <span className="mt-2 text-sm text-slate-500">Supported formats: JPG, PNG, HEIC (converted client-side)</span>
      </label>
      {error && <p className="text-sm text-red-600">{error}</p>}
      {previewUrl && (
        <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
          <img src={previewUrl} alt="Selected lesion preview" className="h-80 w-full object-cover" />
        </div>
      )}
    </div>
  )
}
