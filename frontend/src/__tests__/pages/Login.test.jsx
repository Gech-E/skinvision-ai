import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { vi } from 'vitest'
import Login from '../../pages/Login'
import axios from 'axios'

vi.mock('axios')

describe('Login Page', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    localStorage.clear()
  })

  it('renders login form', () => {
    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    )
    
    expect(screen.getByText(/Login/i)).toBeInTheDocument()
    expect(screen.getByPlaceholderText(/you@example.com/i)).toBeInTheDocument()
  })

  it('handles form submission', async () => {
    axios.post.mockResolvedValueOnce({
      data: { access_token: 'mock-token', token_type: 'bearer' }
    })

    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    )
    
    const emailInput = screen.getByPlaceholderText(/you@example.com/i)
    const passwordInput = screen.getByPlaceholderText(/password/i) || 
                          screen.getByLabelText(/password/i)
    const submitButton = screen.getByText(/Sign In/i)
    
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } })
    fireEvent.change(passwordInput, { target: { value: 'password123' } })
    fireEvent.click(submitButton)
    
    await waitFor(() => {
      expect(axios.post).toHaveBeenCalledWith(
        expect.stringContaining('/auth/login'),
        expect.objectContaining({
          email: 'test@example.com',
          password: 'password123'
        })
      )
    })
  })

  it('displays error on login failure', async () => {
    axios.post.mockRejectedValueOnce({
      response: { status: 401 }
    })

    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    )
    
    const submitButton = screen.getByText(/Sign In/i)
    fireEvent.click(submitButton)
    
    await waitFor(() => {
      expect(screen.getByText(/Invalid credentials/i)).toBeInTheDocument()
    })
  })
})
