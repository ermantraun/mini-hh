import { useEffect, useState } from 'react'
import Header from './components/Header'
import Home from './pages/Home'
import Auth from './components/Auth'

export default function App() {
  const [token, setToken] = useState<string | null>(null)

  useEffect(() => {
    const t = localStorage.getItem('token')
    if (t) setToken(t)
  }, [])

  const handleLogin = (t: string) => {
    localStorage.setItem('token', t)
    setToken(t)
  }
  const handleLogout = () => {
    localStorage.removeItem('token')
    setToken(null)
  }

  return (
    <div className="app">
      <Header authed={!!token} onLogout={handleLogout} />
      <main className="container">
        {!token ? (
          <Auth onSuccess={handleLogin} />
        ) : (
          <Home token={token} />
        )}
      </main>
    </div>
  )
}
