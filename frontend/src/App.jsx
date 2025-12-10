import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import DashboardPage from './pages/Dashboard'
import HistoryPage from './pages/History'

function Navigation() {
  const linkClass = ({ isActive }) =>
    `px-4 py-2 rounded-full text-sm font-semibold transition-colors ${
      isActive ? 'bg-indigo-600 text-white' : 'bg-white/40 text-slate-700 hover:bg-white'
    }`

  return (
    <header className="bg-white shadow-sm">
      <div className="max-w-6xl mx-auto flex flex-wrap items-center justify-between gap-4 px-4 py-4">
        <h1 className="text-2xl font-bold text-slate-800">SkinVision AI</h1>
        <nav className="flex items-center gap-2">
          <NavLink to="/" className={linkClass} end>
            Dashboard
          </NavLink>
          <NavLink to="/history" className={linkClass}>
            History
          </NavLink>
        </nav>
      </div>
    </header>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-slate-50 text-slate-900">
        <Navigation />
        <main className="max-w-6xl mx-auto px-4 py-10">
          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/history" element={<HistoryPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}
