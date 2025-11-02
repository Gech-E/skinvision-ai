import { render, screen, fireEvent } from '@testing-library/react'
import HeatmapSlider from '../../components/HeatmapSlider'

describe('HeatmapSlider', () => {
  const mockImageUrl = 'https://example.com/image.jpg'
  const mockHeatmapUrl = 'https://example.com/heatmap.jpg'

  it('renders slider with images', () => {
    render(<HeatmapSlider imageUrl={mockImageUrl} heatmapUrl={mockHeatmapUrl} />)
    
    const originalImg = screen.getByAltText('Original skin image')
    const heatmapImg = screen.getByAltText('Heatmap overlay')
    
    expect(originalImg).toBeInTheDocument()
    expect(heatmapImg).toBeInTheDocument()
    expect(screen.getByText(/Slide to compare/i)).toBeInTheDocument()
  })

  it('updates slider position on change', () => {
    render(<HeatmapSlider imageUrl={mockImageUrl} heatmapUrl={mockHeatmapUrl} />)
    
    const slider = screen.getByRole('slider')
    expect(slider).toHaveValue('50')
    
    fireEvent.change(slider, { target: { value: '75' } })
    expect(slider).toHaveValue('75')
  })

  it('shows fallback when images are missing', () => {
    render(<HeatmapSlider imageUrl={null} heatmapUrl={null} />)
    
    expect(screen.getByText(/Image not available/i)).toBeInTheDocument()
  })

  it('handles image load errors', () => {
    render(<HeatmapSlider imageUrl="invalid-url" heatmapUrl="invalid-url" />)
    
    const img = screen.getByAltText('Original skin image')
    fireEvent.error(img)
    
    // After error, should show fallback
    expect(screen.getByText(/Image not available/i)).toBeInTheDocument()
  })
})
