/**
 * Integration tests for complete user flows
 */
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { BrowserRouter, MemoryRouter } from 'react-router-dom'
import { vi } from 'vitest'
import App from '../../App'
import axios from 'axios'

vi.mock('axios')

describe('User Flow Integration Tests', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    localStorage.clear()
    sessionStorage.clear()
  })

  describe('Upload to Result Flow', () => {
    it('completes full upload → analyze → result flow', async () => {
      const mockResult = {
        id: 1,
        predicted_class: 'Melanoma',
        confidence: 0.92,
        image_url: '/static/test.jpg',
        heatmap_url: '/static/heatmap.jpg'
      }

      axios.post.mockResolvedValueOnce({ data: mockResult })

      render(
        <MemoryRouter initialEntries={['/upload']}>
          <App />
        </MemoryRouter>
      )

      // Upload file
      const file = new File(['test'], 'test.png', { type: 'image/png' })
      const input = document.querySelector('input[type="file"]')
      fireEvent.change(input, { target: { files: [file] } })

      await waitFor(() => {
        const analyzeBtn = screen.getByText(/Analyze Image/i).closest('button')
        expect(analyzeBtn).not.toBeDisabled()
      })

      // Click analyze
      fireEvent.click(screen.getByText(/Analyze Image/i))

      // Should navigate to result page
      await waitFor(() => {
        expect(screen.getByText('Melanoma')).toBeInTheDocument()
      }, { timeout: 3000 })
    })
  })

  describe('Authentication Flow', () => {
    it('completes signup → login → dashboard flow', async () => {
      // Mock API responses
      axios.post
        .mockResolvedValueOnce({ // Signup
          data: { id: 1, email: 'test@example.com', role: 'admin' }
        })
        .mockResolvedValueOnce({ // Login
          data: { access_token: 'mock-token', token_type: 'bearer' }
        })

      axios.get.mockResolvedValueOnce({ // History
        data: []
      })

      render(
        <MemoryRouter initialEntries={['/signup']}>
          <App />
        </MemoryRouter>
      )

      // Signup
      const emailInput = screen.getByPlaceholderText(/you@example.com/i)
      const passwordInput = screen.getByLabelText(/Password/i)
      const signupBtn = screen.getByText(/Sign Up/i)

      fireEvent.change(emailInput, { target: { value: 'test@example.com' } })
      fireEvent.change(passwordInput, { target: { value: 'password123' } })
      fireEvent.click(signupBtn)

      // Should navigate to login
      await waitFor(() => {
        expect(screen.getByText(/Login/i)).toBeInTheDocument()
      })

      // Login
      const loginEmail = screen.getByPlaceholderText(/you@example.com/i)
      const loginPassword = screen.getByLabelText(/Password/i)
      const loginBtn = screen.getByText(/Sign In/i)

      fireEvent.change(loginEmail, { target: { value: 'test@example.com' } })
      fireEvent.change(loginPassword, { target: { value: 'password123' } })
      fireEvent.click(loginBtn)

      // Should navigate to admin dashboard
      await waitFor(() => {
        expect(screen.getByText(/Admin Dashboard/i)).toBeInTheDocument()
      })
    })
  })

  describe('Navigation Flow', () => {
    it('navigates between pages correctly', () => {
      render(
        <BrowserRouter>
          <App />
        </BrowserRouter>
      )

      // Start at home
      expect(screen.getByText(/AI-Powered Skin Disease Detection/i)).toBeInTheDocument()

      // Navigate to upload
      const uploadLink = screen.getByText(/Upload Your Image/i)
      fireEvent.click(uploadLink)

      // Should show upload page
      expect(screen.getByText(/Upload Your Skin Image/i)).toBeInTheDocument()
    })
  })
})
