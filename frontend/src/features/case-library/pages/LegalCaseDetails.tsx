import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, ExternalLink, Calendar, MapPin, Scale, Star, Copy, Check, Building2, AlertTriangle, RefreshCw, DollarSign, FileText, Users } from 'lucide-react'
import { getCaseById, type LegalCase } from '../../../lib/api'
import { formatDate } from '../../../lib/utils'
import { cn } from '../../../lib/utils'
import LoadingSpinner from '../../../shared/components/ui/LoadingSpinner'

export default function LegalCaseDetails() {
  const { id } = useParams<{ id: string }>()
  const [caseData, setCaseData] = useState<LegalCase | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [copiedField, setCopiedField] = useState<string | null>(null)
  const [activeSection, setActiveSection] = useState<'overview' | 'contract'>('overview')

  useEffect(() => {
    const fetchCase = async () => {
      if (!id) return

      try {
        setIsLoading(true)
        setError(null)
        
        const case_ = await getCaseById(id)
        setCaseData(case_)
      } catch (error: any) {
        console.error('Error fetching case:', error)
        const errorMessage = error.response?.data?.detail || error.message || 'Failed to load case details'
        setError(typeof errorMessage === 'string' ? errorMessage : 'Failed to load case details')
      } finally {
        setIsLoading(false)
      }
    }

    fetchCase()
  }, [id])

  const copyToClipboard = async (text: string, field: string) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopiedField(field)
      setTimeout(() => setCopiedField(null), 2000)
    } catch (error) {
      console.error('Failed to copy text:', error)
    }
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
      case 'non_disclosure_agreement':
        return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
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

  if (isLoading) {
    return (
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-center py-12">
          <LoadingSpinner size="lg" />
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="max-w-6xl mx-auto">
        <div className="bg-destructive/10 border border-destructive/20 rounded-lg p-6 text-center">
          <p className="text-destructive">{error}</p>
          <Link 
            to="/search" 
            className="inline-flex items-center gap-2 mt-4 text-primary hover:underline"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to Search
          </Link>
        </div>
      </div>
    )
  }

  if (!caseData) {
    return (
      <div className="max-w-6xl mx-auto">
        <div className="text-center py-12">
          <p className="text-muted-foreground">Contract not found</p>
          <Link 
            to="/search" 
            className="inline-flex items-center gap-2 mt-4 text-primary hover:underline"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to Search
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Navigation */}
      <div className="flex items-center gap-2">
        <Link 
          to="/search" 
          className="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to Search
        </Link>
      </div>

      {/* Header */}
      <div className="bg-card border border-border rounded-lg p-6 shadow-sm">
        <div className="flex items-start justify-between gap-4 mb-6">
          <div className="flex-1">
            <h1 className="text-3xl font-bold text-foreground mb-3">
              {caseData.case_name}
            </h1>
            
            {caseData.citation && (
              <div className="flex items-center gap-2 mb-2">
                <span className="text-sm font-medium text-muted-foreground">Citation:</span>
                <p className="text-sm text-muted-foreground">{caseData.citation}</p>
                <button
                  onClick={() => copyToClipboard(caseData.citation!, 'citation')}
                  className="p-1 hover:bg-muted rounded transition-colors"
                  title="Copy citation"
                >
                  {copiedField === 'citation' ? (
                    <Check className="h-3 w-3 text-green-500" />
                  ) : (
                    <Copy className="h-3 w-3" />
                  )}
                </button>
              </div>
            )}
          </div>

          <div className="flex items-center gap-3">
            {caseData.score && (
              <div className="flex items-center gap-2 text-sm bg-muted/50 px-3 py-2 rounded-lg">
                <Star className="h-4 w-4 text-yellow-500" />
                <span className="font-medium">Relevance:</span>
                <span className="text-muted-foreground">
                  {Math.round(caseData.score * 100)}%
                </span>
              </div>
            )}

            {caseData.url && (
              <a
                href={caseData.url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
              >
                <ExternalLink className="h-4 w-4" />
                CUAD Source
              </a>
            )}
          </div>
        </div>

        {/* Contract Type Badge */}
        {caseData.case_type && (
          <div className="mb-6">
            <span className={cn(
              'inline-flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-lg',
              getCaseTypeColor(caseData.case_type)
            )}>
              <FileText className="h-4 w-4" />
              {formatCaseType(caseData.case_type)}
            </span>
          </div>
        )}

        {/* Enhanced Metadata Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {/* Business Details */}
          {caseData.industry && (
            <div className="flex items-center gap-3">
              <Building2 className="h-5 w-5 text-muted-foreground" />
              <div>
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Industry</p>
                <p className="text-sm font-medium">{caseData.industry}</p>
              </div>
            </div>
          )}

          {caseData.company_size && (
            <div className="flex items-center gap-3">
              <Users className="h-5 w-5 text-muted-foreground" />
              <div>
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Company Size</p>
                <p className="text-sm font-medium">{caseData.company_size}</p>
              </div>
            </div>
          )}

          {caseData.estimated_value && (
            <div className="flex items-center gap-3">
              <DollarSign className="h-5 w-5 text-muted-foreground" />
              <div>
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Est. Value</p>
                <p className="text-sm font-medium">{caseData.estimated_value}</p>
              </div>
            </div>
          )}

          {caseData.jurisdiction && (
            <div className="flex items-center gap-3">
              <MapPin className="h-5 w-5 text-muted-foreground" />
              <div>
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Jurisdiction</p>
                <p className="text-sm font-medium capitalize">{caseData.jurisdiction.replace(/_/g, ' ')}</p>
              </div>
            </div>
          )}

          {/* Risk & Status */}
          {caseData.risk_level && (
            <div className="flex items-center gap-3">
              <AlertTriangle className={cn('h-5 w-5', getRiskLevelColor(caseData.risk_level))} />
              <div>
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Risk Level</p>
                <p className={cn('text-sm font-medium', getRiskLevelColor(caseData.risk_level))}>
                  {caseData.risk_level}
                </p>
              </div>
            </div>
          )}

          {caseData.complexity_level && (
            <div className="flex items-center gap-3">
              <Scale className="h-5 w-5 text-muted-foreground" />
              <div>
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Complexity</p>
                <p className="text-sm font-medium">{caseData.complexity_level}</p>
              </div>
            </div>
          )}

          {caseData.contract_status && (
            <div className="flex items-center gap-3">
              <div className={cn(
                'h-5 w-5 rounded-full',
                caseData.contract_status?.toLowerCase() === 'active' ? 'bg-green-500' :
                caseData.contract_status?.toLowerCase() === 'executed' ? 'bg-blue-500' :
                'bg-gray-500'
              )} />
              <div>
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Status</p>
                <p className="text-sm font-medium">{caseData.contract_status}</p>
              </div>
            </div>
          )}

          {caseData.renewal_terms && (
            <div className="flex items-center gap-3">
              <RefreshCw className="h-5 w-5 text-muted-foreground" />
              <div>
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Renewal Terms</p>
                <p className="text-sm font-medium">{caseData.renewal_terms}</p>
              </div>
            </div>
          )}
        </div>

        {/* Contract Duration */}
        {caseData.contract_start_date && caseData.contract_end_date && (
          <div className="mt-6 p-4 bg-muted/30 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <Calendar className="h-4 w-4 text-muted-foreground" />
              <span className="text-sm font-medium">Contract Period</span>
            </div>
            <p className="text-sm text-muted-foreground">
              {formatDate(caseData.contract_start_date)} → {formatDate(caseData.contract_end_date)}
            </p>
          </div>
        )}
      </div>

      {/* Section Navigation */}
      <div className="flex items-center gap-1 bg-muted/30 p-1 rounded-lg w-fit">
        <button
          onClick={() => setActiveSection('overview')}
          className={cn(
            'px-4 py-2 rounded-md text-sm font-medium transition-colors',
            activeSection === 'overview' 
              ? 'bg-background text-foreground shadow-sm' 
              : 'text-muted-foreground hover:text-foreground'
          )}
        >
          Overview
        </button>
        <button
          onClick={() => setActiveSection('contract')}
          className={cn(
            'px-4 py-2 rounded-md text-sm font-medium transition-colors',
            activeSection === 'contract' 
              ? 'bg-background text-foreground shadow-sm' 
              : 'text-muted-foreground hover:text-foreground'
          )}
        >
          Full Contract Text
        </button>
      </div>

      {/* Content Sections */}
      {activeSection === 'overview' && (
        <div className="space-y-6">
          {/* Summary */}
          {caseData.summary && (
            <div className="bg-card border border-border rounded-lg p-6 shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold">Contract Summary</h2>
                <button
                  onClick={() => copyToClipboard(caseData.summary!, 'summary')}
                  className="p-2 hover:bg-muted rounded transition-colors"
                  title="Copy summary"
                >
                  {copiedField === 'summary' ? (
                    <Check className="h-4 w-4 text-green-500" />
                  ) : (
                    <Copy className="h-4 w-4" />
                  )}
                </button>
              </div>
              <div className="prose prose-sm max-w-none dark:prose-invert">
                <p className="text-muted-foreground leading-relaxed">
                  {caseData.summary}
                </p>
              </div>
            </div>
          )}

          {/* Additional Metadata */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {caseData.court && (
              <div className="bg-card border border-border rounded-lg p-4">
                <h3 className="font-medium mb-2">Court Information</h3>
                <p className="text-sm text-muted-foreground">{caseData.court}</p>
              </div>
            )}

            {caseData.date_filed && (
              <div className="bg-card border border-border rounded-lg p-4">
                <h3 className="font-medium mb-2">Date Filed</h3>
                <p className="text-sm text-muted-foreground">{formatDate(caseData.date_filed)}</p>
              </div>
            )}
          </div>
        </div>
      )}

      {activeSection === 'contract' && caseData.full_text && (
        <div className="bg-card border border-border rounded-lg p-6 shadow-sm">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold">Full Contract Text</h2>
            <button
              onClick={() => copyToClipboard(caseData.full_text!, 'full_text')}
              className="inline-flex items-center gap-2 px-4 py-2 bg-secondary text-secondary-foreground rounded-md hover:bg-secondary/80 transition-colors"
              title="Copy full text"
            >
              {copiedField === 'full_text' ? (
                <Check className="h-4 w-4 text-green-500" />
              ) : (
                <Copy className="h-4 w-4" />
              )}
              {copiedField === 'full_text' ? 'Copied!' : 'Copy Text'}
            </button>
          </div>
          
          <div className="bg-muted/30 rounded-lg p-6 font-mono text-sm leading-relaxed">
            <div className="max-h-96 overflow-y-auto">
              <pre className="whitespace-pre-wrap text-foreground">
                {caseData.full_text}
              </pre>
            </div>
          </div>
          
          <div className="mt-4 text-xs text-muted-foreground">
            <p>Contract length: {caseData.full_text.length} characters</p>
          </div>
        </div>
      )}

      {/* Copy Success Message */}
      {copiedField && (
        <div className="fixed bottom-4 right-4 bg-green-100 border border-green-300 text-green-800 px-4 py-2 rounded-lg shadow-lg">
          <div className="flex items-center gap-2">
            <Check className="h-4 w-4" />
            <span>Copied to clipboard!</span>
          </div>
        </div>
      )}
    </div>
  )
} 