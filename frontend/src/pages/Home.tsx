import { useEffect, useMemo, useState } from 'react'
import VacancyCard from '../components/VacancyCard'
import ResumeForm from '../components/ResumeForm'
import Improvements from '../components/Improvements'
import { listResumes, createResume, updateResume, deleteResume } from '../api'

type Props = { token: string }

type Vacancy = {
  id: number
  title: string
  company: string
  location: string
  salary?: string
  content?: string
}

export default function Home({ token }: Props) {
  const [q, setQ] = useState('')
  const [itemsRaw, setItemsRaw] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showCreate, setShowCreate] = useState(false)
  const [editId, setEditId] = useState<number | null>(null)
  const [showImprFor, setShowImprFor] = useState<number | null>(null)

  async function load() {
    try {
      setLoading(true)
      setError(null)
      const data = await listResumes(token)
      setItemsRaw(data.items || [])
    } catch (e: any) {
      setError(e.message || 'Ошибка загрузки')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token])

  const items: Vacancy[] = useMemo(() => {
    const mapped: Vacancy[] = (itemsRaw || []).map((r: any) => ({
      id: r.id, title: r.title, content: r.content,
      company: '—', location: '—'
    }))
    const s = q.trim().toLowerCase()
    if (!s) return mapped
    return mapped.filter(v =>
      [v.title, v.company, v.location, v.content || ''].some(x => x.toLowerCase().includes(s))
    )
  }, [q, itemsRaw])

  const startEdit = (id: number) => setEditId(id)
  const stopEdit = () => setEditId(null)

  const onCreate = async (title: string, content: string) => {
    await createResume(token, title, content)
    setShowCreate(false)
    await load()
  }
  const onUpdate = async (id: number, title: string, content: string) => {
    await updateResume(token, id, title, content)
    stopEdit()
    await load()
  }
  const onDelete = async (id: number) => {
    if (!confirm('Удалить резюме?')) return
    await deleteResume(token, id)
    await load()
  }

  return (
    <section>
      <div className="searchbar">
        <input
          value={q}
          onChange={e => setQ(e.target.value)}
          className="input"
          placeholder="Поиск по названию/тексту…"
        />
        <button className="btn" onClick={() => setQ('')}>Сброс</button>
        <button className="btn" onClick={() => setShowCreate(true)}>Новое резюме</button>
      </div>

      {loading && <div className="loading">Загрузка...</div>}
      {error && <div className="error">Ошибка: {error}</div>}

      <div className="grid">
        {items.map(v => (
          <div key={v.id} className="card">
            <h3 className="card__title">{v.title}</h3>
            <div className="card__meta">
              <span>ID: {v.id}</span>
              <span>•</span>
              <span>Создано для пользователя</span>
            </div>
            <div style={{ whiteSpace: 'pre-wrap', color: '#cbd5e1' }}>
              {v.content}
            </div>
            <div style={{ display: 'flex', gap: 8, marginTop: 8, flexWrap: 'wrap' }}>
              <button className="btn" onClick={() => setShowImprFor(v.id)}>История/Улучшить</button>
              <button className="btn" onClick={() => startEdit(v.id)}>Редактировать</button>
              <button className="btn" onClick={() => onDelete(v.id)}>Удалить</button>
            </div>
            {editId === v.id && (
              <div style={{ marginTop: 12 }}>
                <ResumeForm
                  initialTitle={v.title}
                  initialContent={v.content || ''}
                  onSubmit={(t, c) => onUpdate(v.id, t, c)}
                  onCancel={stopEdit}
                  submitLabel="Сохранить"
                />
              </div>
            )}
          </div>
        ))}
      </div>

      {items.length === 0 && !loading && !error && <div className="empty">Резюме отсутствуют</div>}

      {showCreate && (
        <div className="card" style={{ marginTop: 16 }}>
          <h3 className="card__title">Новое резюме</h3>
          <ResumeForm
            onSubmit={(t, c) => onCreate(t, c)}
            onCancel={() => setShowCreate(false)}
            submitLabel="Создать"
          />
        </div>
      )}

      {showImprFor !== null && (
        <div className="card" style={{ marginTop: 16 }}>
          <Improvements token={token} resumeId={showImprFor} onClose={() => setShowImprFor(null)} />
        </div>
      )}
    </section>
  )
}
