from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from enum import Enum
import random
import uuid

app = FastAPI(title="AI-DOS Analytics Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enums
class ReportFormat(str, Enum):
    PDF = "pdf"
    CSV = "csv"
    JSON = "json"

class TimeRange(str, Enum):
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"

# Models
class ModelPerformance(BaseModel):
    model_id: str
    accuracy_trend: List[Dict]
    predictions_per_day: List[Dict]
    avg_response_time: float
    total_predictions: int
    error_rate: float

class ExperimentComparison(BaseModel):
    experiment_ids: List[str]
    metrics: Dict[str, List[float]]
    best_experiment: str
    comparison_chart: Dict

class UsageAnalytics(BaseModel):
    total_users: int
    active_users: int
    total_api_calls: int
    most_used_models: List[Dict]
    peak_hours: List[int]
    user_growth: List[Dict]

class CostAnalytics(BaseModel):
    total_cost: float
    cost_by_service: Dict[str, float]
    cost_trend: List[Dict]
    cost_per_prediction: float
    savings_from_autoscale: float

class BusinessMetrics(BaseModel):
    marketplace_revenue: float
    total_deployments: int
    total_experiments: int
    total_datasets: int
    revenue_trend: List[Dict]
    top_sellers: List[Dict]

# Storage
analytics_data = {
    "models": {},
    "experiments": {},
    "usage": {},
    "costs": {},
    "business": {}
}

@app.get("/")
def root():
    return {
        "service": "AI-DOS Analytics Service",
        "version": "1.0.0",
        "status": "running",
        "features": [
            "model_performance",
            "experiment_comparison",
            "usage_analytics",
            "cost_analytics",
            "business_intelligence",
            "custom_reports"
        ]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "analytics"}

# Model Performance Analytics
@app.get("/analytics/model/{model_id}/performance")
def get_model_performance(model_id: str, time_range: TimeRange = TimeRange.WEEK):
    # Generate mock data
    days = {"hour": 1, "day": 1, "week": 7, "month": 30, "year": 365}[time_range]
    
    accuracy_trend = []
    predictions_per_day = []
    
    for i in range(days):
        date = (datetime.utcnow() - timedelta(days=days-i-1)).strftime("%Y-%m-%d")
        accuracy_trend.append({
            "date": date,
            "accuracy": round(random.uniform(0.85, 0.95), 3)
        })
        predictions_per_day.append({
            "date": date,
            "predictions": random.randint(100, 1000)
        })
    
    return ModelPerformance(
        model_id=model_id,
        accuracy_trend=accuracy_trend,
        predictions_per_day=predictions_per_day,
        avg_response_time=round(random.uniform(50, 200), 2),
        total_predictions=sum(p["predictions"] for p in predictions_per_day),
        error_rate=round(random.uniform(0.01, 0.05), 3)
    )

@app.get("/analytics/model/{model_id}/confusion-matrix")
def get_confusion_matrix(model_id: str):
    # Generate mock confusion matrix
    return {
        "model_id": model_id,
        "matrix": [
            [850, 50, 30, 20],
            [40, 880, 45, 35],
            [25, 55, 890, 30],
            [15, 35, 25, 925]
        ],
        "labels": ["Class A", "Class B", "Class C", "Class D"],
        "accuracy": 0.912,
        "precision": 0.908,
        "recall": 0.915,
        "f1_score": 0.911
    }

# Experiment Comparison
@app.post("/analytics/experiments/compare")
def compare_experiments(experiment_ids: List[str]):
    metrics = {
        "accuracy": [round(random.uniform(0.80, 0.95), 3) for _ in experiment_ids],
        "precision": [round(random.uniform(0.78, 0.93), 3) for _ in experiment_ids],
        "recall": [round(random.uniform(0.79, 0.94), 3) for _ in experiment_ids],
        "f1_score": [round(random.uniform(0.80, 0.93), 3) for _ in experiment_ids],
        "training_time": [round(random.uniform(100, 500), 1) for _ in experiment_ids]
    }
    
    best_idx = metrics["accuracy"].index(max(metrics["accuracy"]))
    
    return ExperimentComparison(
        experiment_ids=experiment_ids,
        metrics=metrics,
        best_experiment=experiment_ids[best_idx],
        comparison_chart={
            "type": "bar",
            "data": metrics,
            "labels": experiment_ids
        }
    )

@app.get("/analytics/experiments/{experiment_id}/metrics-over-time")
def get_experiment_metrics_over_time(experiment_id: str):
    epochs = 50
    metrics_over_time = []
    
    for epoch in range(1, epochs + 1):
        metrics_over_time.append({
            "epoch": epoch,
            "train_loss": round(1.0 - (epoch / epochs) * 0.8 + random.uniform(-0.05, 0.05), 4),
            "val_loss": round(1.0 - (epoch / epochs) * 0.75 + random.uniform(-0.05, 0.05), 4),
            "train_accuracy": round((epoch / epochs) * 0.9 + random.uniform(-0.02, 0.02), 4),
            "val_accuracy": round((epoch / epochs) * 0.85 + random.uniform(-0.02, 0.02), 4)
        })
    
    return {
        "experiment_id": experiment_id,
        "metrics": metrics_over_time,
        "total_epochs": epochs
    }

# Usage Analytics
@app.get("/analytics/usage/overview")
def get_usage_overview(time_range: TimeRange = TimeRange.WEEK):
    days = {"hour": 1, "day": 1, "week": 7, "month": 30, "year": 365}[time_range]
    
    user_growth = []
    for i in range(days):
        date = (datetime.utcnow() - timedelta(days=days-i-1)).strftime("%Y-%m-%d")
        user_growth.append({
            "date": date,
            "users": 100 + i * 5 + random.randint(-2, 5)
        })
    
    return UsageAnalytics(
        total_users=500 + random.randint(0, 100),
        active_users=250 + random.randint(0, 50),
        total_api_calls=50000 + random.randint(0, 10000),
        most_used_models=[
            {"model_id": "model_1", "name": "Sentiment Analyzer", "calls": 15000},
            {"model_id": "model_2", "name": "Image Classifier", "calls": 12000},
            {"model_id": "model_3", "name": "Text Generator", "calls": 8000}
        ],
        peak_hours=[9, 10, 11, 14, 15, 16],
        user_growth=user_growth
    )

@app.get("/analytics/usage/api-calls")
def get_api_calls_analytics(time_range: TimeRange = TimeRange.DAY):
    hours = {"hour": 1, "day": 24, "week": 168, "month": 720, "year": 8760}[time_range]
    
    api_calls = []
    for i in range(min(hours, 100)):
        timestamp = (datetime.utcnow() - timedelta(hours=hours-i-1)).strftime("%Y-%m-%d %H:00")
        api_calls.append({
            "timestamp": timestamp,
            "calls": random.randint(50, 500),
            "errors": random.randint(0, 10),
            "avg_response_time": round(random.uniform(50, 200), 2)
        })
    
    return {
        "time_range": time_range,
        "data": api_calls,
        "total_calls": sum(c["calls"] for c in api_calls),
        "total_errors": sum(c["errors"] for c in api_calls),
        "avg_response_time": round(sum(c["avg_response_time"] for c in api_calls) / len(api_calls), 2)
    }

# Cost Analytics
@app.get("/analytics/cost/overview")
def get_cost_overview(time_range: TimeRange = TimeRange.MONTH):
    days = {"hour": 1, "day": 1, "week": 7, "month": 30, "year": 365}[time_range]
    
    cost_trend = []
    for i in range(days):
        date = (datetime.utcnow() - timedelta(days=days-i-1)).strftime("%Y-%m-%d")
        cost_trend.append({
            "date": date,
            "cost": round(random.uniform(10, 50), 2)
        })
    
    return CostAnalytics(
        total_cost=round(sum(c["cost"] for c in cost_trend), 2),
        cost_by_service={
            "compute": round(random.uniform(200, 400), 2),
            "storage": round(random.uniform(50, 100), 2),
            "network": round(random.uniform(30, 60), 2),
            "database": round(random.uniform(40, 80), 2)
        },
        cost_trend=cost_trend,
        cost_per_prediction=round(random.uniform(0.001, 0.01), 4),
        savings_from_autoscale=round(random.uniform(100, 300), 2)
    )

@app.get("/analytics/cost/predictions")
def get_cost_predictions(months: int = 3):
    predictions = []
    for i in range(1, months + 1):
        month = (datetime.utcnow() + timedelta(days=30*i)).strftime("%Y-%m")
        predictions.append({
            "month": month,
            "predicted_cost": round(random.uniform(500, 1000), 2),
            "confidence": round(random.uniform(0.80, 0.95), 2)
        })
    
    return {
        "predictions": predictions,
        "total_predicted": round(sum(p["predicted_cost"] for p in predictions), 2)
    }

# Business Metrics
@app.get("/analytics/business/overview")
def get_business_overview(time_range: TimeRange = TimeRange.MONTH):
    days = {"hour": 1, "day": 1, "week": 7, "month": 30, "year": 365}[time_range]
    
    revenue_trend = []
    for i in range(days):
        date = (datetime.utcnow() - timedelta(days=days-i-1)).strftime("%Y-%m-%d")
        revenue_trend.append({
            "date": date,
            "revenue": round(random.uniform(50, 200), 2)
        })
    
    return BusinessMetrics(
        marketplace_revenue=round(sum(r["revenue"] for r in revenue_trend), 2),
        total_deployments=random.randint(50, 200),
        total_experiments=random.randint(200, 500),
        total_datasets=random.randint(100, 300),
        revenue_trend=revenue_trend,
        top_sellers=[
            {"user_id": "user_1", "revenue": 1500.50, "models_sold": 25},
            {"user_id": "user_2", "revenue": 1200.30, "models_sold": 20},
            {"user_id": "user_3", "revenue": 980.75, "models_sold": 18}
        ]
    )

@app.get("/analytics/business/roi")
def calculate_roi():
    total_investment = random.uniform(5000, 10000)
    total_revenue = random.uniform(8000, 15000)
    roi = ((total_revenue - total_investment) / total_investment) * 100
    
    return {
        "total_investment": round(total_investment, 2),
        "total_revenue": round(total_revenue, 2),
        "net_profit": round(total_revenue - total_investment, 2),
        "roi_percentage": round(roi, 2),
        "payback_period_months": round(random.uniform(3, 8), 1)
    }

# Custom Reports
@app.post("/analytics/reports/generate")
def generate_report(report_type: str, time_range: TimeRange, format: ReportFormat):
    report_id = f"report_{uuid.uuid4().hex[:8]}"
    
    return {
        "report_id": report_id,
        "type": report_type,
        "time_range": time_range,
        "format": format,
        "status": "generated",
        "download_url": f"/analytics/reports/{report_id}/download",
        "generated_at": datetime.utcnow().isoformat(),
        "size_kb": random.randint(100, 1000)
    }

@app.get("/analytics/reports/{report_id}/download")
def download_report(report_id: str):
    return {
        "report_id": report_id,
        "content": "Report content would be here (PDF/CSV/JSON)",
        "message": "In production, this would return the actual file"
    }

# Dashboard Summary
@app.get("/analytics/dashboard/summary")
def get_dashboard_summary():
    return {
        "total_models": random.randint(50, 150),
        "total_experiments": random.randint(200, 500),
        "total_deployments": random.randint(30, 100),
        "total_predictions_today": random.randint(5000, 15000),
        "avg_model_accuracy": round(random.uniform(0.85, 0.95), 3),
        "total_revenue": round(random.uniform(5000, 15000), 2),
        "active_users": random.randint(100, 300),
        "system_health": "excellent",
        "top_performing_model": {
            "id": "model_123",
            "name": "Sentiment Analyzer Pro",
            "accuracy": 0.952
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
