import React from 'react'

export default function UploadCard({ onFiles, previewUrl }) {
  const inputRef = React.useRef(null)
  const [isOver, setIsOver] = React.useState(false)

  const open = () => inputRef.current?.click()

  function handleFiles(files) {
    if (!files?.length) return
    onFiles(files)
  }

  return (
    <div>
      <input ref={inputRef} type="file" accept="image/*" className="hidden" onChange={e => handleFiles(e.target.files)} />
      <div
        onDragOver={e => { e.preventDefault(); setIsOver(true) }}
        onDragLeave={() => setIsOver(false)}
        onDrop={e => { e.preventDefault(); setIsOver(false); handleFiles(e.dataTransfer.files) }}
        onClick={open}
        className={[
          'relative flex flex-col items-center justify-center h-64 rounded-2xl border-2 border-dashed cursor-pointer transition-all',
          isOver ? 'border-primary bg-background' : 'border-secondary hover:bg-background'
        ].join(' ')}
      >
        <div className="text-center px-6">
          <div className="text-3xl mb-2"></div>
          <p className="text-text font-medium">Drag & Drop your image</p>
          <p className="text-sm text-text/70">or click to choose a file</p>
        </div>
      </div>
      {previewUrl && (
        <div className="mt-4">
          <p className="text-sm text-text/70 mb-2">Preview</p>
          <img src={previewUrl} alt="preview" className="rounded-2xl max-h-72 object-contain border border-secondary" />
        </div>
      )}
    </div>
  )
}


