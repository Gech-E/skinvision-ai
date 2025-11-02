import { render, screen } from '@testing-library/react'
import PredictionCard from '../../components/PredictionCard'

describe('PredictionCard', () => {
  it('renders disease name and confidence', () => {
    render(<PredictionCard disease="Melanoma" confidence={0.92} />)
    
    expect(screen.getByText('Melanoma')).toBeInTheDocument()
    expect(screen.getByText(/92%/)).toBeInTheDocument()
  })

  it('displays confidence percentage correctly', () => {
    render(<PredictionCard disease="Nevus" confidence={0.75} />)
    
    expect(screen.getByText(/75%/)).toBeInTheDocument()
  })

  it('shows appropriate confidence message for high confidence', () => {
    render(<PredictionCard disease="BCC" confidence={0.85} />)
    
    expect(screen.getByText(/High confidence/i)).toBeInTheDocument()
  })

  it('shows appropriate confidence message for medium confidence', () => {
    render(<PredictionCard disease="AK" confidence={0.65} />)
    
    expect(screen.getByText(/Moderate confidence/i)).toBeInTheDocument()
  })

  it('handles missing confidence gracefully', () => {
    render(<PredictionCard disease="Benign" />)
    
    expect(screen.getByText('Benign')).toBeInTheDocument()
  })
})
