from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
import uuid
import requests

app = FastAPI(title="AI-DOS Deploy Service", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
deployments = {}
deployment_metrics = {}

class DeployRequest(BaseModel):
    experiment_id: str
    name: str
    description: Optional[str] = None
    environment: Optional[Dict] = None

class DeploymentResponse(BaseModel):
    deployment_id: str
    experiment_id: str
    name: str
    status: str
    endpoint_url: str
    created_at: str
    port: int

@app.get("/")
def root():
    return {
        "service": "AI-DOS Deploy Service",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "deploy": "/deploy/create",
            "list": "/deploy/list",
            "get": "/deploy/{deployment_id}",
            "delete": "/deploy/{deployment_id}",
            "logs": "/deploy/{deployment_id}/logs",
            "metrics": "/deploy/{deployment_id}/metrics"
        }
    }

@app.post("/deploy/create", response_model=DeploymentResponse)
def create_deployment(request: DeployRequest):
    """Deploy a model from ModelHub experiment"""
    
    # Verify experiment exists
    try:
        modelhub_url = "http://modelhub:8000"
        response = requests.get(f"{modelhub_url}/experiments/{request.experiment_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Experiment not found")
        experiment = response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch experiment: {str(e)}")
    
    # Generate deployment
    deployment_id = f"deploy_{uuid.uuid4().hex[:8]}"
    port = 9000 + len(deployments)  # Dynamic port assignment
    
    deployment = {
        "deployment_id": deployment_id,
        "experiment_id": request.experiment_id,
        "name": request.name,
        "description": request.description or f"Deployment of {experiment.get('name', 'model')}",
        "status": "running",
        "endpoint_url": f"http://localhost:{port}/predict",
        "port": port,
        "created_at": datetime.utcnow().isoformat(),
        "environment": request.environment or {},
        "experiment_data": experiment
    }
    
    deployments[deployment_id] = deployment
    
    # Initialize metrics
    deployment_metrics[deployment_id] = {
        "total_requests": 0,
        "successful_requests": 0,
        "failed_requests": 0,
        "avg_latency_ms": 0,
        "last_request": None
    }
    
    return DeploymentResponse(**deployment)

@app.get("/deploy/list")
def list_deployments():
    """List all deployments"""
    return {
        "deployments": list(deployments.values()),
        "total": len(deployments)
    }

@app.get("/deploy/{deployment_id}")
def get_deployment(deployment_id: str):
    """Get deployment details"""
    if deployment_id not in deployments:
        raise HTTPException(status_code=404, detail="Deployment not found")
    
    deployment = deployments[deployment_id]
    metrics = deployment_metrics.get(deployment_id, {})
    
    return {
        **deployment,
        "metrics": metrics
    }

@app.delete("/deploy/{deployment_id}")
def delete_deployment(deployment_id: str):
    """Shut down a deployment"""
    if deployment_id not in deployments:
        raise HTTPException(status_code=404, detail="Deployment not found")
    
    deployment = deployments[deployment_id]
    deployment["status"] = "stopped"
    deployment["stopped_at"] = datetime.utcnow().isoformat()
    
    return {
        "message": "Deployment stopped successfully",
        "deployment_id": deployment_id
    }

@app.get("/deploy/{deployment_id}/logs")
def get_deployment_logs(deployment_id: str, limit: int = 100):
    """Get deployment logs"""
    if deployment_id not in deployments:
        raise HTTPException(status_code=404, detail="Deployment not found")
    
    # Mock logs for now
    logs = [
        {"timestamp": datetime.utcnow().isoformat(), "level": "INFO", "message": "Deployment started"},
        {"timestamp": datetime.utcnow().isoformat(), "level": "INFO", "message": "Model loaded successfully"},
        {"timestamp": datetime.utcnow().isoformat(), "level": "INFO", "message": "API endpoint ready"},
    ]
    
    return {
        "deployment_id": deployment_id,
        "logs": logs[-limit:],
        "total": len(logs)
    }

@app.get("/deploy/{deployment_id}/metrics")
def get_deployment_metrics(deployment_id: str):
    """Get deployment usage metrics"""
    if deployment_id not in deployments:
        raise HTTPException(status_code=404, detail="Deployment not found")
    
    metrics = deployment_metrics.get(deployment_id, {})
    deployment = deployments[deployment_id]
    
    # Calculate uptime
    created_at = datetime.fromisoformat(deployment["created_at"])
    uptime_seconds = (datetime.utcnow() - created_at).total_seconds()
    
    return {
        "deployment_id": deployment_id,
        "status": deployment["status"],
        "uptime_seconds": uptime_seconds,
        "metrics": metrics,
        "endpoint_url": deployment["endpoint_url"]
    }

@app.post("/deploy/{deployment_id}/predict")
def predict(deployment_id: str, data: Dict):
    """Make prediction using deployed model"""
    if deployment_id not in deployments:
        raise HTTPException(status_code=404, detail="Deployment not found")
    
    deployment = deployments[deployment_id]
    
    if deployment["status"] != "running":
        raise HTTPException(status_code=400, detail="Deployment is not running")
    
    # Update metrics
    metrics = deployment_metrics[deployment_id]
    metrics["total_requests"] += 1
    metrics["successful_requests"] += 1
    metrics["last_request"] = datetime.utcnow().isoformat()
    
    # Mock prediction
    return {
        "deployment_id": deployment_id,
        "prediction": "positive",
        "confidence": 0.95,
        "model": deployment["name"],
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "deploy",
        "active_deployments": len([d for d in deployments.values() if d["status"] == "running"])
    }
