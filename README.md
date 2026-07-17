# AI Assistance Platform

A monorepo for building an enterprise-grade AI assistance platform.

## Project Structure

```
.
├── backend/              # FastAPI application
├── frontend/             # React application
├── infra/
│   ├── terraform/        # Infrastructure as Code
│   └── k8s/              # Kubernetes manifests (Helm/Kustomize)
├── evals/                # Ragas/DeepEval evaluation suites
├── docker/               # Docker configuration
├── .github/workflows/    # CI/CD pipelines
└── enterprise-ai-assistant-platform-plan.md
```

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Terraform
- kubectl & Helm (optional, for k8s deployment)
- `uv` package manager ([install](https://docs.astral.sh/uv/getting-started/installation/))
- `pre-commit` hooks

### Development Setup

**Backend (with uv):**
```bash
cd backend
uv venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
uv pip install -e ".[dev]"
pre-commit install
```

**Frontend:**
```bash
cd frontend
npm install
```

### Running Locally

**Using Docker Compose (recommended):**
```bash
docker-compose -f docker/compose.yml up
```

**Or run separately:**
```bash
# Terminal 1: Backend
cd backend
source .venv/bin/activate
uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend
npm start
```

### Code Quality

**Run tests:**
```bash
cd backend
pytest                  # Run all tests
pytest -v             # Verbose output
pytest --cov          # With coverage report
```

**Run linters:**
```bash
cd backend
ruff check .
mypy .
```

**Format code:**
```bash
cd backend
ruff format .
ruff check . --fix
```

**Pre-commit hooks (automatic on git commit):**
- Ruff formatting and linting
- MyPy type checking
- Pytest unit tests
- Trailing whitespace & other checks

## Phase 0: Skeleton Setup
- [x] Monorepo layout
- [ ] Backend initialization (FastAPI)
- [ ] Frontend initialization (React)
- [ ] Docker Compose setup
- [ ] CI/CD GitHub Actions
- [ ] Terraform base configuration
- [ ] Evaluation framework setup
