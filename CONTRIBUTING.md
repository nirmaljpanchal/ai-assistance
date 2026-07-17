# Contributing Guidelines

## Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git

### Backend Development
```bash
cd backend
uv venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
uv pip install -e ".[dev]"
pre-commit install
```

### Frontend Development
```bash
cd frontend
npm install
npm start
```

### Running Tests
```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test

# Evaluations
cd evals
pytest test_ai_response.py
```

### Code Style & Quality
- **Python**: Ruff (linting + formatting), MyPy (type checking), Pytest (testing)
- **JavaScript**: Prettier, ESLint
- **Pre-commit hooks**: Automatically run on `git commit` (see .pre-commit-config.yaml)

Run formatters before committing:
```bash
# Backend (or let pre-commit handle it)
cd backend
ruff format .
ruff check . --fix
mypy .
pytest
```

## Git Workflow
1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Run tests locally
4. Commit with clear messages
5. Push and create a Pull Request

## PR Guidelines
- Provide a clear description of changes
- Link related issues
- Ensure CI/CD passes
- Request review from maintainers

## Commit Message Format
```
<type>: <subject>

<body>

<footer>
```

Types: feat, fix, docs, style, refactor, test, chore

## Questions?
Open an issue or contact the maintainers.
