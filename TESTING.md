# Testing Guide for SkinVision AI

This document provides comprehensive information about testing the SkinVision AI application.

## 📋 Test Structure

### Backend Tests
- **Location**: `backend/tests/`
- **Framework**: pytest
- **Coverage Target**: 70%+

#### Test Categories:
1. **Unit Tests** (`test_unit_*.py`, `test_crud_*.py`, `test_auth_*.py`, `test_ml_*.py`)
   - Individual function testing
   - CRUD operations
   - Authentication utilities
   - ML/Grad-CAM functions

2. **Integration Tests** (`test_integration_*.py`, `test_*_integration.py`)
   - Full API workflows
   - End-to-end user flows
   - Authentication flows
   - Prediction to history workflow

3. **Smoke Tests** (`test_app_smoke.py`)
   - Basic health checks
   - API availability

### Frontend Tests
- **Location**: `frontend/src/__tests__/`
- **Framework**: Vitest + React Testing Library
- **Coverage Target**: 70%+

#### Test Categories:
1. **Component Tests**
   - Individual component rendering
   - User interactions
   - Props handling

2. **Page Tests**
   - Full page rendering
   - Navigation
   - API integration

3. **Integration Tests** (`integration/`)
   - Complete user flows
   - Cross-component interactions

## 🚀 Running Tests

### Backend Tests

#### Run all tests:
```bash
cd backend
pytest
```

#### Run with coverage:
```bash
cd backend
pytest --cov=app --cov-report=html --cov-report=term
```

#### Run specific test file:
```bash
pytest tests/test_predict_comprehensive.py
```

#### Run specific test:
```bash
pytest tests/test_predict_comprehensive.py::test_predict_without_authentication
```

#### Run with markers:
```bash
pytest -m unit          # Only unit tests
pytest -m integration   # Only integration tests
pytest -m "not slow"    # Skip slow tests
```

#### Run in verbose mode:
```bash
pytest -v
```

### Frontend Tests

#### Run all tests:
```bash
cd frontend
npm test
```

#### Run in watch mode:
```bash
npm run test:watch
```

#### Run with coverage:
```bash
npm run test:coverage
```

#### Run specific test file:
```bash
npm test -- Upload.test.jsx
```

#### Run with UI:
```bash
npm run test:ui
```

## 📊 Test Coverage

### View Coverage Reports

**Backend:**
- HTML report: `backend/htmlcov/index.html`
- Terminal output: Shown after running `pytest --cov`

**Frontend:**
- Coverage folder: `frontend/coverage/`
- Open `frontend/coverage/index.html` in browser

### Coverage Targets

- **Overall**: 70%+
- **Critical paths**: 85%+
- **New code**: 80%+

## 🧪 Test Examples

### Backend: Testing API Endpoint

```python
def test_predict_endpoint(client):
    img_bytes = create_test_image()
    files = {"file": ("test.png", img_bytes, "image/png")}
    
    response = client.post("/predict", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert "predicted_class" in data
    assert "confidence" in data
```

### Frontend: Testing Component

```jsx
it('renders component correctly', () => {
  render(<MyComponent prop="value" />)
  expect(screen.getByText('Expected Text')).toBeInTheDocument()
})
```

### Frontend: Testing User Interaction

```jsx
it('handles button click', () => {
  const mockFn = vi.fn()
  render(<Button onClick={mockFn} />)
  
  fireEvent.click(screen.getByRole('button'))
  expect(mockFn).toHaveBeenCalled()
})
```

## 🔧 Test Configuration

### Backend (pytest.ini)

- Test discovery pattern: `test_*.py`
- Coverage source: `app/`
- Minimum coverage: 70%
- Output formats: HTML, XML, Terminal

### Frontend (vite.config.js)

- Test environment: jsdom
- Coverage provider: v8
- Setup file: `src/setupTests.js`

## 🐛 Debugging Tests

### Backend

**Show print statements:**
```bash
pytest -s
```

**Stop on first failure:**
```bash
pytest -x
```

**Drop into debugger on failure:**
```bash
pytest --pdb
```

### Frontend

**Debug specific test:**
```jsx
// Add in test
console.log(screen.debug())
```

**Run single test file:**
```bash
npm test -- Upload.test.jsx
```

## 🔄 CI/CD Integration

Tests run automatically on:
- Push to `main` or `develop` branches
- Pull requests

See `.github/workflows/tests.yml` for configuration.

## 📝 Writing New Tests

### Backend Test Template

```python
def test_feature_name(db_session):  # or client
    # Arrange
    setup_data = create_test_data()
    
    # Act
    result = function_to_test(setup_data)
    
    # Assert
    assert result.expected_property == expected_value
```

### Frontend Test Template

```jsx
describe('ComponentName', () => {
  it('does something', () => {
    // Arrange
    render(<Component />)
    
    // Act
    fireEvent.click(screen.getByRole('button'))
    
    // Assert
    expect(screen.getByText('Expected')).toBeInTheDocument()
  })
})
```

## ✅ Test Checklist

Before committing:

- [ ] All existing tests pass
- [ ] New code has tests
- [ ] Coverage threshold met (70%+)
- [ ] Integration tests cover main flows
- [ ] Edge cases are tested
- [ ] Error handling is tested
- [ ] Tests are fast (< 1 min total)

## 🚨 Common Issues

### Backend

**Issue**: Database connection errors
**Solution**: Ensure test database is configured correctly in `conftest.py`

**Issue**: Import errors
**Solution**: Run from `backend/` directory or use `PYTHONPATH`

### Frontend

**Issue**: `vi is not defined`
**Solution**: Import from vitest: `import { vi } from 'vitest'`

**Issue**: Mock not working
**Solution**: Clear mocks in `beforeEach`: `vi.clearAllMocks()`

**Issue**: Router errors
**Solution**: Wrap component in `<MemoryRouter>` or `<BrowserRouter>`

## 📚 Additional Resources

- [pytest documentation](https://docs.pytest.org/)
- [Vitest documentation](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

## 🎯 Test Priorities

**High Priority:**
- Authentication flows
- Prediction endpoints
- Critical user flows
- Error handling

**Medium Priority:**
- UI component rendering
- Form validations
- Navigation flows

**Low Priority:**
- Static content
- Styling
- Non-critical features

---

For questions or issues, please open a GitHub issue or contact the development team.
