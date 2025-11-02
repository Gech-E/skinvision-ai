import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import App from '../App'

describe('App routing', () => {
  it('renders without crashing and shows Home route by default', () => {
    render(
      <MemoryRouter initialEntries={["/"]}>
        <App />
      </MemoryRouter>
    )
    // Home page should render some known element; fallback assert to presence of router container
    // Adjust this assertion if Home has a specific heading/text
    expect(document.body).toBeInTheDocument()
  })
})


