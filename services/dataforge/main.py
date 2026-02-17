from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import hashlib
import json

app = FastAPI(title="DataForge", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class Dataset(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    owner_id: str
    data_type: str  # image, text, audio, video, tabular
    size_bytes: int = 0
    num_samples: int = 0
    tags: List[str] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class DatasetVersion(BaseModel):
    id: Optional[str] = None
    dataset_id: str
    version: str
    commit_hash: str
    commit_message: str
    changes: Dict[str, Any]
    created_by: str
    created_at: Optional[datetime] = None

class Label(BaseModel):
    id: Optional[str] = None
    dataset_id: str
    file_path: str
    annotations: Dict[str, Any]
    labeler_id: str
    confidence: float = 1.0
    verified: bool = False
    created_at: Optional[datetime] = None

class QualityMetric(BaseModel):
    id: Optional[str] = None
    dataset_id: str
    metric_name: str
    value: float
    details: Dict[str, Any] = {}
    timestamp: Optional[datetime] = None

class SyntheticDataRequest(BaseModel):
    dataset_id: str
    num_samples: int
    generation_method: str  # augmentation, gan, diffusion, llm
    parameters: Dict[str, Any] = {}

# In-memory storage (replace with actual database)
datasets_db: Dict[str, Dataset] = {}
versions_db: Dict[str, List[DatasetVersion]] = {}
labels_db: Dict[str, List[Label]] = {}
metrics_db: Dict[str, List[QualityMetric]] = {}

# Endpoints

@app.get("/")
def root():
    return {
        "service": "DataForge",
        "version": "1.0.0",
        "status": "operational",
        "capabilities": [
            "dataset_management",
            "versioning",
            "labeling",
            "quality_analysis",
            "synthetic_generation"
        ]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# Dataset Management
@app.post("/datasets", response_model=Dataset)
def create_dataset(dataset: Dataset):
    dataset.id = hashlib.md5(f"{dataset.name}{datetime.utcnow()}".encode()).hexdigest()
    dataset.created_at = datetime.utcnow()
    dataset.updated_at = datetime.utcnow()
    datasets_db[dataset.id] = dataset
    versions_db[dataset.id] = []
    labels_db[dataset.id] = []
    metrics_db[dataset.id] = []
    return dataset

@app.get("/datasets", response_model=List[Dataset])
def list_datasets(owner_id: Optional[str] = None, data_type: Optional[str] = None):
    results = list(datasets_db.values())
    if owner_id:
        results = [d for d in results if d.owner_id == owner_id]
    if data_type:
        results = [d for d in results if d.data_type == data_type]
    return results

@app.get("/datasets/{dataset_id}", response_model=Dataset)
def get_dataset(dataset_id: str):
    if dataset_id not in datasets_db:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return datasets_db[dataset_id]

@app.put("/datasets/{dataset_id}", response_model=Dataset)
def update_dataset(dataset_id: str, dataset: Dataset):
    if dataset_id not in datasets_db:
        raise HTTPException(status_code=404, detail="Dataset not found")
    dataset.id = dataset_id
    dataset.updated_at = datetime.utcnow()
    datasets_db[dataset_id] = dataset
    return dataset

@app.delete("/datasets/{dataset_id}")
def delete_dataset(dataset_id: str):
    if dataset_id not in datasets_db:
        raise HTTPException(status_code=404, detail="Dataset not found")
    del datasets_db[dataset_id]
    del versions_db[dataset_id]
    del labels_db[dataset_id]
    del metrics_db[dataset_id]
    return {"message": "Dataset deleted successfully"}

# Versioning
@app.post("/datasets/{dataset_id}/versions", response_model=DatasetVersion)
def create_version(dataset_id: str, version: DatasetVersion):
    if dataset_id not in datasets_db:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    version.id = hashlib.md5(f"{dataset_id}{version.version}{datetime.utcnow()}".encode()).hexdigest()
    version.dataset_id = dataset_id
    version.created_at = datetime.utcnow()
    
    if dataset_id not in versions_db:
        versions_db[dataset_id] = []
    versions_db[dataset_id].append(version)
    
    return version

@app.get("/datasets/{dataset_id}/versions", response_model=List[DatasetVersion])
def list_versions(dataset_id: str):
    if dataset_id not in datasets_db:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return versions_db.get(dataset_id, [])

@app.get("/datasets/{dataset_id}/versions/{version_id}", response_model=DatasetVersion)
def get_version(dataset_id: str, version_id: str):
    if dataset_id not in datasets_db:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    versions = versions_db.get(dataset_id, [])
    for v in versions:
        if v.id == version_id:
            return v
    
    raise HTTPException(status_code=404, detail="Version not found")

# Labeling
@app.post("/datasets/{dataset_id}/labels", response_model=Label)
def create_label(dataset_id: str, label: Label):
    if dataset_id not in datasets_db:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    label.id = hashlib.md5(f"{dataset_id}{label.file_path}{datetime.utcnow()}".encode()).hexdigest()
    label.dataset_id = dataset_id
    label.created_at = datetime.utcnow()
    
    if dataset_id not in labels_db:
        labels_db[dataset_id] = []
    labels_db[dataset_id].append(label)
    
    return label

@app.get("/datasets/{dataset_id}/labels", response_model=List[Label])
def list_labels(dataset_id: str, verified: Optional[bool] = None):
    if dataset_id not in datasets_db:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    labels = labels_db.get(dataset_id, [])
    if verified is not None:
        labels = [l for l in labels if l.verified == verified]
    return labels

@app.put("/datasets/{dataset_id}/labels/{label_id}/verify")
def verify_label(dataset_id: str, label_id: str):
    if dataset_id not in datasets_db:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    labels = labels_db.get(dataset_id, [])
    for label in labels:
        if label.id == label_id:
            label.verified = True
            return {"message": "Label verified successfully"}
    
    raise HTTPException(status_code=404, detail="Label not found")

# Quality Metrics
@app.post("/datasets/{dataset_id}/metrics", response_model=QualityMetric)
def create_metric(dataset_id: str, metric: QualityMetric):
    if dataset_id not in datasets_db:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    metric.id = hashlib.md5(f"{dataset_id}{metric.metric_name}{datetime.utcnow()}".encode()).hexdigest()
    metric.dataset_id = dataset_id
    metric.timestamp = datetime.utcnow()
    
    if dataset_id not in metrics_db:
        metrics_db[dataset_id] = []
    metrics_db[dataset_id].append(metric)
    
    return metric

@app.get("/datasets/{dataset_id}/metrics", response_model=List[QualityMetric])
def list_metrics(dataset_id: str, metric_name: Optional[str] = None):
    if dataset_id not in datasets_db:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    metrics = metrics_db.get(dataset_id, [])
    if metric_name:
        metrics = [m for m in metrics if m.metric_name == metric_name]
    return metrics

@app.post("/datasets/{dataset_id}/analyze")
def analyze_quality(dataset_id: str):
    if dataset_id not in datasets_db:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Simulate quality analysis
    metrics = [
        QualityMetric(
            dataset_id=dataset_id,
            metric_name="completeness",
            value=0.95,
            details={"missing_values": 50, "total_values": 1000}
        ),
        QualityMetric(
            dataset_id=dataset_id,
            metric_name="consistency",
            value=0.98,
            details={"inconsistent_records": 20}
        ),
        QualityMetric(
            dataset_id=dataset_id,
            metric_name="accuracy",
            value=0.92,
            details={"validation_errors": 80}
        )
    ]
    
    for metric in metrics:
        create_metric(dataset_id, metric)
    
    return {"message": "Quality analysis completed", "metrics": metrics}

# Synthetic Data Generation
@app.post("/datasets/{dataset_id}/generate-synthetic")
def generate_synthetic(dataset_id: str, request: SyntheticDataRequest):
    if dataset_id not in datasets_db:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Simulate synthetic data generation
    return {
        "message": "Synthetic data generation started",
        "job_id": hashlib.md5(f"{dataset_id}{datetime.utcnow()}".encode()).hexdigest(),
        "status": "processing",
        "estimated_completion": "5 minutes",
        "method": request.generation_method,
        "num_samples": request.num_samples
    }

@app.post("/datasets/{dataset_id}/upload")
async def upload_data(dataset_id: str, file: UploadFile = File(...)):
    if dataset_id not in datasets_db:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Simulate file upload
    contents = await file.read()
    file_size = len(contents)
    
    dataset = datasets_db[dataset_id]
    dataset.size_bytes += file_size
    dataset.num_samples += 1
    dataset.updated_at = datetime.utcnow()
    
    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "size_bytes": file_size,
        "dataset_id": dataset_id
    }

@app.get("/datasets/{dataset_id}/statistics")
def get_statistics(dataset_id: str):
    if dataset_id not in datasets_db:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    dataset = datasets_db[dataset_id]
    labels = labels_db.get(dataset_id, [])
    versions = versions_db.get(dataset_id, [])
    metrics = metrics_db.get(dataset_id, [])
    
    return {
        "dataset_id": dataset_id,
        "total_samples": dataset.num_samples,
        "total_size_bytes": dataset.size_bytes,
        "total_labels": len(labels),
        "verified_labels": len([l for l in labels if l.verified]),
        "total_versions": len(versions),
        "quality_metrics": len(metrics),
        "data_type": dataset.data_type,
        "created_at": dataset.created_at,
        "last_updated": dataset.updated_at
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
