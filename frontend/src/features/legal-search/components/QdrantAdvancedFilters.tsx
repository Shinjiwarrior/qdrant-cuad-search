import { useState } from 'react'
import { X } from 'lucide-react'
import { FilterOptions, SearchRequest } from '../../../lib/api'
import { cn } from '../../../lib/utils'

interface QdrantAdvancedFiltersProps {
  options: FilterOptions
  activeFilters: SearchRequest['filters']
  onFiltersChange: (filters: SearchRequest['filters']) => void
}

export default function QdrantAdvancedFilters({ options, activeFilters, onFiltersChange }: QdrantAdvancedFiltersProps) {
  const handleFilterChange = (filterType: string, values: string[]) => {
    const newFilters = {
      ...activeFilters,
      [filterType]: values.length > 0 ? values : undefined
    }
    onFiltersChange(newFilters)
  }

  const handleDateChange = (field: 'date_from' | 'date_to', value: string) => {
    const newFilters = {
      ...activeFilters,
      [field]: value || undefined
    }
    onFiltersChange(newFilters)
  }

  const clearAllFilters = () => {
    onFiltersChange({})
  }

  const hasActiveFilters = Object.values(activeFilters).some(filter => 
    Array.isArray(filter) ? filter.length > 0 : Boolean(filter)
  )

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-medium">Filter Results</h3>
        {hasActiveFilters && (
          <button
            onClick={clearAllFilters}
            className="text-sm text-muted-foreground hover:text-foreground transition-colors"
          >
            Clear all
          </button>
        )}
      </div>

      {/* Core Contract Filters */}
      <div>
        <h4 className="text-sm font-medium text-muted-foreground mb-3">Contract Details</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Contract Type Filter */}
          <FilterSelect
            label="Contract Type"
            options={options.case_types}
            selected={activeFilters.case_type || []}
            onChange={(values) => handleFilterChange('case_type', values)}
          />

          {/* Industry Filter */}
          {options.industries && options.industries.length > 0 && (
            <FilterSelect
              label="Industry"
              options={options.industries}
              selected={activeFilters.industry || []}
              onChange={(values) => handleFilterChange('industry', values)}
            />
          )}

          {/* Company Size Filter */}
          {options.company_sizes && options.company_sizes.length > 0 && (
            <FilterSelect
              label="Company Size"
              options={options.company_sizes}
              selected={activeFilters.company_size || []}
              onChange={(values) => handleFilterChange('company_size', values)}
            />
          )}

          {/* Contract Status Filter */}
          {options.contract_statuses && options.contract_statuses.length > 0 && (
            <FilterSelect
              label="Contract Status"
              options={options.contract_statuses}
              selected={activeFilters.contract_status || []}
              onChange={(values) => handleFilterChange('contract_status', values)}
            />
          )}
        </div>
      </div>

      {/* Risk & Complexity Filters */}
      <div>
        <h4 className="text-sm font-medium text-muted-foreground mb-3">Risk Assessment</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Complexity Level Filter */}
          {options.complexity_levels && options.complexity_levels.length > 0 && (
            <FilterSelect
              label="Complexity Level"
              options={options.complexity_levels}
              selected={activeFilters.complexity_level || []}
              onChange={(values) => handleFilterChange('complexity_level', values)}
            />
          )}

          {/* Risk Level Filter */}
          {options.risk_levels && options.risk_levels.length > 0 && (
            <FilterSelect
              label="Risk Level"
              options={options.risk_levels}
              selected={activeFilters.risk_level || []}
              onChange={(values) => handleFilterChange('risk_level', values)}
            />
          )}

          {/* Renewal Terms Filter */}
          {options.renewal_terms && options.renewal_terms.length > 0 && (
            <FilterSelect
              label="Renewal Terms"
              options={options.renewal_terms}
              selected={activeFilters.renewal_terms || []}
              onChange={(values) => handleFilterChange('renewal_terms', values)}
            />
          )}
        </div>
      </div>

      {/* Legal & Geographic Filters */}
      <div>
        <h4 className="text-sm font-medium text-muted-foreground mb-3">Legal Context</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Jurisdiction Filter */}
          <FilterSelect
            label="Jurisdiction"
            options={options.jurisdictions}
            selected={activeFilters.jurisdiction || []}
            onChange={(values) => handleFilterChange('jurisdiction', values)}
          />

          {/* Court Level Filter */}
          <FilterSelect
            label="Business Context"
            options={options.court_levels}
            selected={activeFilters.court_level || []}
            onChange={(values) => handleFilterChange('court_level', values)}
          />
        </div>
      </div>

      {/* Date Range Filter */}
      <div>
        <h4 className="text-sm font-medium text-muted-foreground mb-3">Date Range</h4>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="text-sm font-medium block mb-2">From Date</label>
            <input
              type="date"
              placeholder="From date"
              value={activeFilters.date_from || ''}
              onChange={(e) => handleDateChange('date_from', e.target.value)}
              className="w-full px-3 py-2 text-sm border border-input rounded-md bg-background h-10"
            />
          </div>
          <div>
            <label className="text-sm font-medium block mb-2">To Date</label>
            <input
              type="date"
              placeholder="To date"
              value={activeFilters.date_to || ''}
              onChange={(e) => handleDateChange('date_to', e.target.value)}
              className="w-full px-3 py-2 text-sm border border-input rounded-md bg-background h-10"
            />
          </div>
        </div>
      </div>

      {/* Active Filters Display */}
      {hasActiveFilters && (
        <div className="space-y-2 pt-4 border-t border-border">
          <h4 className="text-sm font-medium text-muted-foreground">Active Filters</h4>
          <div className="flex flex-wrap gap-2">
            {activeFilters.case_type?.map((caseType) => (
              <FilterTag
                key={`case-type-${caseType}`}
                label={`Type: ${formatFilterValue(caseType)}`}
                onRemove={() => {
                  const newValues = activeFilters.case_type?.filter(c => c !== caseType) || []
                  handleFilterChange('case_type', newValues)
                }}
              />
            ))}
            {activeFilters.industry?.map((industry) => (
              <FilterTag
                key={`industry-${industry}`}
                label={`Industry: ${industry}`}
                onRemove={() => {
                  const newValues = activeFilters.industry?.filter(i => i !== industry) || []
                  handleFilterChange('industry', newValues)
                }}
              />
            ))}
            {activeFilters.company_size?.map((size) => (
              <FilterTag
                key={`company-size-${size}`}
                label={`Size: ${size}`}
                onRemove={() => {
                  const newValues = activeFilters.company_size?.filter(s => s !== size) || []
                  handleFilterChange('company_size', newValues)
                }}
              />
            ))}
            {activeFilters.contract_status?.map((status) => (
              <FilterTag
                key={`contract-status-${status}`}
                label={`Status: ${status}`}
                onRemove={() => {
                  const newValues = activeFilters.contract_status?.filter(s => s !== status) || []
                  handleFilterChange('contract_status', newValues)
                }}
              />
            ))}
            {activeFilters.complexity_level?.map((level) => (
              <FilterTag
                key={`complexity-${level}`}
                label={`Complexity: ${level}`}
                onRemove={() => {
                  const newValues = activeFilters.complexity_level?.filter(l => l !== level) || []
                  handleFilterChange('complexity_level', newValues)
                }}
              />
            ))}
            {activeFilters.risk_level?.map((level) => (
              <FilterTag
                key={`risk-${level}`}
                label={`Risk: ${level}`}
                onRemove={() => {
                  const newValues = activeFilters.risk_level?.filter(r => r !== level) || []
                  handleFilterChange('risk_level', newValues)
                }}
              />
            ))}
            {activeFilters.renewal_terms?.map((terms) => (
              <FilterTag
                key={`renewal-${terms}`}
                label={`Renewal: ${terms}`}
                onRemove={() => {
                  const newValues = activeFilters.renewal_terms?.filter(t => t !== terms) || []
                  handleFilterChange('renewal_terms', newValues)
                }}
              />
            ))}
            {activeFilters.jurisdiction?.map((jurisdiction) => (
              <FilterTag
                key={`jurisdiction-${jurisdiction}`}
                label={`Jurisdiction: ${jurisdiction}`}
                onRemove={() => {
                  const newValues = activeFilters.jurisdiction?.filter(j => j !== jurisdiction) || []
                  handleFilterChange('jurisdiction', newValues)
                }}
              />
            ))}
            {activeFilters.court_level?.map((courtLevel) => (
              <FilterTag
                key={`court-level-${courtLevel}`}
                label={`Context: ${formatFilterValue(courtLevel)}`}
                onRemove={() => {
                  const newValues = activeFilters.court_level?.filter(c => c !== courtLevel) || []
                  handleFilterChange('court_level', newValues)
                }}
              />
            ))}
            {activeFilters.date_from && (
              <FilterTag
                label={`From: ${activeFilters.date_from}`}
                onRemove={() => handleDateChange('date_from', '')}
              />
            )}
            {activeFilters.date_to && (
              <FilterTag
                label={`To: ${activeFilters.date_to}`}
                onRemove={() => handleDateChange('date_to', '')}
              />
            )}
          </div>
        </div>
      )}
    </div>
  )
}

// Helper function to format filter values for display
const formatFilterValue = (value: string): string => {
  return value.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
}

interface FilterSelectProps {
  label: string
  options: string[]
  selected: string[]
  onChange: (values: string[]) => void
}

function FilterSelect({ label, options, selected, onChange }: FilterSelectProps) {
  const [isOpen, setIsOpen] = useState(false)

  const toggleOption = (option: string) => {
    const newSelected = selected.includes(option)
      ? selected.filter(s => s !== option)
      : [...selected, option]
    onChange(newSelected)
  }

  if (!options || options.length === 0) {
    return null
  }

  return (
    <div className="relative h-fit">
      <label className="text-sm font-medium block mb-2 min-h-[2.5rem] flex items-end leading-tight">{label}</label>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-3 py-2 text-sm border border-input rounded-md bg-background text-left hover:bg-muted transition-colors h-10 flex items-center"
      >
        {selected.length > 0 ? `${selected.length} selected` : `Select ${label.toLowerCase()}`}
      </button>

      {isOpen && (
        <>
          <div 
            className="fixed inset-0 z-0" 
            onClick={() => setIsOpen(false)}
          />
          <div className="absolute top-full left-0 right-0 z-10 mt-1 bg-popover border border-border rounded-md shadow-lg max-h-48 overflow-y-auto">
            {options.map((option) => (
              <button
                key={option}
                onClick={() => toggleOption(option)}
                className={cn(
                  'w-full px-3 py-2 text-sm text-left hover:bg-muted transition-colors',
                  selected.includes(option) ? 'bg-primary/10 text-primary' : ''
                )}
              >
                <div className="flex items-center gap-2">
                  <div className={cn(
                    'w-3 h-3 border rounded-sm flex-shrink-0',
                    selected.includes(option) ? 'bg-primary border-primary' : 'border-input'
                  )} />
                  <span className="truncate">{formatFilterValue(option)}</span>
                </div>
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  )
}

interface FilterTagProps {
  label: string
  onRemove: () => void
}

function FilterTag({ label, onRemove }: FilterTagProps) {
  return (
    <div className="inline-flex items-center gap-1 px-2 py-1 bg-primary/10 text-primary text-sm rounded-md">
      <span>{label}</span>
      <button
        onClick={onRemove}
        className="hover:bg-primary/20 rounded-sm p-0.5 transition-colors"
      >
        <X className="h-3 w-3" />
      </button>
    </div>
  )
} 