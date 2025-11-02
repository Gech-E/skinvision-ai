import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { vi } from 'vitest'
import UploadCard from '../../components/UploadCard'

describe('UploadCard', () => {
  it('renders drag and drop zone', () => {
    render(<UploadCard onFiles={() => {}} />)
    expect(screen.getByText(/Drag & Drop your image/i)).toBeInTheDocument()
  })

  it('calls onFiles when file is selected', () => {
    const mockOnFiles = vi.fn()
    const { container } = render(<UploadCard onFiles={mockOnFiles} />)
    
    const input = container.querySelector('input[type="file"]')
    const file = new File(['test'], 'test.png', { type: 'image/png' })
    
    fireEvent.change(input, { target: { files: [file] } })
    
    expect(mockOnFiles).toHaveBeenCalledWith([file])
  })

  it('handles drag and drop', () => {
    const mockOnFiles = vi.fn()
    render(<UploadCard onFiles={mockOnFiles} />)
    
    const dropZone = screen.getByText(/Drag & Drop your image/i).closest('div')
    const file = new File(['test'], 'test.png', { type: 'image/png' })
    
    fireEvent.dragOver(dropZone)
    fireEvent.drop(dropZone, { dataTransfer: { files: [file] } })
    
    expect(mockOnFiles).toHaveBeenCalledWith([file])
  })

  it('shows preview when previewUrl is provided', () => {
    const previewUrl = 'data:image/png;base64,test'
    render(<UploadCard onFiles={() => {}} previewUrl={previewUrl} />)
    
    const img = screen.getByAltText('preview')
    expect(img).toBeInTheDocument()
    expect(img.src).toContain('data:image')
  })

  it('highlights on drag over', () => {
    render(<UploadCard onFiles={() => {}} />)
    const dropZone = screen.getByText(/Drag & Drop your image/i).closest('div')
    
    fireEvent.dragOver(dropZone)
    expect(dropZone).toHaveClass('border-primary')
  })
})
