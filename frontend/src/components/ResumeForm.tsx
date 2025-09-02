import { useState } from 'react'

type Props = {
  initialTitle?: string
  initialContent?: string
  submitLabel?: string
  onSubmit: (title: string, content: string) => void | Promise<void>
  onCancel?: () => void
}

export default function ResumeForm({ initialTitle = '', initialContent = '', submitLabel = 'Сохранить', onSubmit, onCancel }: Props) {
  const [title, setTitle] = useState(initialTitle)
  const [content, setContent] = useState(initialContent)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      setLoading(true)
      setError(null)
      await onSubmit(title, content)
    } catch (e: any) {
      setError(e.message || 'Ошибка')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={submit} style={{ display: 'grid', gap: 8 }}>
      <input className="input" placeholder="Заголовок" value={title} onChange={e => setTitle(e.target.value)} />
      <textarea className="input" placeholder="Содержимое" value={content} onChange={e => setContent(e.target.value)} rows={6} />
      {error && <div className="error">Ошибка: {error}</div>}
      <div style={{ display: 'flex', gap: 8 }}>
        <button className="btn" disabled={loading}>{loading ? '...' : submitLabel}</button>
        {onCancel && <button type="button" className="btn" onClick={onCancel}>Отмена</button>}
      </div>
    </form>
  )
}
