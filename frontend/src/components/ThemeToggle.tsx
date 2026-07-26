import { useTheme } from '../context/ThemeContext'
import { IconMoon, IconSun } from './icons/Icons'

export function ThemeToggle() {
  const { theme, toggleTheme } = useTheme()

  return (
    <button type="button" className="theme-toggle-btn" onClick={toggleTheme} title="Przełącz motyw jasny/ciemny">
      {theme === 'light' ? <IconMoon /> : <IconSun />}
    </button>
  )
}
