# 🚀 AI-DOS Python SDK

Build production ML models in seconds with plain English.

## Installation

```bash
pip install aidos
```

Or install from source:
```bash
cd sdk/python
pip install -e .
```

## Quick Start

### Magic Mode (One Line!)

```python
from aidos import magic

# That's it! One line to create a complete ML pipeline
result = magic("Build a sentiment analyzer for tweets")

print(f"✅ Dataset: {result['dataset_id']}")
print(f"✅ Experiment: {result['experiment_id']}")
print(f"✅ API: {result['api_endpoint']}")
print(f"✅ Code:\n{result['code']}")
```

### Full Control

```python
from aidos import Magic, DataForge, ModelHub

# Create dataset
df = DataForge()
dataset = df.create_dataset(
    name="Twitter Sentiment Data",
    description="10K tweets with sentiment labels",
    owner_id="user123",
    data_type="text"
)

# Track experiment
mh = ModelHub()
experiment = mh.create_experiment(
    name="Sentiment Analysis v1",
    description="Testing different architectures",
    project_id="sentiment-project",
    user_id="user123",
    tags=["nlp", "sentiment"]
)

# Create training run
run = mh.create_run(
    experiment_id=experiment['id'],
    name="BERT baseline",
    parameters={
        "model": "bert-base-uncased",
        "learning_rate": 2e-5,
        "batch_size": 32,
        "epochs": 3
    },
    user_id="user123"
)

# Log metrics
mh.log_metrics(
    run_id=run['id'],
    metrics={
        "accuracy": 0.95,
        "f1_score": 0.94,
        "loss": 0.12
    },
    step=100
)

# Use Magic Mode
magic = Magic()
result = magic.create("Build a sentiment analyzer for tweets")
```

### Authentication

```python
from aidos import AIDOS

client = AIDOS()

# Register
client.register(
    username="john_doe",
    email="john@example.com",
    password="secure_password",
    full_name="John Doe"
)

# Login
token = client.login("john_doe", "secure_password")
print(f"Access token: {token}")
```

## Examples

### Example 1: Sentiment Analysis

```python
from aidos import magic

result = magic("Build a sentiment analyzer for tweets")
# ✅ Complete pipeline created in 1 second!
```

### Example 2: Image Classification

```python
from aidos import magic

result = magic("Build an image classifier for cats vs dogs")
# ✅ Dataset, model, training, deployment - all done!
```

### Example 3: Text Generation

```python
from aidos import magic

result = magic("Build a text generator for product descriptions")
# ✅ GPT-2 model trained and deployed!
```

### Example 4: Track Your Own Training

```python
from aidos import ModelHub

mh = ModelHub()

# Create experiment
exp = mh.create_experiment(
    name="My Custom Model",
    description="Testing new architecture",
    project_id="my-project",
    user_id="me"
)

# Create run
run = mh.create_run(
    experiment_id=exp['id'],
    name="Run 1",
    parameters={"lr": 0.001, "batch_size": 64},
    user_id="me"
)

# Log metrics during training
for epoch in range(10):
    # ... your training code ...
    mh.log_metrics(
        run_id=run['id'],
        metrics={"loss": loss, "accuracy": acc},
        step=epoch
    )
```

## API Reference

### Magic

```python
Magic(api_url="http://localhost:8003")
```

**Methods:**
- `create(prompt, user_id, auto_deploy)` - Create ML pipeline from text
- `status(job_id)` - Get job status

### DataForge

```python
DataForge(api_url="http://localhost:8001")
```

**Methods:**
- `create_dataset(name, description, owner_id, data_type)` - Create dataset
- `list_datasets(skip, limit)` - List all datasets
- `get_dataset(dataset_id)` - Get dataset by ID
- `create_version(dataset_id, version, changes, created_by)` - Version dataset

### ModelHub

```python
ModelHub(api_url="http://localhost:8002")
```

**Methods:**
- `create_experiment(name, description, project_id, user_id, tags)` - Create experiment
- `list_experiments(skip, limit)` - List experiments
- `create_run(experiment_id, name, parameters, user_id)` - Create training run
- `log_metrics(run_id, metrics, step)` - Log metrics

### AIDOS

```python
AIDOS(api_url="http://localhost:8000", api_key=None)
```

**Methods:**
- `register(username, email, password, full_name)` - Register user
- `login(username, password)` - Login and get token

## Configuration

Set custom API URLs:

```python
from aidos import Magic, DataForge, ModelHub

magic = Magic(api_url="https://api.ai-dos.io")
df = DataForge(api_url="https://dataforge.ai-dos.io")
mh = ModelHub(api_url="https://modelhub.ai-dos.io")
```

## Help

```python
from aidos import quick_start

quick_start()  # Prints quick start guide
```

## License

MIT License - see LICENSE file for details

## Links

- 🌐 Website: https://ai-dos.io
- 📚 Docs: https://docs.ai-dos.io
- 💬 Discord: https://discord.gg/ai-dos
- 🐙 GitHub: https://github.com/your-org/ai-dos

---

**Built with ❤️ by the AI-DOS community**
