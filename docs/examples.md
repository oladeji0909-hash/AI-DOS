# AI-DOS Usage Examples

Complete examples showing how to use AI-DOS for real-world AI/ML workflows.

---

## Example 1: Image Classification Pipeline

### Complete workflow from dataset to deployed model

```python
import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
DATAFORGE_URL = "http://localhost:8001"
MODELHUB_URL = "http://localhost:8002"

# Step 1: Register and Login
print("Step 1: Authentication")
register_response = requests.post(
    f"{BASE_URL}/auth/register",
    json={
        "username": "ml_engineer",
        "email": "ml@company.com",
        "password": "secure_password",
        "full_name": "ML Engineer"
    }
)
print(f"✅ User registered: {register_response.status_code == 200}")

login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"username": "ml_engineer", "password": "secure_password"}
)
token = login_response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print(f"✅ Logged in successfully")

# Step 2: Create Dataset
print("\nStep 2: Create Dataset")
dataset_response = requests.post(
    f"{DATAFORGE_URL}/datasets",
    headers=headers,
    json={
        "name": "CIFAR-10",
        "description": "60,000 32x32 color images in 10 classes",
        "owner_id": "ml_engineer",
        "data_type": "image",
        "tags": ["classification", "computer-vision", "cifar"]
    }
)
dataset = dataset_response.json()
dataset_id = dataset["id"]
print(f"✅ Dataset created: {dataset_id}")

# Step 3: Upload Data (simulated)
print("\nStep 3: Upload Training Data")
# In real scenario, you'd upload actual files
for i in range(10):
    requests.post(
        f"{DATAFORGE_URL}/datasets/{dataset_id}/upload",
        headers=headers,
        files={"file": (f"batch_{i}.tar", b"fake_data")}
    )
print(f"✅ Uploaded 10 batches")

# Step 4: Create Version
print("\nStep 4: Version Dataset")
version_response = requests.post(
    f"{DATAFORGE_URL}/datasets/{dataset_id}/versions",
    headers=headers,
    json={
        "dataset_id": dataset_id,
        "version": "v1.0",
        "commit_hash": "abc123",
        "commit_message": "Initial dataset version",
        "changes": {"added": 60000, "modified": 0, "deleted": 0},
        "created_by": "ml_engineer"
    }
)
print(f"✅ Version created: v1.0")

# Step 5: Analyze Quality
print("\nStep 5: Analyze Data Quality")
quality_response = requests.post(
    f"{DATAFORGE_URL}/datasets/{dataset_id}/analyze",
    headers=headers
)
print(f"✅ Quality analysis complete")

# Step 6: Create Experiment
print("\nStep 6: Create Experiment")
experiment_response = requests.post(
    f"{MODELHUB_URL}/experiments",
    headers=headers,
    json={
        "name": "ResNet-50 CIFAR-10",
        "description": "Train ResNet-50 on CIFAR-10 dataset",
        "project_id": "image_classification",
        "user_id": "ml_engineer",
        "tags": ["resnet", "cifar10", "classification"]
    }
)
experiment = experiment_response.json()
experiment_id = experiment["id"]
print(f"✅ Experiment created: {experiment_id}")

# Step 7: Hyperparameter Optimization
print("\nStep 7: Hyperparameter Optimization")
hp_job_response = requests.post(
    f"{MODELHUB_URL}/experiments/{experiment_id}/hyperparameter-jobs",
    headers=headers,
    json={
        "experiment_id": experiment_id,
        "search_space": {
            "learning_rate": [0.001, 0.01, 0.1],
            "batch_size": [32, 64, 128],
            "optimizer": ["adam", "sgd"],
            "weight_decay": [0.0001, 0.001]
        },
        "search_method": "bayesian",
        "num_trials": 20
    }
)
hp_job = hp_job_response.json()
print(f"✅ HP optimization started: {hp_job['id']}")

# Step 8: Training Runs
print("\nStep 8: Training Runs")
best_accuracy = 0
best_run_id = None

for trial in range(3):
    # Create run
    run_response = requests.post(
        f"{MODELHUB_URL}/experiments/{experiment_id}/runs",
        headers=headers,
        json={
            "experiment_id": experiment_id,
            "name": f"Trial {trial + 1}",
            "parameters": {
                "learning_rate": 0.001 * (trial + 1),
                "batch_size": 64,
                "epochs": 50,
                "optimizer": "adam"
            }
        }
    )
    run = run_response.json()
    run_id = run["id"]
    
    # Simulate training with metric logging
    for epoch in range(50):
        accuracy = 0.5 + (epoch * 0.01) + (trial * 0.05)
        loss = 2.0 - (epoch * 0.03) - (trial * 0.1)
        
        requests.post(
            f"{MODELHUB_URL}/runs/{run_id}/log-metrics",
            headers=headers,
            json={
                "run_id": run_id,
                "step": epoch,
                "metrics": {
                    "train_loss": loss,
                    "train_accuracy": accuracy,
                    "val_loss": loss + 0.1,
                    "val_accuracy": accuracy - 0.05
                }
            }
        )
    
    # Complete run
    final_accuracy = 0.5 + (50 * 0.01) + (trial * 0.05)
    requests.put(
        f"{MODELHUB_URL}/runs/{run_id}/complete",
        headers=headers,
        json={
            "loss": 0.5 - (trial * 0.1),
            "accuracy": final_accuracy
        }
    )
    
    if final_accuracy > best_accuracy:
        best_accuracy = final_accuracy
        best_run_id = run_id
    
    print(f"✅ Trial {trial + 1} complete: accuracy={final_accuracy:.3f}")

# Step 9: Register Best Model
print("\nStep 9: Register Best Model")
model_response = requests.post(
    f"{MODELHUB_URL}/models",
    headers=headers,
    json={
        "name": "ResNet-50-CIFAR10",
        "version": "1.0.0",
        "description": "ResNet-50 trained on CIFAR-10",
        "framework": "pytorch",
        "experiment_id": experiment_id,
        "run_id": best_run_id,
        "metrics": {
            "accuracy": best_accuracy,
            "loss": 0.5,
            "f1_score": 0.89
        },
        "parameters": {
            "learning_rate": 0.001,
            "batch_size": 64,
            "epochs": 50
        },
        "registry_path": "/models/resnet50_cifar10_v1.pth",
        "size_bytes": 102400000,
        "tags": ["production", "resnet50", "cifar10"],
        "created_by": "ml_engineer"
    }
)
model = model_response.json()
print(f"✅ Model registered: {model['id']}")

# Step 10: Get Experiment Summary
print("\nStep 10: Experiment Summary")
summary_response = requests.get(
    f"{MODELHUB_URL}/experiments/{experiment_id}/summary",
    headers=headers
)
summary = summary_response.json()
print(f"✅ Total runs: {summary['total_runs']}")
print(f"✅ Completed: {summary['completed_runs']}")
print(f"✅ Best accuracy: {best_accuracy:.3f}")

print("\n🎉 Complete pipeline executed successfully!")
```

---

## Example 2: NLP Model Development

```python
import requests

BASE_URL = "http://localhost:8000"
DATAFORGE_URL = "http://localhost:8001"
MODELHUB_URL = "http://localhost:8002"

# Authenticate
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"username": "nlp_researcher", "password": "password"}
)
token = login_response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Create text dataset
dataset = requests.post(
    f"{DATAFORGE_URL}/datasets",
    headers=headers,
    json={
        "name": "IMDB Reviews",
        "description": "50K movie reviews for sentiment analysis",
        "owner_id": "nlp_researcher",
        "data_type": "text",
        "tags": ["nlp", "sentiment", "reviews"]
    }
).json()

# Add labels
for i in range(100):
    requests.post(
        f"{DATAFORGE_URL}/datasets/{dataset['id']}/labels",
        headers=headers,
        json={
            "dataset_id": dataset['id'],
            "file_path": f"review_{i}.txt",
            "annotations": {
                "sentiment": "positive" if i % 2 == 0 else "negative",
                "confidence": 0.95
            },
            "labeler_id": "nlp_researcher",
            "confidence": 0.95
        }
    )

# Create experiment
experiment = requests.post(
    f"{MODELHUB_URL}/experiments",
    headers=headers,
    json={
        "name": "BERT Sentiment Analysis",
        "description": "Fine-tune BERT for sentiment classification",
        "project_id": "nlp_project",
        "user_id": "nlp_researcher",
        "tags": ["bert", "sentiment", "transformer"]
    }
).json()

# Training run
run = requests.post(
    f"{MODELHUB_URL}/experiments/{experiment['id']}/runs",
    headers=headers,
    json={
        "experiment_id": experiment['id'],
        "name": "BERT-base fine-tuning",
        "parameters": {
            "model": "bert-base-uncased",
            "learning_rate": 2e-5,
            "batch_size": 16,
            "epochs": 3,
            "max_length": 512
        }
    }
).json()

# Log training metrics
for epoch in range(3):
    requests.post(
        f"{MODELHUB_URL}/runs/{run['id']}/log-metrics",
        headers=headers,
        json={
            "run_id": run['id'],
            "step": epoch,
            "metrics": {
                "train_loss": 0.5 - (epoch * 0.15),
                "train_accuracy": 0.7 + (epoch * 0.08),
                "val_loss": 0.6 - (epoch * 0.12),
                "val_accuracy": 0.68 + (epoch * 0.07)
            }
        }
    )

# Complete and register
requests.put(
    f"{MODELHUB_URL}/runs/{run['id']}/complete",
    headers=headers,
    json={"loss": 0.2, "accuracy": 0.91}
)

model = requests.post(
    f"{MODELHUB_URL}/models",
    headers=headers,
    json={
        "name": "BERT-Sentiment-IMDB",
        "version": "1.0.0",
        "description": "BERT fine-tuned on IMDB reviews",
        "framework": "pytorch",
        "experiment_id": experiment['id'],
        "run_id": run['id'],
        "metrics": {"accuracy": 0.91, "f1": 0.90},
        "registry_path": "/models/bert_sentiment_v1.pth",
        "created_by": "nlp_researcher"
    }
).json()

print(f"✅ NLP model trained and registered: {model['id']}")
```

---

## Example 3: Multi-Model Comparison

```python
import requests
import pandas as pd

MODELHUB_URL = "http://localhost:8002"
headers = {"Authorization": f"Bearer {token}"}

# Create experiment
experiment = requests.post(
    f"{MODELHUB_URL}/experiments",
    headers=headers,
    json={
        "name": "Model Architecture Comparison",
        "description": "Compare different architectures on same dataset",
        "project_id": "comparison_study",
        "user_id": "researcher"
    }
).json()

# Train multiple models
models = ["ResNet-50", "EfficientNet-B0", "ViT-Base", "MobileNet-V3"]
run_ids = []

for model_name in models:
    run = requests.post(
        f"{MODELHUB_URL}/experiments/{experiment['id']}/runs",
        headers=headers,
        json={
            "experiment_id": experiment['id'],
            "name": f"{model_name} Training",
            "parameters": {
                "model": model_name,
                "learning_rate": 0.001,
                "batch_size": 64,
                "epochs": 50
            }
        }
    ).json()
    
    # Simulate training
    for epoch in range(50):
        accuracy = 0.6 + (epoch * 0.008) + (models.index(model_name) * 0.02)
        requests.post(
            f"{MODELHUB_URL}/runs/{run['id']}/log-metrics",
            headers=headers,
            json={
                "run_id": run['id'],
                "step": epoch,
                "metrics": {
                    "accuracy": accuracy,
                    "loss": 1.0 - (epoch * 0.015)
                }
            }
        )
    
    requests.put(
        f"{MODELHUB_URL}/runs/{run['id']}/complete",
        headers=headers,
        json={"accuracy": accuracy, "loss": 0.25}
    )
    
    run_ids.append(run['id'])

# Compare runs
comparison = requests.post(
    f"{MODELHUB_URL}/compare-runs",
    headers=headers,
    json=run_ids
).json()

# Display results
print("\n📊 Model Comparison Results:")
print("-" * 60)
for run in comparison['runs']:
    print(f"{run['name']:20} | Accuracy: {run['metrics']['accuracy']:.3f}")
print("-" * 60)
```

---

## Example 4: Dataset Versioning Workflow

```python
import requests

DATAFORGE_URL = "http://localhost:8001"
headers = {"Authorization": f"Bearer {token}"}

# Create dataset
dataset = requests.post(
    f"{DATAFORGE_URL}/datasets",
    headers=headers,
    json={
        "name": "Customer Data",
        "description": "Customer behavior dataset",
        "owner_id": "data_scientist",
        "data_type": "tabular"
    }
).json()

dataset_id = dataset['id']

# Version 1.0 - Initial data
requests.post(
    f"{DATAFORGE_URL}/datasets/{dataset_id}/versions",
    headers=headers,
    json={
        "dataset_id": dataset_id,
        "version": "v1.0",
        "commit_hash": "abc123",
        "commit_message": "Initial dataset with 10K samples",
        "changes": {"added": 10000, "modified": 0, "deleted": 0},
        "created_by": "data_scientist"
    }
)

# Version 1.1 - Added more data
requests.post(
    f"{DATAFORGE_URL}/datasets/{dataset_id}/versions",
    headers=headers,
    json={
        "dataset_id": dataset_id,
        "version": "v1.1",
        "commit_hash": "def456",
        "commit_message": "Added 5K more samples",
        "changes": {"added": 5000, "modified": 0, "deleted": 0},
        "created_by": "data_scientist"
    }
)

# Version 1.2 - Cleaned data
requests.post(
    f"{DATAFORGE_URL}/datasets/{dataset_id}/versions",
    headers=headers,
    json={
        "dataset_id": dataset_id,
        "version": "v1.2",
        "commit_hash": "ghi789",
        "commit_message": "Removed duplicates and outliers",
        "changes": {"added": 0, "modified": 500, "deleted": 200},
        "created_by": "data_scientist"
    }
)

# List all versions
versions = requests.get(
    f"{DATAFORGE_URL}/datasets/{dataset_id}/versions",
    headers=headers
).json()

print(f"\n📦 Dataset Versions:")
for v in versions:
    print(f"  {v['version']}: {v['commit_message']}")
```

---

## Example 5: Collaborative Labeling

```python
import requests

DATAFORGE_URL = "http://localhost:8001"

# Multiple labelers
labelers = ["labeler1", "labeler2", "labeler3"]
tokens = {}

# Each labeler logs in
for labeler in labelers:
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": labeler, "password": "password"}
    )
    tokens[labeler] = response.json()["access_token"]

# Create dataset
headers = {"Authorization": f"Bearer {tokens['labeler1']}"}
dataset = requests.post(
    f"{DATAFORGE_URL}/datasets",
    headers=headers,
    json={
        "name": "Medical Images",
        "description": "X-ray images for disease detection",
        "owner_id": "labeler1",
        "data_type": "image"
    }
).json()

# Each labeler labels different images
for i, labeler in enumerate(labelers):
    headers = {"Authorization": f"Bearer {tokens[labeler]}"}
    
    for j in range(10):
        image_id = i * 10 + j
        requests.post(
            f"{DATAFORGE_URL}/datasets/{dataset['id']}/labels",
            headers=headers,
            json={
                "dataset_id": dataset['id'],
                "file_path": f"xray_{image_id}.jpg",
                "annotations": {
                    "disease": "pneumonia" if image_id % 3 == 0 else "normal",
                    "confidence": 0.85 + (j * 0.01),
                    "bounding_boxes": []
                },
                "labeler_id": labeler,
                "confidence": 0.85
            }
        )

# Get labeling statistics
labels = requests.get(
    f"{DATAFORGE_URL}/datasets/{dataset['id']}/labels",
    headers=headers
).json()

print(f"\n👥 Labeling Statistics:")
print(f"  Total labels: {len(labels)}")
print(f"  Verified: {len([l for l in labels if l['verified']])}")
print(f"  Pending: {len([l for l in labels if not l['verified']])}")
```

---

## Example 6: API Key Usage

```python
import requests

BASE_URL = "http://localhost:8000"

# Login
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"username": "api_user", "password": "password"}
)
token = login_response.json()["access_token"]

# Generate API key
api_key_response = requests.post(
    f"{BASE_URL}/api-keys/generate",
    headers={"Authorization": f"Bearer {token}"}
)
api_key = api_key_response.json()["api_key"]
print(f"✅ API Key generated: {api_key[:20]}...")

# Use API key instead of JWT
headers = {"X-API-Key": api_key}

# Make requests with API key
dataset = requests.post(
    f"{DATAFORGE_URL}/datasets",
    headers=headers,
    json={
        "name": "API Test Dataset",
        "description": "Created using API key",
        "owner_id": "api_user",
        "data_type": "text"
    }
).json()

print(f"✅ Dataset created using API key: {dataset['id']}")

# Validate API key
validation = requests.get(
    f"{BASE_URL}/api-keys/validate",
    headers=headers
).json()

print(f"✅ API key valid: {validation['valid']}")
```

---

## Example 7: Batch Operations

```python
import requests
import concurrent.futures

DATAFORGE_URL = "http://localhost:8001"
headers = {"Authorization": f"Bearer {token}"}

# Create multiple datasets in parallel
def create_dataset(i):
    return requests.post(
        f"{DATAFORGE_URL}/datasets",
        headers=headers,
        json={
            "name": f"Dataset {i}",
            "description": f"Batch created dataset {i}",
            "owner_id": "batch_user",
            "data_type": "image"
        }
    ).json()

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    datasets = list(executor.map(create_dataset, range(50)))

print(f"✅ Created {len(datasets)} datasets in parallel")

# Batch quality analysis
for dataset in datasets[:10]:  # Analyze first 10
    requests.post(
        f"{DATAFORGE_URL}/datasets/{dataset['id']}/analyze",
        headers=headers
    )

print(f"✅ Analyzed 10 datasets")
```

---

## Tips for Using AI-DOS

### 1. Always Use Authentication
```python
# Get token first
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"username": "user", "password": "pass"}
)
token = login_response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Use headers in all requests
response = requests.get(url, headers=headers)
```

### 2. Handle Errors Gracefully
```python
try:
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    result = response.json()
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```

### 3. Use Pagination for Large Results
```python
page = 0
page_size = 100
all_datasets = []

while True:
    response = requests.get(
        f"{DATAFORGE_URL}/datasets?page={page}&size={page_size}",
        headers=headers
    )
    datasets = response.json()
    if not datasets:
        break
    all_datasets.extend(datasets)
    page += 1
```

### 4. Monitor Long-Running Operations
```python
# Submit job
job = requests.post(url, json=data, headers=headers).json()
job_id = job['id']

# Poll for completion
import time
while True:
    status = requests.get(f"{url}/{job_id}", headers=headers).json()
    if status['status'] in ['completed', 'failed']:
        break
    time.sleep(5)
```

---

**These examples show the power and flexibility of AI-DOS!** 🚀
