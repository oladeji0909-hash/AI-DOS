# AI-DOS Development Guide

## Getting Started

### Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose v2.0+
- Git
- Python 3.11+ (for local development)
- Node.js 18+ (for frontend development)
- 16GB RAM minimum (32GB recommended)
- 50GB free disk space

### Initial Setup

1. **Clone the repository**
```bash
git clone https://github.com/your-org/ai-dos.git
cd ai-dos
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Start the development environment**
```bash
docker-compose up -d
```

4. **Verify all services are running**
```bash
docker-compose ps
```

5. **Access the services**
- API Gateway: http://localhost:8000
- DataForge: http://localhost:8001
- ModelHub: http://localhost:8002
- Grafana: http://localhost:3000
- MinIO Console: http://localhost:9001
- RabbitMQ Management: http://localhost:15672

### Development Workflow

#### Working on a Service

1. **Navigate to the service directory**
```bash
cd services/dataforge
```

2. **Install dependencies locally (optional, for IDE support)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Make your changes**
The service will auto-reload thanks to volume mounting in docker-compose.yml

4. **Test your changes**
```bash
# Run unit tests
pytest tests/

# Run integration tests
pytest tests/integration/
```

5. **Check code quality**
```bash
# Format code
black .
isort .

# Lint code
flake8 .
pylint **/*.py

# Type checking
mypy .
```

#### Adding a New Endpoint

1. Define your Pydantic models
2. Implement the endpoint function
3. Add route to the FastAPI app
4. Write tests
5. Update API documentation
6. Test manually using Swagger UI at http://localhost:800X/docs

#### Database Migrations

We use Alembic for database migrations:

```bash
# Create a new migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Testing

#### Unit Tests

```bash
# Run all unit tests
pytest tests/unit/

# Run specific test file
pytest tests/unit/test_dataforge.py

# Run with coverage
pytest --cov=services --cov-report=html
```

#### Integration Tests

```bash
# Start test environment
docker-compose -f docker-compose.test.yml up -d

# Run integration tests
pytest tests/integration/

# Cleanup
docker-compose -f docker-compose.test.yml down -v
```

#### End-to-End Tests

```bash
# Run E2E tests
pytest tests/e2e/

# Run specific scenario
pytest tests/e2e/test_training_pipeline.py
```

### Code Style Guide

#### Python

- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use docstrings for all public functions/classes
- Prefer composition over inheritance
- Keep functions small and focused

Example:
```python
from typing import List, Optional
from pydantic import BaseModel

class Dataset(BaseModel):
    """Represents a dataset in the system.
    
    Attributes:
        id: Unique identifier
        name: Human-readable name
        owner_id: ID of the user who owns this dataset
    """
    id: Optional[str] = None
    name: str
    owner_id: str
    
def create_dataset(dataset: Dataset) -> Dataset:
    """Create a new dataset.
    
    Args:
        dataset: Dataset object to create
        
    Returns:
        Created dataset with generated ID
        
    Raises:
        ValueError: If dataset name is invalid
    """
    # Implementation
    pass
```

#### TypeScript/JavaScript

- Use TypeScript for all new code
- Follow Airbnb style guide
- Use functional components with hooks
- Prefer async/await over promises
- Use meaningful variable names

#### Go

- Follow official Go style guide
- Use gofmt for formatting
- Write table-driven tests
- Handle all errors explicitly
- Use context for cancellation

### Debugging

#### Debugging a Service

1. **View logs**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f dataforge
```

2. **Attach debugger**
```bash
# Add to docker-compose.yml
ports:
  - "5678:5678"  # debugpy port

# In your code
import debugpy
debugpy.listen(("0.0.0.0", 5678))
debugpy.wait_for_client()
```

3. **Interactive shell**
```bash
docker-compose exec dataforge python
```

#### Common Issues

**Service won't start**
- Check logs: `docker-compose logs service-name`
- Verify dependencies are running
- Check port conflicts
- Ensure environment variables are set

**Database connection errors**
- Wait for database to be ready (add health checks)
- Verify connection string
- Check network connectivity

**Import errors**
- Rebuild container: `docker-compose build service-name`
- Clear Python cache: `find . -type d -name __pycache__ -exec rm -r {} +`

### Performance Optimization

#### Profiling

```python
# Add profiling to endpoint
from fastapi import Request
import time

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

#### Caching

```python
from functools import lru_cache
import redis

# In-memory cache
@lru_cache(maxsize=128)
def expensive_computation(param: str) -> str:
    # Computation
    pass

# Redis cache
redis_client = redis.Redis(host='redis', port=6379)

def get_cached(key: str) -> Optional[str]:
    return redis_client.get(key)

def set_cached(key: str, value: str, ttl: int = 3600):
    redis_client.setex(key, ttl, value)
```

### Security Best Practices

1. **Never commit secrets**
   - Use environment variables
   - Use .env files (add to .gitignore)
   - Use secrets management (Vault)

2. **Validate all inputs**
   - Use Pydantic models
   - Sanitize user input
   - Validate file uploads

3. **Use HTTPS in production**
   - Configure SSL certificates
   - Redirect HTTP to HTTPS
   - Use HSTS headers

4. **Implement rate limiting**
   - Per user/IP
   - Per endpoint
   - Use Redis for distributed rate limiting

5. **Audit logging**
   - Log all authentication attempts
   - Log data access
   - Log configuration changes

### Monitoring and Observability

#### Metrics

```python
from prometheus_client import Counter, Histogram

# Define metrics
request_count = Counter('http_requests_total', 'Total HTTP requests')
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')

# Use in endpoint
@app.get("/data")
def get_data():
    request_count.inc()
    with request_duration.time():
        # Process request
        pass
```

#### Logging

```python
import logging
import structlog

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)

logger = structlog.get_logger()

# Use in code
logger.info("dataset_created", dataset_id=dataset.id, user_id=user.id)
logger.error("database_error", error=str(e), query=query)
```

#### Tracing

```python
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Initialize tracing
tracer = trace.get_tracer(__name__)

# Instrument FastAPI
FastAPIInstrumentor.instrument_app(app)

# Add custom spans
with tracer.start_as_current_span("process_dataset"):
    # Processing logic
    pass
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Write/update tests
5. Ensure all tests pass
6. Update documentation
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

### Pull Request Guidelines

- Write clear, descriptive commit messages
- Reference related issues
- Include tests for new features
- Update documentation
- Ensure CI passes
- Request review from maintainers
- Address review feedback promptly

### Release Process

1. Update version numbers
2. Update CHANGELOG.md
3. Create release branch
4. Run full test suite
5. Build and tag Docker images
6. Create GitHub release
7. Deploy to staging
8. Run smoke tests
9. Deploy to production
10. Monitor for issues

### Useful Commands

```bash
# Rebuild all services
docker-compose build

# Rebuild specific service
docker-compose build dataforge

# View resource usage
docker stats

# Clean up everything
docker-compose down -v
docker system prune -a

# Database backup
docker-compose exec postgres pg_dump -U aidos aidos > backup.sql

# Database restore
docker-compose exec -T postgres psql -U aidos aidos < backup.sql

# Run migrations
docker-compose exec dataforge alembic upgrade head

# Generate API client
docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate \
  -i /local/openapi.json \
  -g python \
  -o /local/client
```

### Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Python Best Practices](https://docs.python-guide.org/)

### Getting Help

- Check existing issues on GitHub
- Join our Discord community
- Read the documentation
- Ask in discussions forum
- Contact maintainers

---

Happy coding! 🚀
