# 🚀 Getting Started with AI-DOS

Welcome to AI-DOS! This guide will get you up and running in 5 minutes.

---

## 📋 Prerequisites

Before you start, make sure you have:

- ✅ **Docker Desktop** installed ([Download here](https://www.docker.com/products/docker-desktop))
- ✅ **Git** installed ([Download here](https://git-scm.com/downloads))
- ✅ **Python 3.8+** (optional, for SDK/CLI) ([Download here](https://www.python.org/downloads/))
- ✅ **8GB+ RAM** (for running all services)
- ✅ **Ports 8000-8008 available** (for the 9 services)

---

## ⚡ Quick Start (5 Minutes)

### Step 1: Clone the Repository

```bash
git clone https://github.com/oladeji0909-hash/AI-DOS.git
cd AI-DOS
```

### Step 2: Start All Services

```bash
docker-compose -f docker-compose-minimal.yml up -d
```

This starts:
- 9 microservices (API Gateway, DataForge, ModelHub, Magic Mode, Marketplace, Deploy, Collaboration, AutoScale, Analytics)
- 5 databases (PostgreSQL, MongoDB, Redis, MinIO, RabbitMQ)

**Wait 60 seconds** for all services to start.

### Step 3: Verify Everything is Running

```bash
docker-compose -f docker-compose-minimal.yml ps
```

You should see all containers with status "Up".

### Step 4: Access the Platform

**Web Dashboards:**
- Landing Page: Open `frontend/dashboard/index.html` in your browser
- Marketplace: Open `frontend/marketplace/index.html`
- Monitoring: Open `frontend/monitoring/index.html`

**API Documentation (Swagger UI):**
- API Gateway: http://localhost:8000/docs
- DataForge: http://localhost:8001/docs
- ModelHub: http://localhost:8002/docs
- Magic Mode: http://localhost:8003/docs
- Marketplace: http://localhost:8004/docs
- Deploy: http://localhost:8005/docs
- Collaboration: http://localhost:8006/docs
- AutoScale: http://localhost:8007/docs
- Analytics: http://localhost:8008/docs

---

## 🎯 Your First ML Pipeline

Let's create your first ML pipeline using Magic Mode!

### Option 1: Using the Web Dashboard

1. Open `frontend/dashboard/index.html`
2. Scroll to the Magic Mode section
3. Type: `"Build a sentiment analyzer for product reviews"`
4. Click "Create Pipeline"
5. Watch it create dataset, experiment, and API endpoint!

### Option 2: Using Python SDK

```bash
# Install SDK
cd sdk/python
pip install -e .
```

```python
from aidos import magic

# Create ML pipeline with one line
result = magic("Build a sentiment analyzer for product reviews")

print(f"Dataset ID: {result['dataset_id']}")
print(f"Experiment ID: {result['experiment_id']}")
print(f"API Endpoint: {result['api_endpoint']}")
```

### Option 3: Using CLI

```bash
# Install CLI
cd sdk/python
pip install -e .

# Create pipeline
aidos magic "Build a sentiment analyzer for product reviews"
```

---

## 📚 Using Each Service

### 1. DataForge - Dataset Management

**Create a Dataset:**

```python
from aidos import DataForge

df = DataForge()
dataset = df.create_dataset(
    name="Customer Reviews",
    description="Product reviews from e-commerce site",
    data_type="text"
)
print(f"Dataset created: {dataset['id']}")
```

**CLI:**
```bash
aidos dataset create "Customer Reviews" --type text
aidos dataset list
```

**API:**
```bash
curl -X POST http://localhost:8001/datasets/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Customer Reviews","description":"Product reviews","data_type":"text"}'
```

---

### 2. ModelHub - Experiment Tracking

**Create an Experiment:**

```python
from aidos import ModelHub

mh = ModelHub()
experiment = mh.create_experiment(
    name="Sentiment Model v1",
    description="BERT-based sentiment classifier",
    project_id="proj_001",
    user_id="user_001"
)
print(f"Experiment created: {experiment['id']}")
```

**CLI:**
```bash
aidos experiment create "Sentiment Model v1" --project proj_001
aidos experiment list
```

**API:**
```bash
curl -X POST http://localhost:8002/experiments \
  -H "Content-Type: application/json" \
  -d '{"name":"Sentiment Model v1","description":"BERT classifier","project_id":"proj_001","user_id":"user_001"}'
```

---

### 3. Magic Mode - Natural Language ML

**Create Pipeline:**

```python
from aidos import magic

result = magic("Build an image classifier for cats vs dogs")
print(result)
```

**CLI:**
```bash
aidos magic "Build an image classifier for cats vs dogs"
```

**API:**
```bash
curl -X POST http://localhost:8003/magic/create \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Build an image classifier for cats vs dogs"}'
```

---

### 4. Marketplace - Buy/Sell Models

**Browse Models:**

```python
from aidos import AIDOS

client = AIDOS()
models = client.get("http://localhost:8004/marketplace/models")
print(models.json())
```

**CLI:**
```bash
# View in browser
# Open frontend/marketplace/index.html
```

**API:**
```bash
curl http://localhost:8004/marketplace/models
```

---

### 5. Deploy - Production Deployment

**Deploy a Model:**

```python
from aidos import Deploy

deploy = Deploy()
deployment = deploy.create(
    experiment_id="exp_123",
    name="Sentiment API",
    description="Production sentiment analysis"
)
print(f"Deployed at: {deployment['endpoint_url']}")
```

**CLI:**
```bash
aidos deploy create exp_123 "Sentiment API"
aidos deploy list
aidos deploy metrics deploy_123
```

**API:**
```bash
curl -X POST http://localhost:8005/deploy/create \
  -H "Content-Type: application/json" \
  -d '{"experiment_id":"exp_123","name":"Sentiment API"}'
```

---

### 6. Collaboration - Team Workflows

**Create a Team:**

```python
from aidos import Collab

collab = Collab()
team = collab.create_team(
    name="ML Research Team",
    description="Building sentiment models",
    owner_id="user_001"
)
print(f"Team created: {team['id']}")
```

**Share an Experiment:**

```python
collab.share(
    resource_type="experiment",
    resource_id="exp_123",
    owner_id="user_001",
    shared_with="user_002",
    permission="editor",
    message="Check out this model!"
)
```

**CLI:**
```bash
aidos team create "ML Research Team" --description "Building models"
aidos share experiment exp_123 user_002 --role editor
```

---

### 7. AutoScale - Smart Scaling

**Create Scaling Rule:**

```python
from aidos import AutoScale

autoscale = AutoScale()
rule = autoscale.create_rule(
    deployment_id="deploy_123",
    name="CPU-based scaling",
    metric="cpu",
    min_instances=1,
    max_instances=10,
    scale_up_threshold=70,
    scale_down_threshold=30
)
print(f"Scaling rule created: {rule['id']}")
```

**Check Cost Savings:**

```python
cost = autoscale.get_cost("deploy_123")
print(f"Savings: ${cost['savings']} ({cost['savings_percent']}%)")
```

**CLI:**
```bash
aidos autoscale create deploy_123 --min 1 --max 10 --up 70 --down 30
aidos autoscale cost deploy_123
```

---

### 8. Analytics - Business Intelligence

**View Dashboard:**

```python
from aidos import Analytics

analytics = Analytics()
dashboard = analytics.get_dashboard()
print(f"Total Models: {dashboard['total_models']}")
print(f"Total Revenue: ${dashboard['total_revenue']}")
print(f"ROI: {dashboard['avg_model_accuracy']}")
```

**Calculate ROI:**

```python
roi = analytics.calculate_roi()
print(f"ROI: {roi['roi_percent']}%")
print(f"Net Profit: ${roi['net_profit']}")
```

**CLI:**
```bash
aidos analytics dashboard
aidos analytics roi
aidos analytics model model_123
```

---

## 🔧 Complete Workflow Example

Here's a complete workflow from dataset to deployment:

```python
from aidos import DataForge, ModelHub, Deploy, Analytics

# 1. Create dataset
df = DataForge()
dataset = df.create_dataset(
    name="Product Reviews",
    description="Customer feedback",
    data_type="text"
)

# 2. Create experiment
mh = ModelHub()
experiment = mh.create_experiment(
    name="Sentiment Classifier",
    description="BERT model",
    project_id="proj_001",
    user_id="user_001"
)

# 3. Deploy model
deploy = Deploy()
deployment = deploy.create(
    experiment_id=experiment['id'],
    name="Sentiment API"
)

# 4. Check analytics
analytics = Analytics()
performance = analytics.get_model_performance(deployment['deployment_id'])
print(f"Model accuracy: {performance['accuracy']}")

print(f"✅ Complete! API: {deployment['endpoint_url']}")
```

---

## 🛠️ Troubleshooting

### Services Not Starting

**Problem:** Docker containers fail to start

**Solution:**
```bash
# Check Docker is running
docker --version

# Check logs
docker-compose -f docker-compose-minimal.yml logs

# Restart services
docker-compose -f docker-compose-minimal.yml down
docker-compose -f docker-compose-minimal.yml up -d
```

---

### Port Already in Use

**Problem:** Error: "port is already allocated"

**Solution:**
```bash
# Check what's using the port
# Windows:
netstat -ano | findstr :8000

# Stop the process or change AI-DOS ports in docker-compose-minimal.yml
```

---

### Services Show as Unhealthy

**Problem:** Monitoring dashboard shows red status

**Solution:**
```bash
# Wait 60 seconds after starting
# Services need time to initialize

# Check specific service
curl http://localhost:8001/health

# Restart specific service
docker-compose -f docker-compose-minimal.yml restart dataforge
```

---

### SDK Import Error

**Problem:** `ModuleNotFoundError: No module named 'aidos'`

**Solution:**
```bash
cd sdk/python
pip install -e .

# Or install in development mode
pip install --editable .
```

---

### CORS Errors in Browser

**Problem:** Browser console shows CORS errors

**Solution:**
- All services have CORS enabled
- Make sure you're opening HTML files directly (file://)
- Or use a local server:
```bash
cd frontend/dashboard
python -m http.server 3000
# Visit http://localhost:3000
```

---

## 📖 Next Steps

Now that you're set up, explore:

1. **📚 [API Reference](docs/api-reference.md)** - Detailed API documentation
2. **🐍 [Python SDK Guide](sdk/python/README.md)** - Full SDK documentation
3. **💻 [CLI Reference](docs/cli-reference.md)** - All CLI commands
4. **🏗️ [Architecture Guide](docs/architecture.md)** - How AI-DOS works
5. **🤝 [Contributing Guide](CONTRIBUTING.md)** - Help build AI-DOS

---

## 💡 Tips & Best Practices

### Performance Tips

1. **Allocate enough RAM** - Docker needs 8GB+ for all services
2. **Use SSD** - Faster disk = faster services
3. **Close unused services** - Stop services you're not using:
   ```bash
   docker-compose -f docker-compose-minimal.yml stop marketplace
   ```

### Development Tips

1. **Use the SDK** - Easier than raw API calls
2. **Check logs** - When something fails:
   ```bash
   docker-compose -f docker-compose-minimal.yml logs -f magic
   ```
3. **Test with Swagger** - Use `/docs` endpoints to test APIs

### Production Tips

1. **Use environment variables** - Don't hardcode credentials
2. **Enable authentication** - Secure your APIs
3. **Monitor everything** - Use the monitoring dashboard
4. **Set up auto-scaling** - Save costs with AutoScale service

---

## 🎯 Common Use Cases

### Use Case 1: Experiment Tracking

```python
from aidos import ModelHub

mh = ModelHub()

# Create experiment
exp = mh.create_experiment("My Model", "Testing", "proj_1", "user_1")

# Track metrics
mh.log_metrics(exp['id'], {"accuracy": 0.95, "loss": 0.05})

# List all experiments
experiments = mh.list_experiments()
```

### Use Case 2: Team Collaboration

```python
from aidos import Collab

collab = Collab()

# Create team
team = collab.create_team("Data Science", "ML team", "user_1")

# Add member
collab.add_member(team['id'], "user_2", "editor")

# Share experiment
collab.share("experiment", "exp_123", "user_1", "user_2", "viewer")
```

### Use Case 3: Production Deployment

```python
from aidos import Deploy, AutoScale

# Deploy model
deploy = Deploy()
deployment = deploy.create("exp_123", "Production API")

# Set up auto-scaling
autoscale = AutoScale()
autoscale.create_rule(
    deployment['deployment_id'],
    "Auto scale",
    "cpu",
    min_instances=2,
    max_instances=20
)
```

---

## 🆘 Getting Help

Need help? Here's where to go:

- 💬 **Discord** - [Join our community](https://discord.gg/ai-dos)
- 🐛 **GitHub Issues** - [Report bugs](https://github.com/oladeji0909-hash/AI-DOS/issues)
- 📧 **Email** - team@ai-dos.io
- 📖 **Documentation** - Check other docs in `/docs`

---

## 🎉 You're Ready!

You now know how to:
- ✅ Install and run AI-DOS
- ✅ Use all 9 services
- ✅ Work with SDK and CLI
- ✅ Deploy models to production
- ✅ Troubleshoot common issues

**Start building amazing ML projects!** 🚀

---

<div align="center">

**[Back to README](README.md)** • **[API Reference](docs/api-reference.md)** • **[Contributing](CONTRIBUTING.md)**

Made with 🔥 by the AI-DOS community

</div>
