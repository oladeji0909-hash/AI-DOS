# Quick Reference Guide

Fast access to all AI-DOS commands and examples. 🚀

---

## 📋 Table of Contents

- [Installation](#-installation)
- [Magic Mode](#-magic-mode)
- [DataForge](#-dataforge)
- [ModelHub](#-modelhub)
- [Deploy](#-deploy)
- [Collaboration](#-collaboration)
- [AutoScale](#-autoscale)
- [Analytics](#-analytics)
- [Troubleshooting](#-troubleshooting)

---

## 🚀 Installation

### Docker (Recommended)
```bash
git clone https://github.com/oladeji0909-hash/AI-DOS.git
cd AI-DOS
docker-compose -f docker-compose-minimal.yml up -d
```

### Python SDK
```bash
cd sdk/python
pip install -e .
```

### Check Status
```bash
# CLI
aidos status

# Or visit
http://localhost:8000/docs  # API Gateway
```

---

## 🪄 Magic Mode

### Python SDK
```python
from aidos import magic

# One-line ML pipeline
result = magic("Build a sentiment analyzer for tweets")
print(result['api_endpoint'])
```

### CLI
```bash
# Create pipeline
aidos magic "Build a sentiment analyzer for tweets"

# With code display
aidos magic "Build image classifier" --show-code
```

### API
```bash
curl -X POST http://localhost:8003/magic/create \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Build a sentiment analyzer"}'
```

---

## 📦 DataForge

### Python SDK
```python
from aidos import DataForge

df = DataForge()

# Create dataset
dataset = df.create_dataset(
    name="Customer Reviews",
    description="Product reviews",
    data_type="text"
)

# List datasets
datasets = df.list_datasets()

# Get dataset
dataset = df.get_dataset("dataset_id")
```

### CLI
```bash
# Create dataset
aidos dataset create "Customer Reviews" --type text

# List datasets
aidos dataset list
```

### API
```bash
# Create
curl -X POST http://localhost:8001/datasets/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Reviews","description":"Customer feedback","data_type":"text"}'

# List
curl http://localhost:8001/datasets/
```

---

## 🧪 ModelHub

### Python SDK
```python
from aidos import ModelHub

mh = ModelHub()

# Create experiment
exp = mh.create_experiment(
    name="Sentiment Model v1",
    description="BERT classifier",
    project_id="proj_001",
    user_id="user_001"
)

# Log metrics
mh.log_metrics(exp['id'], {
    "accuracy": 0.95,
    "loss": 0.05
})

# List experiments
experiments = mh.list_experiments()
```

### CLI
```bash
# Create experiment
aidos experiment create "Sentiment Model v1" --project proj_001

# List experiments
aidos experiment list
```

### API
```bash
# Create
curl -X POST http://localhost:8002/experiments \
  -H "Content-Type: application/json" \
  -d '{"name":"Model v1","description":"Test","project_id":"proj_001","user_id":"user_001"}'

# List
curl http://localhost:8002/experiments/
```

---

## 🚀 Deploy

### Python SDK
```python
from aidos import Deploy

deploy = Deploy()

# Create deployment
deployment = deploy.create(
    experiment_id="exp_123",
    name="Sentiment API",
    description="Production API"
)
print(f"Endpoint: {deployment['endpoint_url']}")

# List deployments
deployments = deploy.list()

# Get metrics
metrics = deploy.get_metrics("deploy_123")

# Make prediction
result = deploy.predict("deploy_123", {"text": "Great product!"})
```

### CLI
```bash
# Create deployment
aidos deploy create exp_123 "Sentiment API"

# List deployments
aidos deploy list

# Get metrics
aidos deploy metrics deploy_123
```

### API
```bash
# Create
curl -X POST http://localhost:8005/deploy/create \
  -H "Content-Type: application/json" \
  -d '{"experiment_id":"exp_123","name":"Sentiment API"}'

# List
curl http://localhost:8005/deploy/list

# Predict
curl -X POST http://localhost:8005/deploy/deploy_123/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"Amazing!"}'
```

---

## 🤝 Collaboration

### Python SDK
```python
from aidos import Collab

collab = Collab()

# Create team
team = collab.create_team(
    name="ML Research Team",
    description="Building models",
    owner_id="user_001"
)

# Add member
collab.add_member(team['id'], "user_002", "editor")

# Share resource
collab.share(
    resource_type="experiment",
    resource_id="exp_123",
    owner_id="user_001",
    shared_with="user_002",
    permission="editor",
    message="Check this out!"
)

# Add comment
collab.comment("experiment", "exp_123", "user_002", "Great results!")

# Get notifications
notifications = collab.get_notifications("user_002")
```

### CLI
```bash
# Create team
aidos team create "ML Research Team" --description "Building models"

# Share resource
aidos share experiment exp_123 user_002 --role editor
```

### API
```bash
# Create team
curl -X POST http://localhost:8006/teams/create \
  -H "Content-Type: application/json" \
  -d '{"name":"ML Team","description":"Research","owner_id":"user_001"}'

# Share
curl -X POST http://localhost:8006/share \
  -H "Content-Type: application/json" \
  -d '{"resource_type":"experiment","resource_id":"exp_123","owner_id":"user_001","shared_with":"user_002","permission":"editor"}'
```

---

## ⚡ AutoScale

### Python SDK
```python
from aidos import AutoScale

autoscale = AutoScale()

# Create scaling rule
rule = autoscale.create_rule(
    deployment_id="deploy_123",
    name="CPU-based scaling",
    metric="cpu",
    min_instances=1,
    max_instances=10,
    scale_up_threshold=70,
    scale_down_threshold=30
)

# Check autoscale
result = autoscale.check("deploy_123")

# Get cost savings
cost = autoscale.get_cost("deploy_123")
print(f"Savings: ${cost['savings']}")

# List rules
rules = autoscale.list_rules("deploy_123")

# Get instances
instances = autoscale.get_instances("deploy_123")
```

### CLI
```bash
# Create rule
aidos autoscale create deploy_123 --min 1 --max 10 --up 70 --down 30

# Check cost
aidos autoscale cost deploy_123
```

### API
```bash
# Create rule
curl -X POST http://localhost:8007/autoscale/rules \
  -H "Content-Type: application/json" \
  -d '{"deployment_id":"deploy_123","name":"CPU scaling","metric":"cpu","min_instances":1,"max_instances":10,"scale_up_threshold":70,"scale_down_threshold":30}'

# Get cost
curl http://localhost:8007/autoscale/deploy_123/cost
```

---

## 📊 Analytics

### Python SDK
```python
from aidos import Analytics

analytics = Analytics()

# Dashboard summary
dashboard = analytics.get_dashboard()
print(f"Total Models: {dashboard['total_models']}")
print(f"Revenue: ${dashboard['total_revenue']}")

# Model performance
perf = analytics.get_model_performance("model_123", time_range="week")

# Compare experiments
comparison = analytics.compare_experiments(["exp_1", "exp_2", "exp_3"])

# Usage analytics
usage = analytics.get_usage_analytics(time_range="month")

# Cost analytics
cost = analytics.get_cost_analytics(time_range="month")

# Business metrics
business = analytics.get_business_overview(time_range="month")

# Calculate ROI
roi = analytics.calculate_roi()
print(f"ROI: {roi['roi_percent']}%")
print(f"Net Profit: ${roi['net_profit']}")
```

### CLI
```bash
# Dashboard
aidos analytics dashboard

# ROI
aidos analytics roi

# Model performance
aidos analytics model model_123
```

### API
```bash
# Dashboard
curl http://localhost:8008/analytics/dashboard

# ROI
curl http://localhost:8008/analytics/roi

# Model performance
curl http://localhost:8008/analytics/model/model_123/performance?time_range=week
```

---

## 🔧 Troubleshooting

### Services Won't Start
```bash
# Check Docker
docker --version

# Restart services
docker-compose -f docker-compose-minimal.yml down
docker-compose -f docker-compose-minimal.yml up -d

# Check logs
docker-compose -f docker-compose-minimal.yml logs -f
```

### Port Conflicts
```bash
# Windows: Find process
netstat -ano | findstr :8000

# Change ports in docker-compose-minimal.yml
```

### SDK Import Error
```bash
cd sdk/python
pip install -e .
```

### Check Service Health
```bash
# Individual service
curl http://localhost:8001/health

# All services
aidos status
```

---

## 🎯 Common Workflows

### Complete ML Pipeline
```python
from aidos import DataForge, ModelHub, Deploy, Analytics

# 1. Create dataset
df = DataForge()
dataset = df.create_dataset("Reviews", "Customer feedback", "text")

# 2. Create experiment
mh = ModelHub()
exp = mh.create_experiment("Model v1", "Test", "proj_1", "user_1")

# 3. Deploy
deploy = Deploy()
deployment = deploy.create(exp['id'], "Production API")

# 4. Check analytics
analytics = Analytics()
roi = analytics.calculate_roi()
print(f"ROI: {roi['roi_percent']}%")
```

### Team Collaboration
```python
from aidos import Collab

collab = Collab()

# Create team
team = collab.create_team("ML Team", "Research", "user_1")

# Add members
collab.add_member(team['id'], "user_2", "editor")
collab.add_member(team['id'], "user_3", "viewer")

# Share experiment
collab.share("experiment", "exp_123", "user_1", "user_2", "editor")

# Get activity
activity = collab.get_activity_feed("user_1")
```

### Auto-Scaling Setup
```python
from aidos import Deploy, AutoScale

# Deploy model
deploy = Deploy()
deployment = deploy.create("exp_123", "API")

# Set up auto-scaling
autoscale = AutoScale()
rule = autoscale.create_rule(
    deployment['deployment_id'],
    "Auto scale",
    "cpu",
    min_instances=2,
    max_instances=20,
    scale_up_threshold=75,
    scale_down_threshold=25
)

# Monitor
cost = autoscale.get_cost(deployment['deployment_id'])
print(f"Savings: {cost['savings_percent']}%")
```

---

## 📝 Quick Tips

### Performance
- Allocate 8GB+ RAM for Docker
- Use SSD for faster performance
- Close unused services to save resources

### Development
- Use SDK for complex workflows
- Use CLI for quick tasks
- Check Swagger UI at `/docs` endpoints

### Production
- Enable authentication
- Use environment variables for secrets
- Set up auto-scaling
- Monitor with Analytics service

---

## 🔗 Useful Links

- **Documentation:** [README.md](README.md)
- **Getting Started:** [GETTING_STARTED.md](GETTING_STARTED.md)
- **FAQ:** [FAQ.md](FAQ.md)
- **Roadmap:** [ROADMAP.md](ROADMAP.md)
- **Contributing:** [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📞 Need Help?

- 📚 [Full Documentation](README.md)
- ❓ [FAQ](FAQ.md)
- 🐛 [GitHub Issues](https://github.com/oladeji0909-hash/AI-DOS/issues)
- 📧 Email: team@ai-dos.io

---

<div align="center">

**[Back to README](README.md)** • **[Getting Started](GETTING_STARTED.md)** • **[FAQ](FAQ.md)**

Made with 🔥 by the AI-DOS community

</div>
