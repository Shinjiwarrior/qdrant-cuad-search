import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { useState, useEffect } from 'react'
import NavigationHeader from './shared/components/layout/NavigationHeader'
import ErrorBoundary from './shared/components/ui/ErrorBoundary'
import LandingPage from './features/marketing/pages/LandingPage'
import SearchWorkspace from './features/legal-search/pages/SearchWorkspace'
import LegalCaseDetails from './features/case-library/pages/LegalCaseDetails'

function App() {
  const [isDarkMode, setIsDarkMode] = useState(() => {
    return localStorage.getItem('darkMode') === 'true'
  })

  useEffect(() => {
    localStorage.setItem('darkMode', isDarkMode.toString())
    if (isDarkMode) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [isDarkMode])

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode)
  }

  return (
    <Router>
      <ErrorBoundary>
        <div className="min-h-screen bg-background text-foreground">
          <NavigationHeader 
            isDarkMode={isDarkMode}
            onToggleDarkMode={toggleDarkMode}
          />
          
          <main>
            <Routes>
              <Route path="/" element={<LandingPage />} />
              <Route path="/search" element={<SearchWorkspace />} />
              <Route path="/case/:id" element={<LegalCaseDetails />} />
            </Routes>
          </main>
        </div>
      </ErrorBoundary>
    </Router>
  )
}

export default App 