type Props = {
  title: string
  company: string
  location: string
  salary?: string
  onOpen?: () => void
}

export default function VacancyCard({ title, company, location, salary, onOpen }: Props) {
  return (
    <article className="card" onClick={onOpen} role="button">
      <h3 className="card__title">{title}</h3>
      <div className="card__meta">
        <span>{company}</span>
        <span>•</span>
        <span>{location}</span>
        {salary ? (
          <>
            <span>•</span>
            <span className="salary">{salary}</span>
          </>
        ) : null}
      </div>
      <button className="btn">Подробнее</button>
    </article>
  )
}
