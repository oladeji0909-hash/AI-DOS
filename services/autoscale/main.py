from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from enum import Enum
import uuid
import random

app = FastAPI(title="AI-DOS AutoScale Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enums
class ScalingMetric(str, Enum):
    CPU = "cpu"
    MEMORY = "memory"
    REQUEST_RATE = "request_rate"
    RESPONSE_TIME = "response_time"

class ScalingAction(str, Enum):
    SCALE_UP = "scale_up"
    SCALE_DOWN = "scale_down"
    NO_ACTION = "no_action"

# Models
class ScalingRule(BaseModel):
    id: Optional[str] = None
    deployment_id: str
    name: str
    metric: ScalingMetric
    min_instances: int = 1
    max_instances: int = 10
    scale_up_threshold: float
    scale_down_threshold: float
    cooldown_seconds: int = 300
    enabled: bool = True
    created_at: Optional[str] = None

class Instance(BaseModel):
    id: str
    deployment_id: str
    port: int
    status: str
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    request_count: int = 0
    avg_response_time: float = 0.0
    started_at: str
    health_check_url: str

class ScalingEvent(BaseModel):
    id: str
    deployment_id: str
    rule_id: str
    action: ScalingAction
    reason: str
    instances_before: int
    instances_after: int
    metric_value: float
    timestamp: str

class LoadBalancerStats(BaseModel):
    deployment_id: str
    total_instances: int
    healthy_instances: int
    total_requests: int
    avg_response_time: float
    requests_per_second: float

# Storage
scaling_rules = {}
instances = {}
scaling_events = []
deployment_metrics = {}

@app.get("/")
def root():
    return {
        "service": "AI-DOS AutoScale Service",
        "version": "1.0.0",
        "status": "running",
        "features": [
            "auto_scaling",
            "load_balancing",
            "health_checks",
            "cost_optimization",
            "scaling_history"
        ]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "autoscale"}

# Scaling Rules
@app.post("/rules")
def create_scaling_rule(rule: ScalingRule):
    rule.id = f"rule_{uuid.uuid4().hex[:8]}"
    rule.created_at = datetime.utcnow().isoformat()
    scaling_rules[rule.id] = rule
    
    # Initialize instances for deployment
    if rule.deployment_id not in instances:
        instances[rule.deployment_id] = []
        # Create initial instance
        instance = Instance(
            id=f"instance_{uuid.uuid4().hex[:8]}",
            deployment_id=rule.deployment_id,
            port=10000 + len(instances),
            status="running",
            started_at=datetime.utcnow().isoformat(),
            health_check_url=f"http://localhost:{10000 + len(instances)}/health"
        )
        instances[rule.deployment_id].append(instance)
    
    return rule

@app.get("/rules")
def list_scaling_rules(deployment_id: Optional[str] = None):
    rules = list(scaling_rules.values())
    if deployment_id:
        rules = [r for r in rules if r.deployment_id == deployment_id]
    return rules

@app.get("/rules/{rule_id}")
def get_scaling_rule(rule_id: str):
    if rule_id not in scaling_rules:
        raise HTTPException(status_code=404, detail="Scaling rule not found")
    return scaling_rules[rule_id]

@app.put("/rules/{rule_id}/toggle")
def toggle_scaling_rule(rule_id: str, enabled: bool):
    if rule_id not in scaling_rules:
        raise HTTPException(status_code=404, detail="Scaling rule not found")
    scaling_rules[rule_id].enabled = enabled
    return scaling_rules[rule_id]

@app.delete("/rules/{rule_id}")
def delete_scaling_rule(rule_id: str):
    if rule_id not in scaling_rules:
        raise HTTPException(status_code=404, detail="Scaling rule not found")
    del scaling_rules[rule_id]
    return {"message": "Scaling rule deleted"}

# Instances
@app.get("/instances/{deployment_id}")
def get_instances(deployment_id: str):
    return instances.get(deployment_id, [])

@app.post("/instances/{deployment_id}/scale")
def manual_scale(deployment_id: str, target_instances: int):
    if deployment_id not in instances:
        raise HTTPException(status_code=404, detail="Deployment not found")
    
    current_count = len(instances[deployment_id])
    
    if target_instances > current_count:
        # Scale up
        for _ in range(target_instances - current_count):
            instance = Instance(
                id=f"instance_{uuid.uuid4().hex[:8]}",
                deployment_id=deployment_id,
                port=10000 + len(instances[deployment_id]),
                status="running",
                started_at=datetime.utcnow().isoformat(),
                health_check_url=f"http://localhost:{10000 + len(instances[deployment_id])}/health"
            )
            instances[deployment_id].append(instance)
        
        event = ScalingEvent(
            id=f"event_{uuid.uuid4().hex[:8]}",
            deployment_id=deployment_id,
            rule_id="manual",
            action=ScalingAction.SCALE_UP,
            reason="Manual scaling",
            instances_before=current_count,
            instances_after=target_instances,
            metric_value=0.0,
            timestamp=datetime.utcnow().isoformat()
        )
        scaling_events.append(event)
    
    elif target_instances < current_count:
        # Scale down
        instances[deployment_id] = instances[deployment_id][:target_instances]
        
        event = ScalingEvent(
            id=f"event_{uuid.uuid4().hex[:8]}",
            deployment_id=deployment_id,
            rule_id="manual",
            action=ScalingAction.SCALE_DOWN,
            reason="Manual scaling",
            instances_before=current_count,
            instances_after=target_instances,
            metric_value=0.0,
            timestamp=datetime.utcnow().isoformat()
        )
        scaling_events.append(event)
    
    return {"instances": instances[deployment_id], "count": len(instances[deployment_id])}

# Auto-scaling Engine
@app.post("/autoscale/check/{deployment_id}")
def check_autoscale(deployment_id: str):
    if deployment_id not in instances:
        raise HTTPException(status_code=404, detail="Deployment not found")
    
    # Get active rules for deployment
    active_rules = [r for r in scaling_rules.values() 
                   if r.deployment_id == deployment_id and r.enabled]
    
    if not active_rules:
        return {"action": ScalingAction.NO_ACTION, "reason": "No active rules"}
    
    rule = active_rules[0]
    current_instances = len(instances[deployment_id])
    
    # Simulate metrics
    if deployment_id not in deployment_metrics:
        deployment_metrics[deployment_id] = {
            "cpu": random.uniform(20, 90),
            "memory": random.uniform(30, 80),
            "request_rate": random.uniform(10, 200),
            "response_time": random.uniform(50, 500)
        }
    
    metric_value = deployment_metrics[deployment_id].get(rule.metric, 50.0)
    
    # Check scaling conditions
    if metric_value > rule.scale_up_threshold and current_instances < rule.max_instances:
        # Scale up
        instance = Instance(
            id=f"instance_{uuid.uuid4().hex[:8]}",
            deployment_id=deployment_id,
            port=10000 + current_instances,
            status="running",
            cpu_usage=metric_value if rule.metric == ScalingMetric.CPU else 0.0,
            started_at=datetime.utcnow().isoformat(),
            health_check_url=f"http://localhost:{10000 + current_instances}/health"
        )
        instances[deployment_id].append(instance)
        
        event = ScalingEvent(
            id=f"event_{uuid.uuid4().hex[:8]}",
            deployment_id=deployment_id,
            rule_id=rule.id,
            action=ScalingAction.SCALE_UP,
            reason=f"{rule.metric} ({metric_value:.1f}%) exceeded threshold ({rule.scale_up_threshold}%)",
            instances_before=current_instances,
            instances_after=current_instances + 1,
            metric_value=metric_value,
            timestamp=datetime.utcnow().isoformat()
        )
        scaling_events.append(event)
        
        return {"action": ScalingAction.SCALE_UP, "event": event}
    
    elif metric_value < rule.scale_down_threshold and current_instances > rule.min_instances:
        # Scale down
        instances[deployment_id] = instances[deployment_id][:-1]
        
        event = ScalingEvent(
            id=f"event_{uuid.uuid4().hex[:8]}",
            deployment_id=deployment_id,
            rule_id=rule.id,
            action=ScalingAction.SCALE_DOWN,
            reason=f"{rule.metric} ({metric_value:.1f}%) below threshold ({rule.scale_down_threshold}%)",
            instances_before=current_instances,
            instances_after=current_instances - 1,
            metric_value=metric_value,
            timestamp=datetime.utcnow().isoformat()
        )
        scaling_events.append(event)
        
        return {"action": ScalingAction.SCALE_DOWN, "event": event}
    
    return {
        "action": ScalingAction.NO_ACTION,
        "reason": f"{rule.metric} ({metric_value:.1f}%) within thresholds",
        "current_instances": current_instances
    }

# Load Balancer
@app.get("/loadbalancer/{deployment_id}/stats")
def get_load_balancer_stats(deployment_id: str):
    if deployment_id not in instances:
        raise HTTPException(status_code=404, detail="Deployment not found")
    
    deployment_instances = instances[deployment_id]
    healthy = [i for i in deployment_instances if i.status == "running"]
    
    total_requests = sum(i.request_count for i in deployment_instances)
    avg_response = sum(i.avg_response_time for i in deployment_instances) / len(deployment_instances) if deployment_instances else 0
    
    return LoadBalancerStats(
        deployment_id=deployment_id,
        total_instances=len(deployment_instances),
        healthy_instances=len(healthy),
        total_requests=total_requests,
        avg_response_time=avg_response,
        requests_per_second=total_requests / 60.0
    )

@app.post("/loadbalancer/{deployment_id}/request")
def route_request(deployment_id: str, request_data: Dict):
    if deployment_id not in instances:
        raise HTTPException(status_code=404, detail="Deployment not found")
    
    healthy_instances = [i for i in instances[deployment_id] if i.status == "running"]
    
    if not healthy_instances:
        raise HTTPException(status_code=503, detail="No healthy instances available")
    
    # Round-robin load balancing
    selected = healthy_instances[0]
    selected.request_count += 1
    selected.avg_response_time = random.uniform(50, 200)
    
    return {
        "instance_id": selected.id,
        "port": selected.port,
        "response_time": selected.avg_response_time,
        "prediction": "positive",
        "confidence": 0.95
    }

# Scaling History
@app.get("/events")
def get_scaling_events(deployment_id: Optional[str] = None, limit: int = 50):
    events = scaling_events
    if deployment_id:
        events = [e for e in events if e.deployment_id == deployment_id]
    return sorted(events, key=lambda x: x.timestamp, reverse=True)[:limit]

@app.get("/events/{deployment_id}/summary")
def get_scaling_summary(deployment_id: str):
    deployment_events = [e for e in scaling_events if e.deployment_id == deployment_id]
    
    scale_ups = len([e for e in deployment_events if e.action == ScalingAction.SCALE_UP])
    scale_downs = len([e for e in deployment_events if e.action == ScalingAction.SCALE_DOWN])
    
    current_instances = len(instances.get(deployment_id, []))
    
    return {
        "deployment_id": deployment_id,
        "current_instances": current_instances,
        "total_events": len(deployment_events),
        "scale_ups": scale_ups,
        "scale_downs": scale_downs,
        "last_event": deployment_events[-1] if deployment_events else None
    }

# Cost Calculator
@app.get("/cost/{deployment_id}")
def calculate_cost(deployment_id: str):
    if deployment_id not in instances:
        raise HTTPException(status_code=404, detail="Deployment not found")
    
    deployment_events = [e for e in scaling_events if e.deployment_id == deployment_id]
    
    # Calculate average instances over time
    total_instance_hours = 0
    for i, event in enumerate(deployment_events):
        if i < len(deployment_events) - 1:
            duration = 1  # Simplified: 1 hour per event
            total_instance_hours += event.instances_after * duration
    
    cost_per_instance_hour = 0.10  # $0.10 per instance per hour
    total_cost = total_instance_hours * cost_per_instance_hour
    
    # Calculate cost without autoscaling (max instances always)
    rules = [r for r in scaling_rules.values() if r.deployment_id == deployment_id]
    max_instances = rules[0].max_instances if rules else 10
    cost_without_autoscale = max_instances * len(deployment_events) * cost_per_instance_hour
    
    savings = cost_without_autoscale - total_cost
    savings_percent = (savings / cost_without_autoscale * 100) if cost_without_autoscale > 0 else 0
    
    return {
        "deployment_id": deployment_id,
        "total_cost": round(total_cost, 2),
        "cost_without_autoscale": round(cost_without_autoscale, 2),
        "savings": round(savings, 2),
        "savings_percent": round(savings_percent, 1),
        "avg_instances": round(total_instance_hours / len(deployment_events), 1) if deployment_events else 0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
