from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import hashlib
import json

app = FastAPI(title="ModelHub", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enums
class ExperimentStatus(str, Enum):
    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ModelFramework(str, Enum):
    PYTORCH = "pytorch"
    TENSORFLOW = "tensorflow"
    JAX = "jax"
    SCIKIT_LEARN = "scikit_learn"
    XGBOOST = "xgboost"
    ONNX = "onnx"

# Models
class Experiment(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    project_id: str
    user_id: str
    status: ExperimentStatus = ExperimentStatus.CREATED
    tags: List[str] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Run(BaseModel):
    id: Optional[str] = None
    experiment_id: str
    name: str
    parameters: Dict[str, Any]
    metrics: Dict[str, float] = {}
    artifacts_path: Optional[str] = None
    status: ExperimentStatus = ExperimentStatus.CREATED
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_seconds: Optional[float] = None

class Model(BaseModel):
    id: Optional[str] = None
    name: str
    version: str
    description: str
    framework: ModelFramework
    experiment_id: Optional[str] = None
    run_id: Optional[str] = None
    metrics: Dict[str, float] = {}
    parameters: Dict[str, Any] = {}
    registry_path: str
    size_bytes: int = 0
    tags: List[str] = []
    created_by: str
    created_at: Optional[datetime] = None

class HyperparameterJob(BaseModel):
    id: Optional[str] = None
    experiment_id: str
    search_space: Dict[str, Any]
    search_method: str  # grid, random, bayesian
    num_trials: int
    best_params: Optional[Dict[str, Any]] = None
    best_score: Optional[float] = None
    status: ExperimentStatus = ExperimentStatus.CREATED
    created_at: Optional[datetime] = None

class MetricLog(BaseModel):
    run_id: str
    step: int
    metrics: Dict[str, float]
    timestamp: Optional[datetime] = None

# In-memory storage
experiments_db: Dict[str, Experiment] = {}
runs_db: Dict[str, List[Run]] = {}
models_db: Dict[str, Model] = {}
hyperparameter_jobs_db: Dict[str, HyperparameterJob] = {}
metric_logs_db: Dict[str, List[MetricLog]] = {}

# Endpoints

@app.get("/")
def root():
    return {
        "service": "ModelHub",
        "version": "1.0.0",
        "status": "operational",
        "capabilities": [
            "experiment_tracking",
            "model_registry",
            "hyperparameter_optimization",
            "metrics_logging",
            "model_comparison"
        ]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# Experiments
@app.post("/experiments", response_model=Experiment)
def create_experiment(experiment: Experiment):
    experiment.id = hashlib.md5(f"{experiment.name}{datetime.utcnow()}".encode()).hexdigest()
    experiment.created_at = datetime.utcnow()
    experiment.updated_at = datetime.utcnow()
    experiments_db[experiment.id] = experiment
    runs_db[experiment.id] = []
    return experiment

@app.get("/experiments", response_model=List[Experiment])
def list_experiments(project_id: Optional[str] = None, user_id: Optional[str] = None):
    results = list(experiments_db.values())
    if project_id:
        results = [e for e in results if e.project_id == project_id]
    if user_id:
        results = [e for e in results if e.user_id == user_id]
    return results

@app.get("/experiments/{experiment_id}", response_model=Experiment)
def get_experiment(experiment_id: str):
    if experiment_id not in experiments_db:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return experiments_db[experiment_id]

@app.put("/experiments/{experiment_id}", response_model=Experiment)
def update_experiment(experiment_id: str, experiment: Experiment):
    if experiment_id not in experiments_db:
        raise HTTPException(status_code=404, detail="Experiment not found")
    experiment.id = experiment_id
    experiment.updated_at = datetime.utcnow()
    experiments_db[experiment_id] = experiment
    return experiment

@app.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: str):
    if experiment_id not in experiments_db:
        raise HTTPException(status_code=404, detail="Experiment not found")
    del experiments_db[experiment_id]
    del runs_db[experiment_id]
    return {"message": "Experiment deleted successfully"}

# Runs
@app.post("/experiments/{experiment_id}/runs", response_model=Run)
def create_run(experiment_id: str, run: Run):
    if experiment_id not in experiments_db:
        raise HTTPException(status_code=404, detail="Experiment not found")
    
    run.id = hashlib.md5(f"{experiment_id}{run.name}{datetime.utcnow()}".encode()).hexdigest()
    run.experiment_id = experiment_id
    run.start_time = datetime.utcnow()
    run.status = ExperimentStatus.RUNNING
    
    if experiment_id not in runs_db:
        runs_db[experiment_id] = []
    runs_db[experiment_id].append(run)
    
    return run

@app.get("/experiments/{experiment_id}/runs", response_model=List[Run])
def list_runs(experiment_id: str):
    if experiment_id not in experiments_db:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return runs_db.get(experiment_id, [])

@app.get("/runs/{run_id}", response_model=Run)
def get_run(run_id: str):
    for runs in runs_db.values():
        for run in runs:
            if run.id == run_id:
                return run
    raise HTTPException(status_code=404, detail="Run not found")

@app.put("/runs/{run_id}/complete")
def complete_run(run_id: str, final_metrics: Dict[str, float]):
    for runs in runs_db.values():
        for run in runs:
            if run.id == run_id:
                run.status = ExperimentStatus.COMPLETED
                run.end_time = datetime.utcnow()
                run.duration_seconds = (run.end_time - run.start_time).total_seconds()
                run.metrics.update(final_metrics)
                return run
    raise HTTPException(status_code=404, detail="Run not found")

@app.post("/runs/{run_id}/log-metrics")
def log_metrics(run_id: str, metric_log: MetricLog):
    metric_log.run_id = run_id
    metric_log.timestamp = datetime.utcnow()
    
    if run_id not in metric_logs_db:
        metric_logs_db[run_id] = []
    metric_logs_db[run_id].append(metric_log)
    
    # Update run metrics
    for runs in runs_db.values():
        for run in runs:
            if run.id == run_id:
                run.metrics.update(metric_log.metrics)
                break
    
    return {"message": "Metrics logged successfully"}

@app.get("/runs/{run_id}/metrics")
def get_run_metrics(run_id: str):
    if run_id not in metric_logs_db:
        return []
    return metric_logs_db[run_id]

# Models
@app.post("/models", response_model=Model)
def register_model(model: Model):
    model.id = hashlib.md5(f"{model.name}{model.version}{datetime.utcnow()}".encode()).hexdigest()
    model.created_at = datetime.utcnow()
    models_db[model.id] = model
    return model

@app.get("/models", response_model=List[Model])
def list_models(framework: Optional[ModelFramework] = None, created_by: Optional[str] = None):
    results = list(models_db.values())
    if framework:
        results = [m for m in results if m.framework == framework]
    if created_by:
        results = [m for m in results if m.created_by == created_by]
    return results

@app.get("/models/{model_id}", response_model=Model)
def get_model(model_id: str):
    if model_id not in models_db:
        raise HTTPException(status_code=404, detail="Model not found")
    return models_db[model_id]

@app.get("/models/{model_id}/versions")
def get_model_versions(model_id: str):
    if model_id not in models_db:
        raise HTTPException(status_code=404, detail="Model not found")
    
    base_model = models_db[model_id]
    versions = [m for m in models_db.values() if m.name == base_model.name]
    return sorted(versions, key=lambda x: x.created_at, reverse=True)

@app.delete("/models/{model_id}")
def delete_model(model_id: str):
    if model_id not in models_db:
        raise HTTPException(status_code=404, detail="Model not found")
    del models_db[model_id]
    return {"message": "Model deleted successfully"}

# Hyperparameter Optimization
@app.post("/experiments/{experiment_id}/hyperparameter-jobs", response_model=HyperparameterJob)
def create_hyperparameter_job(experiment_id: str, job: HyperparameterJob):
    if experiment_id not in experiments_db:
        raise HTTPException(status_code=404, detail="Experiment not found")
    
    job.id = hashlib.md5(f"{experiment_id}{datetime.utcnow()}".encode()).hexdigest()
    job.experiment_id = experiment_id
    job.created_at = datetime.utcnow()
    job.status = ExperimentStatus.RUNNING
    hyperparameter_jobs_db[job.id] = job
    
    return job

@app.get("/hyperparameter-jobs/{job_id}", response_model=HyperparameterJob)
def get_hyperparameter_job(job_id: str):
    if job_id not in hyperparameter_jobs_db:
        raise HTTPException(status_code=404, detail="Hyperparameter job not found")
    return hyperparameter_jobs_db[job_id]

@app.put("/hyperparameter-jobs/{job_id}/complete")
def complete_hyperparameter_job(job_id: str, best_params: Dict[str, Any], best_score: float):
    if job_id not in hyperparameter_jobs_db:
        raise HTTPException(status_code=404, detail="Hyperparameter job not found")
    
    job = hyperparameter_jobs_db[job_id]
    job.status = ExperimentStatus.COMPLETED
    job.best_params = best_params
    job.best_score = best_score
    
    return job

# Comparison
@app.post("/compare-runs")
def compare_runs(run_ids: List[str]):
    comparison = []
    for run_id in run_ids:
        for runs in runs_db.values():
            for run in runs:
                if run.id == run_id:
                    comparison.append({
                        "run_id": run.id,
                        "name": run.name,
                        "parameters": run.parameters,
                        "metrics": run.metrics,
                        "duration_seconds": run.duration_seconds
                    })
                    break
    
    if not comparison:
        raise HTTPException(status_code=404, detail="No runs found")
    
    return {"runs": comparison, "count": len(comparison)}

@app.post("/compare-models")
def compare_models(model_ids: List[str]):
    comparison = []
    for model_id in model_ids:
        if model_id in models_db:
            model = models_db[model_id]
            comparison.append({
                "model_id": model.id,
                "name": model.name,
                "version": model.version,
                "framework": model.framework,
                "metrics": model.metrics,
                "size_bytes": model.size_bytes
            })
    
    if not comparison:
        raise HTTPException(status_code=404, detail="No models found")
    
    return {"models": comparison, "count": len(comparison)}

@app.get("/experiments/{experiment_id}/summary")
def get_experiment_summary(experiment_id: str):
    if experiment_id not in experiments_db:
        raise HTTPException(status_code=404, detail="Experiment not found")
    
    experiment = experiments_db[experiment_id]
    runs = runs_db.get(experiment_id, [])
    
    return {
        "experiment": experiment,
        "total_runs": len(runs),
        "completed_runs": len([r for r in runs if r.status == ExperimentStatus.COMPLETED]),
        "failed_runs": len([r for r in runs if r.status == ExperimentStatus.FAILED]),
        "best_run": max(runs, key=lambda r: r.metrics.get("accuracy", 0)) if runs else None,
        "average_duration": sum([r.duration_seconds or 0 for r in runs]) / len(runs) if runs else 0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
