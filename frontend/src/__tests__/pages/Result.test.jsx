import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import Result from '../../pages/Result'

const mockResult = {
  id: 1,
  predicted_class: 'Melanoma',
  confidence: 0.92,
  image_url: '/static/test.jpg',
  heatmap_url: '/static/heatmap.jpg',
  timestamp: '2024-01-15T10:30:00Z'
}

describe('Result Page', () => {
  beforeEach(() => {
    sessionStorage.clear()
  })

  it('renders result data when available', () => {
    sessionStorage.setItem('predictionResult', JSON.stringify(mockResult))
    
    render(
      <MemoryRouter>
        <Result />
      </MemoryRouter>
    )
    
    expect(screen.getByText('Melanoma')).toBeInTheDocument()
    expect(screen.getByText(/92%/)).toBeInTheDocument()
  })

  it('shows recommendation section', () => {
    sessionStorage.setItem('predictionResult', JSON.stringify(mockResult))
    
    render(
      <MemoryRouter>
        <Result />
      </MemoryRouter>
    )
    
    expect(screen.getByText(/Recommendation/i)).toBeInTheDocument()
    expect(screen.getByText(/Urgency Level/i)).toBeInTheDocument()
  })

  it('displays severity badge based on confidence', () => {
    sessionStorage.setItem('predictionResult', JSON.stringify(mockResult))
    
    render(
      <MemoryRouter>
        <Result />
      </MemoryRouter>
    )
    
    // High confidence should show High severity
    expect(screen.getByText(/High/i)).toBeInTheDocument()
  })

  it('shows action buttons', () => {
    sessionStorage.setItem('predictionResult', JSON.stringify(mockResult))
    
    render(
      <MemoryRouter>
        <Result />
      </MemoryRouter>
    )
    
    expect(screen.getByText(/Download Report/i)).toBeInTheDocument()
    expect(screen.getByText(/Request Dermatologist Review/i)).toBeInTheDocument()
  })

  it('shows heatmap slider', () => {
    sessionStorage.setItem('predictionResult', JSON.stringify(mockResult))
    
    render(
      <MemoryRouter>
        <Result />
      </MemoryRouter>
    )
    
    expect(screen.getByText(/Grad-CAM Heatmap/i)).toBeInTheDocument()
  })
})
