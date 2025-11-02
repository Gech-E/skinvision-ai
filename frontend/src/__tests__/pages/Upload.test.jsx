import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { vi } from 'vitest'
import Upload from '../../pages/Upload'
import axios from 'axios'

vi.mock('axios')

describe('Upload Page', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    localStorage.clear()
  })

  it('renders upload page elements', () => {
    render(
      <BrowserRouter>
        <Upload />
      </BrowserRouter>
    )
    
    expect(screen.getByText(/Upload Your Skin Image/i)).toBeInTheDocument()
    expect(screen.getByText(/Drag & Drop your image/i)).toBeInTheDocument()
  })

  it('handles file selection and shows preview', () => {
    render(
      <BrowserRouter>
        <Upload />
      </BrowserRouter>
    )
    
    const file = new File(['test'], 'test.png', { type: 'image/png' })
    const input = document.querySelector('input[type="file"]')
    
    fireEvent.change(input, { target: { files: [file] } })
    
    // Should show preview
    waitFor(() => {
      expect(screen.getByAltText('preview')).toBeInTheDocument()
    })
  })

  it('disables analyze button when no file is selected', () => {
    render(
      <BrowserRouter>
        <Upload />
      </BrowserRouter>
    )
    
    const analyzeBtn = screen.getByText(/Analyze Image/i).closest('button')
    expect(analyzeBtn).toBeDisabled()
  })

  it('enables analyze button when file is selected', () => {
    render(
      <BrowserRouter>
        <Upload />
      </BrowserRouter>
    )
    
    const file = new File(['test'], 'test.png', { type: 'image/png' })
    const input = document.querySelector('input[type="file"]')
    fireEvent.change(input, { target: { files: [file] } })
    
    waitFor(() => {
      const analyzeBtn = screen.getByText(/Analyze Image/i).closest('button')
      expect(analyzeBtn).not.toBeDisabled()
    })
  })

  it('shows loading state during analysis', async () => {
    axios.post.mockResolvedValueOnce({
      data: {
        id: 1,
        predicted_class: 'Melanoma',
        confidence: 0.92,
        image_url: '/static/test.jpg',
        heatmap_url: '/static/heatmap.jpg'
      }
    })

    render(
      <BrowserRouter>
        <Upload />
      </BrowserRouter>
    )
    
    const file = new File(['test'], 'test.png', { type: 'image/png' })
    const input = document.querySelector('input[type="file"]')
    fireEvent.change(input, { target: { files: [file] } })
    
    await waitFor(() => {
      const analyzeBtn = screen.getByText(/Analyze Image/i).closest('button')
      expect(analyzeBtn).not.toBeDisabled()
    })
    
    fireEvent.click(screen.getByText(/Analyze Image/i))
    
    expect(screen.getByText(/Analyzing.../i)).toBeInTheDocument()
  })

  it('calls predict API on analyze', async () => {
    const mockResponse = {
      id: 1,
      predicted_class: 'Melanoma',
      confidence: 0.92,
      image_url: '/static/test.jpg',
      heatmap_url: '/static/heatmap.jpg'
    }
    
    axios.post.mockResolvedValueOnce({ data: mockResponse })

    render(
      <BrowserRouter>
        <Upload />
      </BrowserRouter>
    )
    
    const file = new File(['test'], 'test.png', { type: 'image/png' })
    const input = document.querySelector('input[type="file"]')
    fireEvent.change(input, { target: { files: [file] } })
    
    await waitFor(() => {
      fireEvent.click(screen.getByText(/Analyze Image/i))
    })
    
    await waitFor(() => {
      expect(axios.post).toHaveBeenCalledWith(
        expect.stringContaining('/predict'),
        expect.any(FormData),
        expect.any(Object)
      )
    })
  })
})
