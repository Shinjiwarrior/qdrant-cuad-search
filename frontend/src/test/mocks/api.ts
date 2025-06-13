import { http, HttpResponse } from 'msw'

const API_BASE = 'http://localhost:8000/api'

export const handlers = [
  // Search endpoint
  http.post(`${API_BASE}/search`, ({ request }) => {
    return HttpResponse.json({
      results: [
        {
          id: 'case_1',
          title: 'Test Software License Agreement',
          content: 'This is a test software license agreement case...',
          score: 0.95,
          metadata: {
            jurisdiction: 'California',
            court_level: 'Superior Court',
            case_type: 'Contract Dispute',
            date: '2023-01-15',
            industry: 'Technology'
          }
        },
        {
          id: 'case_2',
          title: 'Enterprise Service Contract',
          content: 'Enterprise service contract dispute case...',
          score: 0.87,
          metadata: {
            jurisdiction: 'New York',
            court_level: 'Appeals Court', 
            case_type: 'Contract Dispute',
            date: '2023-03-22',
            industry: 'Technology'
          }
        }
      ],
      processing_time: 0.123,
      total_count: 2,
      search_metadata: {
        query_embeddings: 'generated',
        stage_1_candidates: 1000,
        stage_2_candidates: 100,
        final_results: 2
      }
    })
  }),

  // Get case by ID
  http.get(`${API_BASE}/cases/:id`, ({ params }) => {
    const { id } = params
    return HttpResponse.json({
      id,
      title: `Case ${id} Title`,
      content: `Full content for case ${id}...`,
      metadata: {
        jurisdiction: 'California',
        court_level: 'Superior Court',
        case_type: 'Contract Dispute',
        date: '2023-01-15',
        industry: 'Technology',
        company_size: 'Large',
        complexity_level: 'High'
      },
      related_cases: ['related_1', 'related_2'],
      citations: ['Citation 1', 'Citation 2']
    })
  }),

  // Get filter options
  http.get(`${API_BASE}/filters`, () => {
    return HttpResponse.json({
      jurisdictions: ['California', 'New York', 'Texas'],
      court_levels: ['Superior Court', 'Appeals Court', 'Supreme Court'],
      case_types: ['Contract Dispute', 'Intellectual Property', 'Employment'],
      industries: ['Technology', 'Healthcare', 'Finance'],
      company_sizes: ['Small', 'Medium', 'Large'],
      contract_statuses: ['Active', 'Expired', 'Pending'],
      complexity_levels: ['Low', 'Medium', 'High'],
      risk_levels: ['Low', 'Medium', 'High'],
      renewal_terms: ['Annual', 'Quarterly', 'Monthly']
    })
  }),

  // Health check
  http.get(`${API_BASE}/health`, () => {
    return HttpResponse.json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      version: '1.0.0-test',
      qdrant_status: 'healthy'
    })
  }),

  // Stats endpoint
  http.get(`${API_BASE}/stats`, () => {
    return HttpResponse.json({
      collection_status: 'green',
      total_cases: 1000,
      vector_count: 1000,
      search_type: 'Advanced Multi-Vector',
      features: ['Byte vector prefetch', 'Dense vector reranking']
    })
  })
]

// Error handlers for testing error scenarios
export const errorHandlers = [
  http.post(`${API_BASE}/search`, () => {
    return new HttpResponse(null, { status: 500 })
  }),

  http.get(`${API_BASE}/cases/:id`, () => {
    return new HttpResponse(null, { status: 404 })
  }),

  http.get(`${API_BASE}/filters`, () => {
    return new HttpResponse(null, { status: 500 })
  })
] 