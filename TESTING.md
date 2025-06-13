# Testing Guide - Legal Research Platform

This guide covers all testing aspects of the Legal Research Platform, including backend API tests, frontend component tests, integration tests, and end-to-end workflows.

## 🚀 Quick Start

Run all tests with a single command:

```bash
./run_tests.sh
```

## 📚 Test Structure

### Backend Tests (`backend/tests/`)

```
backend/tests/
├── __init__.py
├── conftest.py           # Test configuration and fixtures
├── test_api.py          # API endpoint tests
├── test_middleware.py   # Middleware and error handling tests
├── test_integration.py  # Service integration tests
└── test_e2e.py         # End-to-end workflow tests
```

### Frontend Tests (`frontend/src/`)

```
frontend/src/
├── test/
│   ├── setup.ts         # Test setup and configuration
│   ├── utils.tsx        # Test utilities and helpers
│   └── mocks/
│       └── api.ts       # API mocks for testing
├── components/__tests__/
│   ├── Header.test.tsx
│   └── CaseCard.test.tsx
└── pages/__tests__/
    └── DemoPage.test.tsx
```

## 🧪 Test Categories

### 1. Backend API Tests

**What's tested:**
- All API endpoints (`/api/search`, `/api/cases/:id`, `/api/filters`, etc.)
- Request validation and error handling
- Response format and status codes
- Authentication and authorization (if applicable)

**Run backend tests only:**
```bash
./run_tests.sh --backend-only
```

**Or directly with pytest:**
```bash
cd backend
python3 -m pytest tests/ -v
```

### 2. Frontend Component Tests

**What's tested:**
- Component rendering and props
- User interactions (clicks, form submissions)
- State management and hooks
- Accessibility and keyboard navigation
- Error boundaries and loading states

**Run frontend tests only:**
```bash
./run_tests.sh --frontend-only
```

**Or directly with npm:**
```bash
cd frontend
npm run test:run
```

### 3. Integration Tests

**What's tested:**
- API and service layer interactions
- Database connectivity (Qdrant)
- Search pipeline (embedding → search → ranking)
- Filter functionality
- Error propagation and recovery

### 4. End-to-End Tests

**What's tested:**
- Complete user workflows
- Multi-step search scenarios
- System monitoring and health checks
- Performance under load
- Error recovery scenarios

## 🔧 Test Configuration

### Backend Configuration (`backend/pytest.ini`)

```ini
[tool:pytest]
testpaths = tests
addopts = 
    --verbose
    --cov=app
    --cov-report=term-missing
    --cov-report=html
```

### Frontend Configuration (`frontend/vitest.config.ts`)

```typescript
export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html']
    }
  }
})
```

## 📊 Coverage Reports

### Generate Coverage Reports

**Full coverage (backend + frontend):**
```bash
./run_tests.sh
```

**Backend coverage only:**
```bash
cd backend
python3 -m pytest tests/ --cov=app --cov-report=html
```

**Frontend coverage only:**
```bash
cd frontend
npm run test:coverage
```

### View Coverage Reports

- **Backend:** Open `backend/htmlcov/index.html`
- **Frontend:** Open `frontend/coverage/index.html`

## 🎯 Test Scenarios Covered

### 1. Search Functionality
- ✅ Valid search queries
- ✅ Empty and invalid queries
- ✅ Search with filters
- ✅ Pagination and limits
- ✅ Search result ranking
- ✅ Processing time tracking

### 2. Case Management
- ✅ Individual case retrieval
- ✅ Case metadata validation
- ✅ Non-existent case handling
- ✅ Case content formatting

### 3. Filter System
- ✅ Filter option loading
- ✅ Dynamic filter application
- ✅ Multiple filter combinations
- ✅ Filter validation

### 4. System Health
- ✅ Health check endpoints
- ✅ Database connectivity
- ✅ Service availability
- ✅ Performance monitoring

### 5. Error Handling
- ✅ Network errors
- ✅ Service timeouts
- ✅ Invalid input validation
- ✅ Graceful degradation

### 6. User Interface
- ✅ Component rendering
- ✅ User interactions
- ✅ Form submissions
- ✅ Navigation and routing
- ✅ Responsive design
- ✅ Accessibility (ARIA labels, keyboard navigation)

### 7. Performance
- ✅ Concurrent request handling
- ✅ Large result sets
- ✅ Memory usage
- ✅ Response time monitoring

## 🛠 Running Specific Test Suites

### Run tests by pattern:
```bash
# Backend: Run only API tests
cd backend
python3 -m pytest tests/test_api.py -v

# Backend: Run only integration tests
python3 -m pytest tests/test_integration.py -v

# Frontend: Run only component tests
cd frontend
npm run test -- components

# Frontend: Run only page tests
npm run test -- pages
```

### Run tests with specific markers:
```bash
# Run only integration tests
python3 -m pytest -m integration

# Run only API tests
python3 -m pytest -m api

# Run only end-to-end tests
python3 -m pytest -m e2e
```

## 🔍 Debugging Tests

### Backend Debug Mode
```bash
cd backend
python3 -m pytest tests/ -v -s --tb=long
```

### Frontend Debug Mode
```bash
cd frontend
npm run test:ui  # Opens Vitest UI for interactive debugging
```

### Enable verbose logging:
```bash
./run_tests.sh --verbose
```

## 🚨 Continuous Integration

### GitHub Actions / CI Pipeline

Add this to `.github/workflows/test.yml`:

```yaml
name: Test Suite
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Run tests
        run: ./run_tests.sh
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## 📝 Writing New Tests

### Backend Test Example
```python
@pytest.mark.asyncio
async def test_search_endpoint(async_client, mock_search_service):
    """Test search endpoint functionality."""
    with patch('app.api.routes.advanced_search_service', mock_search_service):
        response = await async_client.post("/api/search", json={
            "query": "test query"
        })
        
    assert response.status_code == 200
    assert "results" in response.json()
```

### Frontend Test Example
```typescript
it('renders search form', () => {
  render(<SearchForm onSubmit={vi.fn()} />)
  
  expect(screen.getByPlaceholderText(/search/i)).toBeInTheDocument()
  expect(screen.getByRole('button', { name: /search/i })).toBeInTheDocument()
})
```

## 🔧 Test Utilities

### Backend Fixtures (`conftest.py`)
- `async_client`: HTTP client for API testing
- `mock_search_service`: Mocked search service
- `sample_search_request`: Sample request data
- `sample_legal_case`: Sample case data

### Frontend Utilities (`test/utils.tsx`)
- `render`: Custom render with providers
- `createMockSearchResult`: Generate mock search results
- `createMockLegalCase`: Generate mock case data
- `waitForLoadingToFinish`: Async operation helper

## 📋 Test Checklist

Before deploying, ensure all tests pass:

- [ ] ✅ All API endpoints respond correctly
- [ ] ✅ Search functionality works with various queries
- [ ] ✅ Filters can be applied and removed
- [ ] ✅ Case details load properly
- [ ] ✅ Error handling works gracefully
- [ ] ✅ UI components render correctly
- [ ] ✅ User interactions work as expected
- [ ] ✅ Accessibility requirements are met
- [ ] ✅ Performance benchmarks are met
- [ ] ✅ Coverage targets are achieved (>80%)

## 🤝 Contributing

When adding new features:

1. **Write tests first** (TDD approach)
2. **Test both happy path and edge cases**
3. **Update existing tests** if changing functionality
4. **Add integration tests** for new API endpoints
5. **Test accessibility** for new UI components
6. **Verify coverage** doesn't decrease

## 🆘 Troubleshooting

### Common Issues

**Tests fail due to missing dependencies:**
```bash
# Backend
cd backend && pip install -r requirements.txt

# Frontend
cd frontend && npm install
```

**Port conflicts:**
```bash
# Kill processes on test ports
lsof -ti:8000 | xargs kill -9  # Backend test port
lsof -ti:3000 | xargs kill -9  # Frontend test port
```

**Database connection issues:**
```bash
# Check if Qdrant is running
docker ps | grep qdrant

# Start Qdrant if needed
docker run -p 6333:6333 qdrant/qdrant
```

**Coverage reports not generating:**
```bash
# Install coverage dependencies
pip install pytest-cov  # Backend
npm install @vitest/coverage-v8  # Frontend
```

## 📞 Support

For test-related issues:
1. Check this documentation first
2. Review test logs for specific error messages
3. Ensure all dependencies are installed
4. Verify environment configuration
5. Run tests in isolation to identify issues

Happy testing! 🎉 