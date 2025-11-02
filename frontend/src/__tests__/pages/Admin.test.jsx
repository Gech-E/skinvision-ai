import { render, screen, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { vi } from 'vitest'
import Admin from '../../pages/Admin'
import axios from 'axios'

vi.mock('axios')

const mockHistoryData = [
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

describe('Admin Page', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    localStorage.setItem('token', 'mock-token')
  })

  it('renders admin dashboard', async () => {
    axios.get.mockResolvedValueOnce({ data: mockHistoryData })
    
    render(
      <BrowserRouter>
        <Admin />
      </BrowserRouter>
    )
    
    await waitFor(() => {
      expect(screen.getByText(/Admin Dashboard/i)).toBeInTheDocument()
    })
  })

  it('loads and displays prediction history', async () => {
    axios.get.mockResolvedValueOnce({ data: mockHistoryData })
    
    render(
      <BrowserRouter>
        <Admin />
      </BrowserRouter>
    )
    
    await waitFor(() => {
      expect(screen.getByText('Melanoma')).toBeInTheDocument()
      expect(screen.getByText('Nevus')).toBeInTheDocument()
    })
  })

  it('displays statistics cards', async () => {
    axios.get.mockResolvedValueOnce({ data: mockHistoryData })
    
    render(
      <BrowserRouter>
        <Admin />
      </BrowserRouter>
    )
    
    await waitFor(() => {
      expect(screen.getByText(/Total Predictions/i)).toBeInTheDocument()
      expect(screen.getByText(/Disease Classes/i)).toBeInTheDocument()
    })
  })

  it('handles delete action', async () => {
    axios.get.mockResolvedValueOnce({ data: mockHistoryData })
    axios.delete.mockResolvedValueOnce({ status: 200 })
    
    render(
      <BrowserRouter>
        <Admin />
      </BrowserRouter>
    )
    
    await waitFor(() => {
      const deleteButtons = screen.getAllByText('Delete')
      expect(deleteButtons.length).toBeGreaterThan(0)
    })
  })

  it('shows loading state', () => {
    axios.get.mockImplementation(() => new Promise(() => {})) // Never resolves
    
    render(
      <BrowserRouter>
        <Admin />
      </BrowserRouter>
    )
    
    expect(screen.getByText(/Loading dashboard/i)).toBeInTheDocument()
  })
})
