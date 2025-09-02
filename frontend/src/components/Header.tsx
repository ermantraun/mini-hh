type Props = {
  authed?: boolean
  onLogout?: () => void
}

export default function Header({ authed, onLogout }: Props) {
  return (
    <header className="header">
      <div className="container header__inner">
        <div className="logo">mini-hh</div>
        <nav className="nav">
          <a href="#" className="nav__link">Главная</a>
          {!authed ? (
            <span className="nav__link" style={{ opacity: 0.7 }}>Гость</span>
          ) : (
            <button className="btn" onClick={onLogout}>Выйти</button>
          )}
        </nav>
      </div>
    </header>
  )
}
