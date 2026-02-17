# AI-DOS Quick Start Guide

Get AI-DOS up and running in 5 minutes!

## Prerequisites

- **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
- **8GB RAM** minimum (16GB recommended)
- **10GB free disk space**

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-org/ai-dos.git
cd ai-dos
```

### Step 2: Run Setup Script

**Windows:**
```bash
scripts\setup.bat
```

**Linux/Mac:**
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### Step 3: Start AI-DOS

```bash
docker-compose up -d
```

Wait 30-60 seconds for all services to start.

### Step 4: Verify Installation

```bash
docker-compose ps
```

All services should show "Up" status.

## First Steps

### 1. Access the API Gateway

Open your browser and go to:
```
http://localhost:8000
```

You should see the AI-DOS welcome page.

### 2. Explore API Documentation

Interactive API docs are available at:
```
http://localhost:8000/docs
```

### 3. Create Your First User

**Using the API:**

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "demo_user",
    "email": "demo@example.com",
    "password": "secure_password",
    "full_name": "Demo User"
  }'
```

**Using Python:**

```python
import requests

response = requests.post(
    "http://localhost:8000/auth/register",
    json={
        "username": "demo_user",
        "email": "demo@example.com",
        "password": "secure_password",
        "full_name": "Demo User"
    }
)
print(response.json())
```

### 4. Login and Get Access Token

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "demo_user",
    "password": "secure_password"
  }'
```

Save the `access_token` from the response.

### 5. Create Your First Dataset

```python
import requests

token = "YOUR_ACCESS_TOKEN"
headers = {"Authorization": f"Bearer {token}"}

response = requests.post(
    "http://localhost:8001/datasets",
    headers=headers,
    json={
        "name": "My First Dataset",
        "description": "A sample dataset for testing",
        "owner_id": "demo_user",
        "data_type": "image",
        "tags": ["test", "demo"]
    }
)
print(response.json())
```

### 6. Create an Experiment

```python
response = requests.post(
    "http://localhost:8002/experiments",
    headers=headers,
    json={
        "name": "My First Experiment",
        "description": "Testing model training",
        "project_id": "project_1",
        "user_id": "demo_user",
        "tags": ["classification", "resnet"]
    }
)
print(response.json())
```

### 7. Track a Training Run

```python
experiment_id = "YOUR_EXPERIMENT_ID"

response = requests.post(
    f"http://localhost:8002/experiments/{experiment_id}/runs",
    headers=headers,
    json={
        "name": "Run 1",
        "parameters": {
            "learning_rate": 0.001,
            "batch_size": 32,
            "epochs": 10
        }
    }
)
run = response.json()
run_id = run["id"]

# Log metrics during training
for epoch in range(10):
    requests.post(
        f"http://localhost:8002/runs/{run_id}/log-metrics",
        headers=headers,
        json={
            "step": epoch,
            "metrics": {
                "loss": 0.5 - (epoch * 0.04),
                "accuracy": 0.6 + (epoch * 0.03)
            }
        }
    )

# Complete the run
requests.put(
    f"http://localhost:8002/runs/{run_id}/complete",
    headers=headers,
    json={
        "loss": 0.15,
        "accuracy": 0.92
    }
)
```

## Access Other Services

### Grafana (Monitoring)
```
URL: http://localhost:3000
Username: admin
Password: admin
```

### MinIO (Object Storage)
```
URL: http://localhost:9001
Username: aidos
Password: aidos_dev_password
```

### RabbitMQ (Message Queue)
```
URL: http://localhost:15672
Username: aidos
Password: aidos_dev_password
```

## Common Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f dataforge
```

### Restart a Service
```bash
docker-compose restart dataforge
```

### Stop AI-DOS
```bash
docker-compose down
```

### Stop and Remove All Data
```bash
docker-compose down -v
```

### Rebuild Services
```bash
docker-compose build
docker-compose up -d
```

## Example Workflows

### Complete ML Pipeline

```python
import requests

BASE_URL = "http://localhost:8000"
token = "YOUR_ACCESS_TOKEN"
headers = {"Authorization": f"Bearer {token}"}

# 1. Create dataset
dataset = requests.post(
    f"{BASE_URL}:8001/datasets",
    headers=headers,
    json={
        "name": "CIFAR-10",
        "description": "Image classification dataset",
        "owner_id": "demo_user",
        "data_type": "image"
    }
).json()

# 2. Create experiment
experiment = requests.post(
    f"{BASE_URL}:8002/experiments",
    headers=headers,
    json={
        "name": "ResNet Training",
        "description": "Train ResNet-50 on CIFAR-10",
        "project_id": "project_1",
        "user_id": "demo_user"
    }
).json()

# 3. Run hyperparameter optimization
hp_job = requests.post(
    f"{BASE_URL}:8002/experiments/{experiment['id']}/hyperparameter-jobs",
    headers=headers,
    json={
        "search_space": {
            "learning_rate": [0.001, 0.01, 0.1],
            "batch_size": [16, 32, 64]
        },
        "search_method": "grid",
        "num_trials": 9
    }
).json()

# 4. Register best model
model = requests.post(
    f"{BASE_URL}:8002/models",
    headers=headers,
    json={
        "name": "ResNet-50-CIFAR10",
        "version": "1.0.0",
        "description": "ResNet-50 trained on CIFAR-10",
        "framework": "pytorch",
        "experiment_id": experiment['id'],
        "metrics": {"accuracy": 0.92, "loss": 0.15},
        "registry_path": "/models/resnet50_v1.pth",
        "created_by": "demo_user"
    }
).json()

print(f"Model registered: {model['id']}")
```

## Troubleshooting

### Services Won't Start

**Check Docker:**
```bash
docker --version
docker-compose --version
```

**Check logs:**
```bash
docker-compose logs
```

**Restart Docker Desktop** (Windows/Mac)

### Port Already in Use

Edit `docker-compose.yml` and change the port mapping:
```yaml
ports:
  - "8080:8000"  # Change 8000 to 8080
```

### Out of Memory

Increase Docker memory limit:
- Docker Desktop → Settings → Resources → Memory
- Set to at least 8GB

### Database Connection Errors

Wait for databases to be ready:
```bash
docker-compose logs postgres
docker-compose logs mongodb
```

Look for "database system is ready to accept connections"

## Next Steps

1. **Read the Documentation**: [docs/architecture.md](./docs/architecture.md)
2. **Explore Examples**: [examples/](./examples/)
3. **Join the Community**: [Discord](https://discord.gg/ai-dos)
4. **Contribute**: [CONTRIBUTING.md](./CONTRIBUTING.md)
5. **Deploy to Production**: [docs/deployment.md](./docs/deployment.md)

## Getting Help

- **Documentation**: [docs/](./docs/)
- **Discord**: https://discord.gg/ai-dos
- **GitHub Issues**: https://github.com/ai-dos/ai-dos/issues
- **Discussions**: https://github.com/ai-dos/ai-dos/discussions

## What's Next?

Now that you have AI-DOS running, you can:

- ✅ Create and manage datasets
- ✅ Track experiments and runs
- ✅ Register and version models
- ✅ Deploy models to production
- ✅ Monitor performance
- ✅ Collaborate with your team

**Happy building!** 🚀
