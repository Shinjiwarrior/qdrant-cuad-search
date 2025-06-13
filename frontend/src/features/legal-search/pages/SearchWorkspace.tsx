import { useState, useEffect, useRef, useCallback } from 'react'
import { Search, Filter, Clock, Scale, ExternalLink, ArrowLeft } from 'lucide-react'
import { searchCases, getFilterOptions, type LegalCase, type SearchRequest, type FilterOptions } from '../../../lib/api'
import { formatDate, truncateText, debounce } from '../../../lib/utils'
import LoadingSpinner from '../../../shared/components/ui/LoadingSpinner'
import QdrantAdvancedFilters from '../components/QdrantAdvancedFilters'
import LegalCaseCard from '../../case-library/components/LegalCaseCard'
import { Link } from 'react-router-dom'

export default function SearchWorkspace() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<LegalCase[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [totalResults, setTotalResults] = useState(0)
  const [processingTime, setProcessingTime] = useState(0)
  const [showFilters, setShowFilters] = useState(false)
  const [filterOptions, setFilterOptions] = useState<FilterOptions | null>(null)
  const [activeFilters, setActiveFilters] = useState<SearchRequest['filters']>({})

  // Refs for handling race conditions and cleanup
  const abortControllerRef = useRef<AbortController | null>(null)
  const searchIdRef = useRef(0)

  // Load filter options on mount
  useEffect(() => {
    const loadFilterOptions = async () => {
      try {
        const options = await getFilterOptions()
        setFilterOptions(options)
      } catch (error) {
        console.error('Failed to load filter options:', error)
      }
    }
    loadFilterOptions()
  }, [])

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort()
      }
    }
  }, [])

  // Search function with proper race condition handling
  const performSearch = useCallback(async (searchQuery: string, filters: SearchRequest['filters']) => {
    if (!searchQuery.trim()) {
      setResults([])
      setTotalResults(0)
      setError(null)
      return
    }

    // Cancel previous request if it exists
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
    }

    // Create new abort controller for this request
    abortControllerRef.current = new AbortController()
    const currentSearchId = ++searchIdRef.current

    console.log(`Starting search ${currentSearchId} for query: "${searchQuery}"`)
    setIsLoading(true)
    setError(null)

    try {
      const searchRequest: SearchRequest = {
        query: searchQuery,
        filters,
        limit: 20,
        offset: 0
      }

      const response = await searchCases(searchRequest, abortControllerRef.current.signal)
      
      // Only update state if this is still the most recent search
      if (currentSearchId === searchIdRef.current) {
        console.log(`Search ${currentSearchId} completed with ${response.results.length} results`)
        setResults(response.results)
        setTotalResults(response.total)
        setProcessingTime(response.processing_time)
      } else {
        console.log(`Search ${currentSearchId} cancelled (newer search ${searchIdRef.current} is active)`)
      }
    } catch (error: any) {
      // Only handle error if this is still the most recent search and not aborted
      if (error.name === 'AbortError') {
        console.log(`Search ${currentSearchId} was aborted`)
      } else if (currentSearchId === searchIdRef.current) {
        console.error(`Search ${currentSearchId} error:`, error)
        const errorMessage = error.response?.data?.detail || error.message || 'Search failed. Please try again.'
        setError(typeof errorMessage === 'string' ? errorMessage : 'An unexpected error occurred.')
        setResults([])
        setTotalResults(0)
      } else {
        console.log(`Search ${currentSearchId} error ignored (newer search ${searchIdRef.current} is active)`)
      }
    } finally {
      // Only update loading state if this is still the most recent search
      if (currentSearchId === searchIdRef.current) {
        setIsLoading(false)
      }
    }
  }, [])

  // Debounced search function
  const debouncedSearch = useCallback(
    debounce((searchQuery: string, filters: SearchRequest['filters']) => {
      performSearch(searchQuery, filters)
    }, 500),
    [performSearch]
  )

  // Handle search input change
  const handleQueryChange = (value: string) => {
    setQuery(value)
    debouncedSearch(value, activeFilters)
  }

  // Handle filter changes
  const handleFiltersChange = (filters: SearchRequest['filters']) => {
    setActiveFilters(filters)
    if (query.trim()) {
      debouncedSearch(query, filters)
    }
  }

  // Handle initial search
  const handleSearch = () => {
    if (query.trim()) {
      performSearch(query, activeFilters)
    }
  }

  const hasActiveFilters = Object.values(activeFilters).some(filter => 
    Array.isArray(filter) ? filter.length > 0 : Boolean(filter)
  )

  return (
    <div className="min-h-screen flex">
      {/* Left Sidebar - Search Controls */}
      <div className="bg-muted/30 border-r border-border p-6 min-h-screen" style={{width: '500px'}}>
        {/* Back Link */}
        <div className="mb-6">
          <Link 
            to="/" 
            className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors text-sm"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to home
          </Link>
        </div>

        <div className="space-y-6">
          {/* Search Bar */}
          <div className="bg-card border border-border rounded-lg p-4 shadow-sm">
            <div className="space-y-4">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <input
                  type="text"
                  placeholder="Search CUAD commercial contracts..."
                  value={query}
                  onChange={(e) => handleQueryChange(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                  className="w-full pl-10 pr-4 py-3 border border-input rounded-md bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent"
                />
              </div>
              
              <button
                onClick={() => setShowFilters(!showFilters)}
                className={`w-full px-4 py-2 border rounded-md transition-colors flex items-center justify-center gap-2 ${
                  showFilters || hasActiveFilters
                    ? 'bg-primary text-primary-foreground border-primary'
                    : 'bg-background border-input hover:bg-muted'
                }`}
              >
                <Filter className="h-4 w-4" />
                Contract Filters
                {hasActiveFilters && (
                  <span className="bg-primary-foreground text-primary text-xs rounded-full w-5 h-5 flex items-center justify-center">
                    !
                  </span>
                )}
              </button>

              {/* Search Filters */}
              {showFilters && filterOptions && (
                <div className="pt-4 border-t border-border">
                  <QdrantAdvancedFilters
                    options={filterOptions}
                    activeFilters={activeFilters}
                    onFiltersChange={handleFiltersChange}
                  />
                </div>
              )}
            </div>
          </div>

          {/* Search Examples */}
          <div className="bg-card border border-border rounded-lg p-4">
            <h3 className="font-semibold mb-3 text-sm">Try These Contract Examples</h3>
            <div className="space-y-1 text-sm">
              <button
                onClick={() => handleQueryChange('employment termination clause')}
                className="block w-full text-left px-2 py-1 rounded hover:bg-muted transition-colors text-muted-foreground hover:text-foreground"
              >
                Employment termination
              </button>
              <button
                onClick={() => handleQueryChange('intellectual property licensing terms')}
                className="block w-full text-left px-2 py-1 rounded hover:bg-muted transition-colors text-muted-foreground hover:text-foreground"
              >
                IP licensing terms
              </button>
              <button
                onClick={() => handleQueryChange('confidentiality obligations')}
                className="block w-full text-left px-2 py-1 rounded hover:bg-muted transition-colors text-muted-foreground hover:text-foreground"
              >
                Confidentiality obligations
              </button>
              <button
                onClick={() => handleQueryChange('indemnification clause')}
                className="block w-full text-left px-2 py-1 rounded hover:bg-muted transition-colors text-muted-foreground hover:text-foreground"
              >
                Indemnification clause
              </button>
              <button
                onClick={() => handleQueryChange('service level agreement')}
                className="block w-full text-left px-2 py-1 rounded hover:bg-muted transition-colors text-muted-foreground hover:text-foreground"
              >
                Service level agreements
              </button>
              <button
                onClick={() => handleQueryChange('payment terms net 30')}
                className="block w-full text-left px-2 py-1 rounded hover:bg-muted transition-colors text-muted-foreground hover:text-foreground"
              >
                Payment terms
              </button>
            </div>
          </div>

          {/* CUAD Features */}
          <div className="bg-card border border-border rounded-lg p-4">
            <h3 className="font-semibold mb-3 text-sm">CUAD Dataset Features</h3>
            <div className="space-y-2 text-xs text-muted-foreground">
              <p>📋 <strong>510 real contracts:</strong> Employment, licensing, supply agreements</p>
              <p>🏷️ <strong>13K+ labeled clauses:</strong> Expert-annotated contract provisions</p>
              <p>🔍 <strong>Semantic search:</strong> Find contracts by meaning, not just keywords</p>
              <p>🎯 <strong>ColBERT refinement:</strong> Precise multi-vector contract matching</p>
              <p>⚡ <strong>Coarse-to-fine:</strong> Fast candidate retrieval with accurate ranking</p>
            </div>
          </div>

          {/* CUAD Notice */}
          <div className="bg-primary/5 border border-primary/20 rounded-lg p-3 text-xs text-muted-foreground">
            <p>
              <strong className="text-primary">CUAD Contract Search:</strong> Powered by the Contract Understanding Atticus Dataset with Qdrant's coarse-to-fine pipeline and ColBERT refinement.
            </p>
          </div>
        </div>
      </div>

      {/* Right Side - Search Results */}
      <div className="flex-1 bg-background">
        {/* Hero Section */}
        <div className="text-center space-y-4 p-8 border-b border-border">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Scale className="h-8 w-8 text-primary" />
            <h1 className="text-3xl font-bold">CUAD Contract Search</h1>
          </div>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Search through 510 real commercial contracts from the premier CUAD dataset using Qdrant's coarse-to-fine pipeline with dense candidate fetching and ColBERT refinement for precise contract intelligence.
          </p>
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-primary/10 text-primary rounded-full text-sm font-medium">
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
            CUAD: 510 Contracts, 13K+ Clauses
          </div>
        </div>

        {/* Results Area */}
        <div className="p-6 min-h-[600px]">
          {isLoading && (
            <div className="flex items-center justify-center py-12">
              <LoadingSpinner size="lg" />
            </div>
          )}

          {error && (
            <div className="bg-destructive/10 border border-destructive/20 rounded-lg p-4 text-center">
              <p className="text-destructive">{error}</p>
            </div>
          )}

          {!isLoading && !error && query && (
            <div className="space-y-4">
              {/* Search Summary */}
              <div className="flex items-center justify-between text-sm text-muted-foreground border-b border-border pb-4">
                <div className="flex items-center gap-4">
                  <span>
                    <strong className="text-foreground">{totalResults}</strong> contracts for "{query}"
                  </span>
                  {processingTime > 0 && (
                    <div className="flex items-center gap-1">
                      <Clock className="h-3 w-3" />
                      <span>{processingTime.toFixed(2)}s</span>
                    </div>
                  )}
                </div>
                {hasActiveFilters && (
                  <button
                    onClick={() => handleFiltersChange({})}
                    className="text-primary hover:underline"
                  >
                    Clear filters
                  </button>
                )}
              </div>

              {/* Results */}
              {results.length > 0 ? (
                <div className="space-y-4">
                  {results.map((case_) => (
                    <LegalCaseCard key={case_.id} case={case_} searchQuery={query} />
                  ))}
                </div>
              ) : (
                <div className="text-center py-12">
                  <Scale className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                  <h3 className="text-lg font-medium mb-2">No contracts found</h3>
                  <p className="text-muted-foreground max-w-md mx-auto">
                    Try adjusting your search terms or removing some filters to find relevant contracts.
                  </p>
                </div>
              )}
            </div>
          )}

          {/* Welcome State */}
          {!query && !isLoading && (
            <div className="text-center py-12">
              <Scale className="h-16 w-16 text-muted-foreground mx-auto mb-6" />
              <h3 className="text-xl font-medium mb-4">Ready to search CUAD contracts</h3>
              <p className="text-muted-foreground mb-6 max-w-md mx-auto">
                Enter a search term or try one of the examples to find relevant commercial contract clauses from the CUAD dataset.
              </p>
              <div className="bg-muted/30 rounded-lg p-6 max-w-lg mx-auto">
                <h4 className="font-medium mb-2">💡 Contract Search Tips</h4>
                <ul className="text-sm text-muted-foreground space-y-1 text-left">
                  <li>• Use natural language - find contracts by meaning</li>
                  <li>• Search for specific clauses like "termination rights"</li>
                  <li>• Filter by contract type, industry, or company size</li>
                  <li>• Explore 510 real commercial agreements</li>
                  <li>• ColBERT ensures precise contract matching</li>
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
} 