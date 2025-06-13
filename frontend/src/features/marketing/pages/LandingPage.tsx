import { Link } from 'react-router-dom'
import { Search, Code, Shield, Zap, ArrowRight, Users, Globe, BarChart3, CheckCircle, Clock, FileText, Building2 } from 'lucide-react'

export default function LandingPage() {
  const features = [
    {
      icon: Search,
      title: "Coarse-to-Fine Contract Search",
      description: "Smaller, faster dense vectors fetch broad contract candidates, then ColBERT's multi-vector model refines results with larger, more accurate representations",
      color: "text-blue-500"
    },
    {
      icon: FileText,
      title: "CUAD Commercial Contract Database", 
      description: "510 real-world commercial contracts from the premier CUAD dataset, spanning technology, healthcare, finance, and enterprise agreements",
      color: "text-green-500"
    },
    {
      icon: Code,
      title: "Best of All Worlds Architecture",
      description: "Qdrant's two-stage interface: coarse results fetched first with dense vectors, then refined with ColBERT's contextualized late interaction",
      color: "text-purple-500"
    },
    {
      icon: Zap,
      title: "Advanced Contract Intelligence",
      description: "Multi-stage search with candidate prefetch, intelligent refinement, and real-time filtering by industry, contract type, and business terms",
      color: "text-orange-500"
    }
  ]

  const useCases = [
    {
      title: "Legal Teams",
      description: "Contract review, due diligence, clause analysis, and precedent research with comprehensive commercial examples",
      icon: "⚖️"
    },
    {
      title: "Business Development", 
      description: "Deal structuring, term sheets, negotiation prep, and competitive analysis with market-standard contract terms",
      icon: "💼"
    },
    {
      title: "Compliance & Risk",
      description: "Risk assessment, regulatory review, audit preparation, and policy alignment with proven contract language",
      icon: "🛡️"
    },
    {
      title: "Contract Research",
      description: "Academic research, market analysis, legal scholarship with the most comprehensive labeled contract dataset",
      icon: "📊"
    }
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section with Gradient */}
      <section className="relative overflow-hidden">
        {/* Gradient Background */}
        <div className="absolute inset-0 bg-gradient-to-r from-violet-600 via-blue-600 via-cyan-500 via-teal-500 to-green-500 opacity-10"></div>
        <div className="absolute inset-0 bg-gradient-to-br from-background/50 to-background/80"></div>
        
        <div className="relative max-w-7xl mx-auto px-4 py-24">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left Column - Hero Content */}
            <div className="space-y-8">
              <div className="space-y-4">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary text-sm font-medium">
                  <CheckCircle className="h-4 w-4" />
                  CUAD Dataset: 510 Real Commercial Contracts
                </div>
                <h1 className="text-5xl lg:text-6xl font-bold leading-tight">
                  Commercial contract
                  <span className="block bg-gradient-to-r from-violet-600 to-cyan-500 bg-clip-text text-transparent">
                    intelligence
                  </span>
                </h1>
                <p className="text-xl text-muted-foreground leading-relaxed max-w-lg">
                  Transform how you analyze commercial contracts with AI-powered semantic search through the premier CUAD dataset. Find the exact clauses and business terms you need in seconds.
                </p>
              </div>

              <div className="flex flex-col sm:flex-row gap-4">
                <Link
                  to="/search"
                  className="inline-flex items-center justify-center px-8 py-4 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors font-medium text-lg group"
                >
                  Explore CUAD contracts
                  <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
                </Link>
                <a
                  href="#case-studies"
                  className="inline-flex items-center justify-center px-8 py-4 border border-border rounded-lg hover:bg-muted transition-colors font-medium text-lg"
                >
                  See success stories
                </a>
              </div>

              {/* Trust Indicators */}
              <div className="flex flex-wrap items-center gap-6 text-sm text-muted-foreground">
                <div className="flex items-center gap-2">
                  <CheckCircle className="h-4 w-4 text-green-500" />
                  <span>510 real contracts</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle className="h-4 w-4 text-blue-500" />
                  <span>13K+ labeled clauses</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle className="h-4 w-4 text-purple-500" />
                  <span>Expert annotations</span>
                </div>
              </div>
            </div>

            {/* Right Column - Visual Element */}
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-violet-500/20 to-cyan-500/20 rounded-3xl blur-3xl"></div>
              <div className="relative bg-card border border-border rounded-2xl shadow-2xl overflow-hidden">
                {/* Mock Interface Content */}
                <div className="p-6 space-y-4">
                  {/* Search Bar */}
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                    <div className="w-full pl-10 pr-4 py-3 bg-background border border-input rounded-md text-sm">
                      <span className="text-foreground">employment termination clause</span>
                      <span className="animate-pulse">|</span>
                    </div>
                  </div>

                  {/* Search Results Header */}
                  <div className="flex items-center justify-between text-xs text-muted-foreground border-b border-border pb-2">
                    <span><strong className="text-foreground">3</strong> results found</span>
                    <span className="flex items-center gap-1">
                      <Clock className="h-3 w-3" />
                      0.28s
                    </span>
                  </div>

                  {/* Mock Search Results */}
                  <div className="space-y-3">
                    {/* CUAD Employment Contract */}
                    <div className="border border-border rounded-lg p-3 space-y-2 hover:shadow-md transition-shadow">
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                        <span className="text-xs font-medium text-blue-600 dark:text-blue-400">EMPLOYMENT AGREEMENT</span>
                        <span className="text-xs text-muted-foreground ml-auto">96% match</span>
                      </div>
                      <h4 className="text-sm font-medium">Tech Corp - Executive Employment Agreement</h4>
                      <p className="text-xs text-muted-foreground leading-relaxed">
                        Company may terminate Executive's employment immediately for Cause, including but not limited to material breach of duties, conviction of felony...
                      </p>
                    </div>

                    {/* CUAD Service Agreement */}
                    <div className="border border-border rounded-lg p-3 space-y-2 hover:shadow-md transition-shadow">
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                        <span className="text-xs font-medium text-green-600 dark:text-green-400">SERVICE AGREEMENT</span>
                        <span className="text-xs text-muted-foreground ml-auto">94% match</span>
                      </div>
                      <h4 className="text-sm font-medium">Software License & Services Agreement</h4>
                      <p className="text-xs text-muted-foreground leading-relaxed">
                        Either party may terminate for cause upon written notice if the other party materially breaches this Agreement...
                      </p>
                    </div>

                    {/* CUAD Vendor Agreement */}
                    <div className="border border-border rounded-lg p-3 space-y-2 hover:shadow-md transition-shadow">
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                        <span className="text-xs font-medium text-purple-600 dark:text-purple-400">VENDOR AGREEMENT</span>
                        <span className="text-xs text-muted-foreground ml-auto">91% match</span>
                      </div>
                      <h4 className="text-sm font-medium">Master Supply Agreement - Healthcare Corp</h4>
                      <p className="text-xs text-muted-foreground leading-relaxed">
                        Customer reserves the right to terminate immediately for cause including supplier's failure to meet quality standards...
                      </p>
                    </div>
                  </div>

                  {/* AI Badge */}
                  <div className="flex justify-center pt-2">
                    <div className="inline-flex items-center gap-2 px-3 py-1 bg-primary/10 text-primary rounded-full text-xs font-medium">
                      <span className="w-2 h-2 bg-primary rounded-full animate-pulse"></span>
                      CUAD Contract Intelligence
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold mb-4">
              Next-Generation Contract Intelligence Platform
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Everything you need to search, analyze, and understand commercial contracts with AI precision using the premier CUAD dataset.
            </p>
          </div>

          <div className="grid lg:grid-cols-2 gap-12">
            {features.map((feature, index) => (
              <div key={index} className="space-y-4">
                <div className="flex items-start gap-4">
                  <div className={`p-3 rounded-lg bg-muted ${feature.color}`}>
                    <feature.icon className="h-6 w-6" />
                  </div>
                  <div className="space-y-2">
                    <h3 className="text-xl font-semibold">
                      {feature.title}
                    </h3>
                    <p className="text-muted-foreground leading-relaxed">
                      {feature.description}
                    </p>
                    <Link 
                      to="/search" 
                      className="inline-flex items-center text-primary hover:underline text-sm font-medium"
                    >
                      Explore contracts
                      <ArrowRight className="ml-1 h-3 w-3" />
                    </Link>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Use Cases Section */}
      <section className="relative py-24 bg-gradient-to-br from-primary/5 to-cyan-500/5 overflow-hidden">
        <div className="absolute inset-0 bg-grid-pattern opacity-[0.02]"></div>
        
        <div className="relative max-w-7xl mx-auto px-4">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div className="space-y-8">
              <div className="space-y-4">
                <h2 className="text-3xl lg:text-4xl font-bold">
                  Perfect for Contract Professionals
                </h2>
                <p className="text-xl text-muted-foreground">
                  Whether you're reviewing contracts, conducting due diligence, or researching business terms, 
                  our platform provides comprehensive intelligence from real commercial agreements.
                </p>
              </div>

              <div className="grid grid-cols-2 gap-6">
                {useCases.map((useCase, index) => (
                  <div key={index} className="bg-background/80 backdrop-blur border border-border rounded-lg p-4 space-y-2">
                    <div className="text-2xl">{useCase.icon}</div>
                    <h3 className="font-semibold text-sm">{useCase.title}</h3>
                    <p className="text-xs text-muted-foreground">{useCase.description}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-violet-500/20 to-cyan-500/20 rounded-3xl blur-3xl"></div>
              <div className="relative bg-card border border-border rounded-2xl p-8 shadow-xl">
                <div className="space-y-6">
                  <div className="flex items-center justify-between">
                    <h3 className="font-semibold">Contract Search</h3>
                    <span className="text-xs text-muted-foreground">3 contracts in 0.31s</span>
                  </div>
                  
                  {[
                    { type: "Employment", color: "bg-blue-500" },
                    { type: "License", color: "bg-green-500" },
                    { type: "Supply", color: "bg-purple-500" }
                  ].map((contract, i) => (
                    <div key={i} className="border border-border rounded-lg p-4 space-y-2">
                      <div className="flex items-center gap-2">
                        <div className={`w-2 h-2 rounded-full ${contract.color}`}></div>
                        <span className="text-sm font-medium">{contract.type} Agreement</span>
                        <span className="text-xs text-muted-foreground ml-auto">95% match</span>
                      </div>
                      <div className="space-y-1">
                        <div className="h-2 bg-muted rounded w-full"></div>
                        <div className="h-2 bg-muted rounded w-3/4"></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Case Studies Section */}
      <section id="case-studies" className="py-24 bg-gradient-to-br from-slate-50 to-blue-50 dark:from-slate-900 dark:to-slate-800">
        <div className="max-w-7xl mx-auto px-4">
          {/* Hero Strip */}
          <div className="text-center mb-16">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-primary/10 text-primary rounded-full text-sm font-medium mb-4">
              <BarChart3 className="h-4 w-4" />
              Proven in Production
            </div>
            <h2 className="text-3xl lg:text-4xl font-bold mb-4">
              From billable hours to bullet-time search
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto mb-8">
              Real legal tech teams using Qdrant vector search to transform their workflows
            </p>
            
            {/* Rotating Stats */}
            <div className="flex flex-wrap justify-center gap-8 text-center">
              <div className="bg-white dark:bg-slate-800 rounded-lg p-4 shadow-md border border-border">
                <div className="text-2xl font-bold text-green-600">90%</div>
                <div className="text-sm text-muted-foreground">Faster due-diligence</div>
              </div>
              <div className="bg-white dark:bg-slate-800 rounded-lg p-4 shadow-md border border-border">
                <div className="text-2xl font-bold text-blue-600">75%</div>
                <div className="text-sm text-muted-foreground">Cost reduction</div>
              </div>
              <div className="bg-white dark:bg-slate-800 rounded-lg p-4 shadow-md border border-border">
                <div className="text-2xl font-bold text-purple-600">92%</div>
                <div className="text-sm text-muted-foreground">Recall accuracy</div>
              </div>
            </div>
          </div>

          {/* Case Studies Grid */}
          <div className="grid lg:grid-cols-2 gap-8 mb-12">
            {/* Aracor Case Study */}
            <div className="bg-white dark:bg-slate-800 rounded-xl border border-border shadow-lg hover:shadow-xl transition-shadow p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center text-white font-bold">
                    A
                  </div>
                  <div>
                    <h3 className="font-semibold text-lg">Aracor</h3>
                    <p className="text-sm text-muted-foreground">M&A Due-Diligence Platform</p>
                  </div>
                </div>
                <div className="flex gap-2">
                  <span className="px-2 py-1 bg-green-100 dark:bg-green-900/20 text-green-700 dark:text-green-300 text-xs rounded-full">
                    Hybrid Search
                  </span>
                  <span className="px-2 py-1 bg-blue-100 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 text-xs rounded-full">
                    Metadata Filters
                  </span>
                </div>
              </div>
              
              <h4 className="font-medium mb-2 text-primary">90% faster M&A workflows</h4>
              <p className="text-sm text-muted-foreground mb-4">
                Replaced weeks of lawyers combing through thousands of PDFs, signature pages, and patent exhibits with 
                hybrid vector search and multi-tenant collections.
              </p>
              
              <div className="grid grid-cols-3 gap-4 mb-4">
                <div className="text-center">
                  <div className="text-lg font-bold text-green-600">90%</div>
                  <div className="text-xs text-muted-foreground">Faster workflows</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-bold text-blue-600">70%</div>
                  <div className="text-xs text-muted-foreground">Time reduction</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-bold text-purple-600">40%</div>
                  <div className="text-xs text-muted-foreground">Fewer billable hours</div>
                </div>
              </div>
              
              <a 
                href="https://qdrant.tech/blog/case-study-aracor/" 
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center text-primary hover:underline text-sm font-medium"
              >
                Read full case study
                <ArrowRight className="ml-1 h-3 w-3" />
              </a>
            </div>

            {/* Lawme.ai Case Study */}
            <div className="bg-white dark:bg-slate-800 rounded-xl border border-border shadow-lg hover:shadow-xl transition-shadow p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-gradient-to-r from-violet-500 to-purple-500 rounded-lg flex items-center justify-center text-white font-bold">
                    L
                  </div>
                  <div>
                    <h3 className="font-semibold text-lg">Lawme.ai</h3>
                    <p className="text-sm text-muted-foreground">AI Legal Assistant</p>
                  </div>
                </div>
                <div className="flex gap-2">
                  <span className="px-2 py-1 bg-orange-100 dark:bg-orange-900/20 text-orange-700 dark:text-orange-300 text-xs rounded-full">
                    HNSW
                  </span>
                  <span className="px-2 py-1 bg-cyan-100 dark:bg-cyan-900/20 text-cyan-700 dark:text-cyan-300 text-xs rounded-full">
                    Binary Quantization
                  </span>
                </div>
              </div>
              
              <h4 className="font-medium mb-2 text-primary">75% infrastructure cost drop</h4>
              <p className="text-sm text-muted-foreground mb-4">
                Migrated from PGVector when costs ballooned and timeouts occurred as document sets grew across 
                multiple jurisdictions. Self-hosted Qdrant solved scaling issues.
              </p>
              
              <div className="grid grid-cols-2 gap-4 mb-4">
                <div className="text-center">
                  <div className="text-lg font-bold text-green-600">75%</div>
                  <div className="text-xs text-muted-foreground">Cost reduction</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-bold text-blue-600">&lt;150ms</div>
                  <div className="text-xs text-muted-foreground">Latency at 10× scale</div>
                </div>
              </div>
              
              <a 
                href="https://www.linkedin.com/posts/qdrant_scaling-ai-legal-assistants-with-vector-activity-7313817633223585793-kzxw" 
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center text-primary hover:underline text-sm font-medium"
              >
                View LinkedIn story
                <ArrowRight className="ml-1 h-3 w-3" />
              </a>
            </div>

            {/* Relari × GitLab Case Study */}
            <div className="bg-white dark:bg-slate-800 rounded-xl border border-border shadow-lg hover:shadow-xl transition-shadow p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-gradient-to-r from-red-500 to-orange-500 rounded-lg flex items-center justify-center text-white font-bold">
                    R
                  </div>
                  <div>
                    <h3 className="font-semibold text-lg">Relari × GitLab</h3>
                    <p className="text-sm text-muted-foreground">Legal Policy RAG</p>
                  </div>
                </div>
                <div className="flex gap-2">
                  <span className="px-2 py-1 bg-green-100 dark:bg-green-900/20 text-green-700 dark:text-green-300 text-xs rounded-full">
                    A/B Testing
                  </span>
                  <span className="px-2 py-1 bg-blue-100 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 text-xs rounded-full">
                    Hybrid RAG
                  </span>
                </div>
              </div>
              
              <h4 className="font-medium mb-2 text-primary">92% recall for policy Q&A</h4>
              <p className="text-sm text-muted-foreground mb-4">
                Needed hard metrics to choose the best retrieval strategy. Ran A/B tests comparing pure vector, 
                BM25, and hybrid approaches directly on Qdrant collections.
              </p>
              
              <div className="grid grid-cols-2 gap-4 mb-4">
                <div className="text-center">
                  <div className="text-lg font-bold text-green-600">92%</div>
                  <div className="text-xs text-muted-foreground">Hybrid recall</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-bold text-blue-600">32%</div>
                  <div className="text-xs text-muted-foreground">Precision improvement</div>
                </div>
              </div>
              
              <a 
                href="https://www.relari.ai/blog/case-study-relari-qdrant-rag-optimization" 
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center text-primary hover:underline text-sm font-medium"
              >
                Read optimization study
                <ArrowRight className="ml-1 h-3 w-3" />
              </a>
            </div>

            {/* Open Source Demos */}
            <div className="bg-white dark:bg-slate-800 rounded-xl border border-border shadow-lg hover:shadow-xl transition-shadow p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-gradient-to-r from-green-500 to-teal-500 rounded-lg flex items-center justify-center text-white font-bold">
                    📚
                  </div>
                  <div>
                    <h3 className="font-semibold text-lg">Open Source Demos</h3>
                    <p className="text-sm text-muted-foreground">Legal Case Search Engines</p>
                  </div>
                </div>
                <div className="flex gap-2">
                  <span className="px-2 py-1 bg-purple-100 dark:bg-purple-900/20 text-purple-700 dark:text-purple-300 text-xs rounded-full">
                    Llama 3
                  </span>
                  <span className="px-2 py-1 bg-yellow-100 dark:bg-yellow-900/20 text-yellow-700 dark:text-yellow-300 text-xs rounded-full">
                    LangChain
                  </span>
                </div>
              </div>
              
              <h4 className="font-medium mb-2 text-primary">Ready-to-fork implementations</h4>
              <p className="text-sm text-muted-foreground mb-4">
                Step-by-step tutorials and notebooks showing how to build legal case search engines with 
                Llama 3, LangChain, and Qdrant, focusing on rich metadata filters.
              </p>
              
              <div className="flex gap-4 mb-4">
                <a 
                  href="https://pub.towardsai.net/building-a-legal-case-search-engine-using-qdrant-llama-3-langchain-and-exploring-different-655ed5b25f30" 
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs px-3 py-1 bg-blue-100 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 rounded-full hover:bg-blue-200 dark:hover:bg-blue-900/40 transition-colors"
                >
                  TowardsAI Tutorial
                </a>
                <a 
                  href="https://medium.com/@sagaruprety/how-to-build-a-legal-information-retrieval-search-engine-using-mistral-qdrant-and-langchain-1a94c1293d72" 
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs px-3 py-1 bg-green-100 dark:bg-green-900/20 text-green-700 dark:text-green-300 rounded-full hover:bg-green-200 dark:hover:bg-green-900/40 transition-colors"
                >
                  Medium Guide
                </a>
              </div>
              
              <a 
                href="https://qdrant.tech/legal-tech/" 
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center text-primary hover:underline text-sm font-medium"
              >
                Explore all legal tech examples
                <ArrowRight className="ml-1 h-3 w-3" />
              </a>
            </div>
          </div>

          {/* Build It Yourself Section */}
          <div className="bg-gradient-to-r from-primary/10 to-cyan-500/10 rounded-2xl p-8 text-center">
            <h3 className="text-2xl font-bold mb-4">Join the legal tech leaders</h3>
            <p className="text-muted-foreground mb-6 max-w-2xl mx-auto">
              Deploy the same coarse-to-fine architecture used by Aracor, Lawme.ai, and GitLab. Get 90% faster workflows with proven vector search technology.
            </p>
            
            <div className="flex flex-wrap justify-center gap-4">
              <Link
                to="/search"
                className="inline-flex items-center px-6 py-3 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors font-medium"
              >
                <Code className="mr-2 h-4 w-4" />
                Experience the search
              </Link>
              <a
                href="https://qdrant.tech/legal-tech/"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center px-6 py-3 border border-border rounded-lg hover:bg-muted transition-colors font-medium"
              >
                <BarChart3 className="mr-2 h-4 w-4" />
                View case studies
              </a>
            </div>
            
            {/* Mini success metrics */}
            <div className="mt-6 flex flex-wrap justify-center gap-8 text-sm text-muted-foreground">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span>Aracor: 90% faster</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                <span>Lawme.ai: 75% cheaper</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                <span>GitLab: 92% accurate</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Developer Section */}
      <section className="bg-slate-900 text-white py-24">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div className="space-y-8">
              <div className="space-y-4">
                <h2 className="text-3xl lg:text-4xl font-bold">
                  Coarse-to-Fine Query API
                </h2>
                <p className="text-xl text-slate-300">
                  Integrate advanced two-stage retrieval into your applications. Dense candidate fetching for speed, 
                  ColBERT refinement for precision, all through Qdrant's convenient interface.
                </p>
              </div>

              <div className="space-y-4">
                {[
                  "Dense vector candidate fetching",
                  "ColBERT multi-vector refinement", 
                  "Coarse-to-fine query optimization",
                  "Smaller → larger representation pipeline",
                  "Sub-second end-to-end latency",
                  "CUAD legal corpus"
                ].map((feature, index) => (
                  <div key={index} className="flex items-center gap-3">
                    <CheckCircle className="h-5 w-5 text-green-400" />
                    <span>{feature}</span>
                  </div>
                ))}
              </div>

              <Link
                to="/search"
                className="inline-flex items-center px-6 py-3 bg-white text-slate-900 rounded-lg hover:bg-slate-100 transition-colors font-medium"
              >
                <Code className="mr-2 h-5 w-5" />
                Try the API
              </Link>
            </div>

            <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
              <div className="space-y-4">
                <div className="flex items-center gap-2 text-sm text-slate-400">
                  <div className="flex gap-1">
                    <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                    <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                    <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                  </div>
                  <span>Terminal</span>
                </div>
                <pre className="text-sm text-slate-300 overflow-x-auto">
{`curl -X POST /api/search \\
  -H "Content-Type: application/json" \\
  -d '{
    "query": "employment termination",
    "filters": {
      "industry": ["Technology"],
      "company_size": ["Enterprise"]
    },
    "limit": 10
  }'`}
                </pre>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24">
        <div className="max-w-4xl mx-auto px-4 text-center space-y-8">
          <h2 className="text-3xl lg:text-4xl font-bold">
            Ready to achieve 90% faster legal workflows?
          </h2>
          <p className="text-xl text-muted-foreground">
            Join Aracor, Lawme.ai, and other leading legal tech companies using Qdrant Legal Search's proven coarse-to-fine architecture for breakthrough performance.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/search"
              className="inline-flex items-center justify-center px-8 py-4 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors font-medium text-lg group"
            >
              Try the proven platform
              <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
            </Link>
            <a
              href="#case-studies"
              className="inline-flex items-center justify-center px-8 py-4 border border-border rounded-lg hover:bg-muted transition-colors font-medium text-lg"
            >
              Read success stories
            </a>
          </div>
          
          {/* Final trust indicators */}
          <div className="flex flex-wrap justify-center gap-6 text-sm text-muted-foreground pt-4">
            <span className="flex items-center gap-2">
              <CheckCircle className="h-4 w-4 text-green-500" />
              Production-tested
            </span>
            <span className="flex items-center gap-2">
              <CheckCircle className="h-4 w-4 text-blue-500" />
              Enterprise-ready
            </span>
            <span className="flex items-center gap-2">
              <CheckCircle className="h-4 w-4 text-purple-500" />
              Open source tutorials
            </span>
          </div>
        </div>
      </section>
    </div>
  )
} 