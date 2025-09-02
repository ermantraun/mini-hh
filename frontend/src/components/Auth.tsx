import { useState } from 'react'
import { login, register } from '../api'

type Props = { onSuccess: (token: string) => void }

export default function Auth({ onSuccess }: Props) {
  const [mode, setMode] = useState<'login' | 'register'>('login')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      setLoading(true)
      setError(null)
      if (mode === 'register') {
        await register(email, password)
      }
      const resp = await login(email, password)
      onSuccess(resp.access_token)
    } catch (e: any) {
      setError(e.message || 'Ошибка авторизации')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card">
      <div style={{ display: 'flex', gap: 8, marginBottom: 8 }}>
        <button className="btn" onClick={() => setMode('login')} disabled={mode === 'login'}>Вход</button>
        <button className="btn" onClick={() => setMode('register')} disabled={mode === 'register'}>Регистрация</button>
      </div>
      <form onSubmit={onSubmit} style={{ display: 'grid', gap: 8 }}>
        <input className="input" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
        <input className="input" type="password" placeholder="Пароль" value={password} onChange={e => setPassword(e.target.value)} />
        {error && <div className="error">Ошибка: {error}</div>}
        <button className="btn" disabled={loading}>{loading ? '...' : (mode === 'login' ? 'Войти' : 'Зарегистрироваться и войти')}</button>
      </form>
    </div>
  )
}
