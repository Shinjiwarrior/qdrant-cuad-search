import { Link } from 'react-router-dom'
import { ExternalLink, Calendar, MapPin, Scale, Star, Building2, DollarSign, AlertTriangle, RefreshCw } from 'lucide-react'
import { LegalCase } from '../../../lib/api'
import { formatDate, truncateText } from '../../../lib/utils'
import { cn } from '../../../lib/utils'

interface LegalCaseCardProps {
  case: LegalCase
  searchQuery?: string
}

export default function LegalCaseCard({ case: legalCase, searchQuery }: LegalCaseCardProps) {
  const getScoreColor = (score?: number) => {
    if (!score) return 'text-muted-foreground'
    if (score >= 0.9) return 'text-green-600'
    if (score >= 0.8) return 'text-green-500'
    if (score >= 0.7) return 'text-yellow-500'
    return 'text-orange-500'
  }

  const getCaseTypeColor = (caseType?: string) => {
    switch (caseType?.toLowerCase()) {
      case 'employment_agreement':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
      case 'license_agreement':
        return 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200'
      case 'service_agreement':
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
      case 'supply_agreement':
        return 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200'
      case 'lease_agreement':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
      case 'non-disclosure_agreement':
        return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
      case 'commercial_contract':
        return 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200'
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200'
    }
  }

  const getRiskLevelColor = (riskLevel?: string) => {
    switch (riskLevel?.toLowerCase()) {
      case 'high':
        return 'text-red-600 dark:text-red-400'
      case 'medium':
        return 'text-yellow-600 dark:text-yellow-400'
      case 'low':
        return 'text-green-600 dark:text-green-400'
      default:
        return 'text-muted-foreground'
    }
  }

  const formatCaseType = (caseType?: string) => {
    if (!caseType) return ''
    return caseType.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
  }

  return (
    <div className="bg-card border border-border rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow">
      {/* Header */}
      <div className="flex items-start justify-between gap-4 mb-4">
        <div className="flex-1">
          <Link 
            to={`/case/${legalCase.id}`}
            className="text-lg font-semibold text-foreground hover:text-primary transition-colors line-clamp-2"
          >
            {legalCase.case_name}
          </Link>
          
          {legalCase.citation && (
            <p className="text-sm text-muted-foreground mt-1">
              {legalCase.citation}
            </p>
          )}
        </div>

        {/* Relevance Score */}
        {legalCase.score && (
          <div className="flex items-center gap-1 text-sm">
            <Star className={cn('h-4 w-4', getScoreColor(legalCase.score))} />
            <span className={getScoreColor(legalCase.score)}>
              {Math.round(legalCase.score * 100)}%
            </span>
          </div>
        )}
      </div>

      {/* Contract Type and Status */}
      <div className="flex flex-wrap items-center gap-2 mb-4">
        {legalCase.case_type && (
          <span className={cn(
            'inline-block px-2 py-1 text-xs font-medium rounded-full',
            getCaseTypeColor(legalCase.case_type)
          )}>
            {formatCaseType(legalCase.case_type)}
          </span>
        )}
        
        {legalCase.contract_status && (
          <span className="inline-block px-2 py-1 text-xs font-medium rounded-full bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-200">
            {legalCase.contract_status}
          </span>
        )}

        {legalCase.estimated_value && (
          <span className="inline-block px-2 py-1 text-xs font-medium rounded-full bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-200">
            {legalCase.estimated_value}
          </span>
        )}
      </div>

      {/* Enhanced Metadata Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4 text-sm">
        {/* Industry & Company Size */}
        {legalCase.industry && (
          <div className="flex items-center gap-1 text-muted-foreground">
            <Building2 className="h-3 w-3" />
            <span className="truncate">{legalCase.industry}</span>
          </div>
        )}
        
        {legalCase.company_size && (
          <div className="flex items-center gap-1 text-muted-foreground">
            <Scale className="h-3 w-3" />
            <span className="truncate">{legalCase.company_size}</span>
          </div>
        )}

        {/* Risk & Complexity */}
        {legalCase.risk_level && (
          <div className="flex items-center gap-1">
            <AlertTriangle className={cn('h-3 w-3', getRiskLevelColor(legalCase.risk_level))} />
            <span className={cn('truncate', getRiskLevelColor(legalCase.risk_level))}>
              {legalCase.risk_level} Risk
            </span>
          </div>
        )}

        {legalCase.complexity_level && (
          <div className="flex items-center gap-1 text-muted-foreground">
            <span className="truncate">{legalCase.complexity_level} Complexity</span>
          </div>
        )}

        {/* Renewal Terms */}
        {legalCase.renewal_terms && (
          <div className="flex items-center gap-1 text-muted-foreground">
            <RefreshCw className="h-3 w-3" />
            <span className="truncate">{legalCase.renewal_terms}</span>
          </div>
        )}

        {/* Location */}
        {legalCase.jurisdiction && (
          <div className="flex items-center gap-1 text-muted-foreground">
            <MapPin className="h-3 w-3" />
            <span className="truncate capitalize">{legalCase.jurisdiction.replace(/_/g, ' ')}</span>
          </div>
        )}

        {/* Date */}
        {legalCase.date_filed && (
          <div className="flex items-center gap-1 text-muted-foreground">
            <Calendar className="h-3 w-3" />
            <span className="truncate">{formatDate(legalCase.date_filed)}</span>
          </div>
        )}

        {/* Court Level / Business Context */}
        {legalCase.court_level && (
          <div className="flex items-center gap-1 text-muted-foreground">
            <span className="truncate capitalize">{formatCaseType(legalCase.court_level)}</span>
          </div>
        )}
      </div>

      {/* Contract Duration (if available) */}
      {legalCase.contract_start_date && legalCase.contract_end_date && (
        <div className="mb-4 p-2 bg-muted/50 rounded-md">
          <div className="text-xs text-muted-foreground">
            <span className="font-medium">Contract Period:</span>
            <span className="ml-2">
              {formatDate(legalCase.contract_start_date)} → {formatDate(legalCase.contract_end_date)}
            </span>
          </div>
        </div>
      )}

      {/* Summary */}
      {legalCase.summary && (
        <div className="mb-4">
          <p className="text-sm text-muted-foreground leading-relaxed">
            {truncateText(legalCase.summary, 300)}
          </p>
        </div>
      )}

      {/* Actions */}
      <div className="flex items-center justify-between pt-4 border-t border-border">
        <Link
          to={`/case/${legalCase.id}`}
          className="inline-flex items-center gap-2 px-3 py-1 text-sm bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
        >
          View Details
        </Link>

        {legalCase.url && (
          <a
            href={legalCase.url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors"
          >
            <ExternalLink className="h-3 w-3" />
            CUAD Source
          </a>
        )}
      </div>
    </div>
  )
} 