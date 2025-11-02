import { render, screen, fireEvent } from '@testing-library/react'
import { vi } from 'vitest'
import HistoryTable from '../../components/HistoryTable'

const mockRows = [
  {
    id: 1,
    timestamp: '2024-01-15T10:30:00Z',
    image_url: '/static/test1.jpg',
    predicted_class: 'Melanoma',
    confidence: 0.92
  },
  {
    id: 2,
    timestamp: '2024-01-14T09:20:00Z',
    image_url: '/static/test2.jpg',
    predicted_class: 'Nevus',
    confidence: 0.78
  }
]

describe('HistoryTable', () => {
  it('renders table with headers', () => {
    render(<HistoryTable rows={mockRows} />)
    
    expect(screen.getByText('Time')).toBeInTheDocument()
    expect(screen.getByText('Image')).toBeInTheDocument()
    expect(screen.getByText('Class')).toBeInTheDocument()
    expect(screen.getByText('Confidence')).toBeInTheDocument()
    expect(screen.getByText('Action')).toBeInTheDocument()
  })

  it('renders all rows', () => {
    render(<HistoryTable rows={mockRows} />)
    
    expect(screen.getByText('Melanoma')).toBeInTheDocument()
    expect(screen.getByText('Nevus')).toBeInTheDocument()
    expect(screen.getByText(/92%/)).toBeInTheDocument()
    expect(screen.getByText(/78%/)).toBeInTheDocument()
  })

  it('calls onDelete when delete button is clicked', () => {
    const mockOnDelete = vi.fn()
    render(<HistoryTable rows={mockRows} onDelete={mockOnDelete} />)
    
    const deleteButtons = screen.getAllByText('Delete')
    fireEvent.click(deleteButtons[0])
    
    expect(mockOnDelete).toHaveBeenCalledWith(1)
  })

  it('handles empty rows', () => {
    render(<HistoryTable rows={[]} />)
    
    // Table should still render with headers
    expect(screen.getByText('Time')).toBeInTheDocument()
  })

  it('formats timestamps correctly', () => {
    render(<HistoryTable rows={mockRows} />)
    
    // Check that timestamps are rendered (format may vary)
    const cells = screen.getAllByText(/2024/i)
    expect(cells.length).toBeGreaterThan(0)
  })

  it('displays confidence as percentage', () => {
    render(<HistoryTable rows={mockRows} />)
    
    expect(screen.getByText(/92%/)).toBeInTheDocument()
    expect(screen.getByText(/78%/)).toBeInTheDocument()
  })
})
