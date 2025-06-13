import React, { ReactElement } from 'react'
import { render, RenderOptions } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'

// Custom render function that includes Router
const AllTheProviders = ({ children }: { children: React.ReactNode }) => {
  return (
    <BrowserRouter>
      {children}
    </BrowserRouter>
  )
}

const customRender = (
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>,
) => render(ui, { wrapper: AllTheProviders, ...options })

export * from '@testing-library/react'
export { customRender as render }

// Helper functions for testing
export const mockLocalStorage = () => {
  const localStorageMock = {
    getItem: vi.fn(),
    setItem: vi.fn(),
    removeItem: vi.fn(),
    clear: vi.fn(),
  }
  
  Object.defineProperty(window, 'localStorage', {
    value: localStorageMock,
    writable: true,
  })
  
  return localStorageMock
}

export const mockMatchMedia = (matches = false) => {
  Object.defineProperty(window, 'matchMedia', {
    writable: true,
    value: vi.fn().mockImplementation(query => ({
      matches,
      media: query,
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    })),
  })
}

// Mock data helpers
export const createMockSearchResult = (overrides = {}) => ({
  id: 'test-case-1',
  title: 'Test Legal Case',
  content: 'This is test content for a legal case...',
  score: 0.95,
  metadata: {
    jurisdiction: 'California',
    court_level: 'Superior Court',
    case_type: 'Contract Dispute',
    date: '2023-01-15',
    industry: 'Technology'
  },
  ...overrides
})

export const createMockLegalCase = (overrides = {}) => ({
  id: 'test-case-detailed',
  title: 'Detailed Test Legal Case',
  content: 'Full detailed content for testing...',
  metadata: {
    jurisdiction: 'California',
    court_level: 'Superior Court',
    case_type: 'Contract Dispute',
    date: '2023-01-15',
    industry: 'Technology',
    company_size: 'Large',
    complexity_level: 'High',
    risk_level: 'Medium'
  },
  related_cases: ['case_1', 'case_2'],
  citations: ['Citation 1', 'Citation 2'],
  ...overrides
})

export const createMockFilterOptions = (overrides = {}) => ({
  jurisdictions: ['California', 'New York', 'Texas'],
  court_levels: ['Superior Court', 'Appeals Court', 'Supreme Court'],
  case_types: ['Contract Dispute', 'Intellectual Property', 'Employment'],
  industries: ['Technology', 'Healthcare', 'Finance'],
  company_sizes: ['Small', 'Medium', 'Large'],
  contract_statuses: ['Active', 'Expired', 'Pending'],
  complexity_levels: ['Low', 'Medium', 'High'],
  risk_levels: ['Low', 'Medium', 'High'],
  renewal_terms: ['Annual', 'Quarterly', 'Monthly'],
  ...overrides
})

// Wait for async operations in tests
export const waitForLoadingToFinish = () =>
  new Promise(resolve => setTimeout(resolve, 0)) 