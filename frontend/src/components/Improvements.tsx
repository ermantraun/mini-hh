import { useEffect, useState } from 'react'
import { improveResume, listImprovements } from '../api'

type Props = {
  token: string
  resumeId: number
  onClose?: () => void
}

export default function Improvements({ token, resumeId, onClose }: Props) {
  const [items, setItems] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [improving, setImproving] = useState(false)

  async function load() {
    try {
      setLoading(true)
      setError(null)
      const data = await listImprovements(token, resumeId)
      setItems(data.items || [])
    } catch (e: any) {
      setError(e.message || 'Ошибка загрузки')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [resumeId])

  const doImprove = async () => {
    try {
      setImproving(true)
      await improveResume(token, resumeId)
      await load()
    } catch (e: any) {
      setError(e.message || 'Ошибка улучшения')
    } finally {
      setImproving(false)
    }
  }

  return (
    <div>
      <div style={{ display: 'flex', gap: 8, alignItems: 'center', marginBottom: 8 }}>
        <h3 className="card__title" style={{ margin: 0 }}>Улучшения резюме #{resumeId}</h3>
        <button className="btn" onClick={doImprove} disabled={improving}>{improving ? '...' : 'Улучшить'}</button>
        {onClose && <button className="btn" onClick={onClose}>Закрыть</button>}
      </div>
      {loading && <div className="loading">Загрузка...</div>}
      {error && <div className="error">Ошибка: {error}</div>}
      {items.length === 0 && !loading && <div className="empty">Нет улучшений</div>}
      <div style={{ display: 'grid', gap: 8 }}>
        {items.map(x => (
          <div key={x.id} className="card">
            <div className="card__meta" style={{ marginBottom: 8 }}>
              <span>ID: {x.id}</span>
              <span>•</span>
              <span>{new Date(x.created_at).toLocaleString()}</span>
            </div>
            <div style={{ display: 'grid', gap: 8 }}>
              <div>
                <div style={{ color: '#9aa1ad', marginBottom: 4 }}>Исходный текст</div>
                <div style={{ whiteSpace: 'pre-wrap' }}>{x.original_content}</div>
              </div>
              <div>
                <div style={{ color: '#9aa1ad', marginBottom: 4 }}>Улучшенный текст</div>
                <div style={{ whiteSpace: 'pre-wrap' }}>{x.improved_content}</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
