import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import Home from '../pages/Home'

describe('Home Page', () => {
  it('renders Home hero heading and buttons', () => {
    render(
      <MemoryRouter>
        <Home />
      </MemoryRouter>
    )
    expect(
      screen.getByText(/AI-Powered Skin Disease Detection/i)
    ).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /Upload Your Image/i })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /Admin Dashboard/i })).toBeInTheDocument()
  })

  it('renders feature cards', () => {
    render(
      <MemoryRouter>
        <Home />
      </MemoryRouter>
    )
    
    expect(screen.getByText(/Why Choose SkinVision AI/i)).toBeInTheDocument()
    expect(screen.getByText(/AI-Powered Diagnosis/i)).toBeInTheDocument()
    expect(screen.getByText(/Dermatologist-Assisted Insights/i)).toBeInTheDocument()
  })

  it('renders trust badges', () => {
    render(
      <MemoryRouter>
        <Home />
      </MemoryRouter>
    )
    
    expect(screen.getByText(/100% Private/i)).toBeInTheDocument()
    expect(screen.getByText(/Mobile-Friendly/i)).toBeInTheDocument()
  })
})


