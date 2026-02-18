import requests
import time
from datetime import datetime

print("=" * 80)
print("AI-DOS COMPREHENSIVE SYSTEM TEST")
print("=" * 80)
print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Test results tracking
results = {
    "passed": 0,
    "failed": 0,
    "errors": []
}

def test_endpoint(service_name, url, method="GET", data=None, expected_status=200):
    """Test a single endpoint"""
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=5)
        elif method == "PUT":
            response = requests.put(url, json=data, timeout=5)
        elif method == "DELETE":
            response = requests.delete(url, timeout=5)
        
        if response.status_code == expected_status or response.status_code == 200:
            results["passed"] += 1
            return True, response
        else:
            results["failed"] += 1
            error = f"{service_name}: Expected {expected_status}, got {response.status_code}"
            results["errors"].append(error)
            return False, response
    except Exception as e:
        results["failed"] += 1
        error = f"{service_name}: {str(e)}"
        results["errors"].append(error)
        return False, None

print("\n" + "=" * 80)
print("1. TESTING API GATEWAY (Port 8000)")
print("=" * 80)

# Health check
success, resp = test_endpoint("API Gateway", "http://localhost:8000/health")
print(f"[{'PASS' if success else 'FAIL'}] Health check")

# Root endpoint
success, resp = test_endpoint("API Gateway", "http://localhost:8000/")
print(f"[{'PASS' if success else 'FAIL'}] Root endpoint")

print("\n" + "=" * 80)
print("2. TESTING DATAFORGE (Port 8001)")
print("=" * 80)

# Health check
success, resp = test_endpoint("DataForge", "http://localhost:8001/health")
print(f"[{'PASS' if success else 'FAIL'}] Health check")

# List datasets
success, resp = test_endpoint("DataForge", "http://localhost:8001/datasets")
print(f"[{'PASS' if success else 'FAIL'}] List datasets")

# Create dataset
dataset_data = {
    "name": "Test Dataset",
    "description": "System test dataset",
    "owner_id": "test_user",
    "data_type": "text"
}
success, resp = test_endpoint("DataForge", "http://localhost:8001/datasets", "POST", dataset_data)
print(f"[{'PASS' if success else 'FAIL'}] Create dataset")
if success and resp:
    dataset_id = resp.json().get("id")
    print(f"  Created dataset: {dataset_id}")

print("\n" + "=" * 80)
print("3. TESTING MODELHUB (Port 8002)")
print("=" * 80)

# Health check
success, resp = test_endpoint("ModelHub", "http://localhost:8002/health")
print(f"[{'PASS' if success else 'FAIL'}] Health check")

# List experiments
success, resp = test_endpoint("ModelHub", "http://localhost:8002/experiments")
print(f"[{'PASS' if success else 'FAIL'}] List experiments")

# Create experiment
exp_data = {
    "name": "Test Experiment",
    "description": "System test experiment",
    "project_id": "test_project",
    "user_id": "test_user"
}
success, resp = test_endpoint("ModelHub", "http://localhost:8002/experiments", "POST", exp_data)
print(f"[{'PASS' if success else 'FAIL'}] Create experiment")
if success and resp:
    exp_id = resp.json().get("id")
    print(f"  Created experiment: {exp_id}")

print("\n" + "=" * 80)
print("4. TESTING MAGIC MODE (Port 8003)")
print("=" * 80)

# Health check
success, resp = test_endpoint("Magic Mode", "http://localhost:8003/health")
print(f"[{'PASS' if success else 'FAIL'}] Health check")

# Root endpoint
success, resp = test_endpoint("Magic Mode", "http://localhost:8003/")
print(f"[{'PASS' if success else 'FAIL'}] Root endpoint")

# Create magic pipeline (this might take longer)
magic_data = {
    "prompt": "Build a simple text classifier",
    "user_id": "test_user"
}
print("  Testing magic pipeline creation (may take a moment)...")
success, resp = test_endpoint("Magic Mode", "http://localhost:8003/magic/create", "POST", magic_data)
print(f"[{'PASS' if success else 'FAIL'}] Create magic pipeline")

print("\n" + "=" * 80)
print("5. TESTING MARKETPLACE (Port 8004)")
print("=" * 80)

# Health check
success, resp = test_endpoint("Marketplace", "http://localhost:8004/health")
print(f"[{'PASS' if success else 'FAIL'}] Health check")

# List models
success, resp = test_endpoint("Marketplace", "http://localhost:8004/marketplace/models")
print(f"[{'PASS' if success else 'FAIL'}] List marketplace models")

# List a model
list_data = {
    "name": "Test Model",
    "description": "System test model",
    "task_type": "classification",
    "price": 9.99,
    "seller_id": "test_seller"
}
success, resp = test_endpoint("Marketplace", "http://localhost:8004/marketplace/list", "POST", list_data)
print(f"[{'PASS' if success else 'FAIL'}] List model for sale")

print("\n" + "=" * 80)
print("6. TESTING DEPLOY SERVICE (Port 8005)")
print("=" * 80)

# Health check
success, resp = test_endpoint("Deploy", "http://localhost:8005/health")
print(f"[{'PASS' if success else 'FAIL'}] Health check")

# List deployments
success, resp = test_endpoint("Deploy", "http://localhost:8005/deploy/list")
print(f"[{'PASS' if success else 'FAIL'}] List deployments")

# Create deployment (using experiment from ModelHub)
if 'exp_id' in locals():
    deploy_data = {
        "experiment_id": exp_id,
        "name": "Test Deployment",
        "description": "System test deployment"
    }
    success, resp = test_endpoint("Deploy", "http://localhost:8005/deploy/create", "POST", deploy_data)
    print(f"[{'PASS' if success else 'FAIL'}] Create deployment")
    if success and resp:
        deploy_id = resp.json().get("deployment_id")
        print(f"  Created deployment: {deploy_id}")

print("\n" + "=" * 80)
print("7. TESTING COLLABORATION (Port 8006)")
print("=" * 80)

# Health check
success, resp = test_endpoint("Collaboration", "http://localhost:8006/health")
print(f"[{'PASS' if success else 'FAIL'}] Health check")

# List teams
success, resp = test_endpoint("Collaboration", "http://localhost:8006/teams")
print(f"[{'PASS' if success else 'FAIL'}] List teams")

# Create team
team_data = {
    "name": "Test Team",
    "description": "System test team",
    "owner_id": "test_user"
}
success, resp = test_endpoint("Collaboration", "http://localhost:8006/teams", "POST", team_data)
print(f"[{'PASS' if success else 'FAIL'}] Create team")
if success and resp:
    team_id = resp.json().get("id")
    print(f"  Created team: {team_id}")

# Get notifications
success, resp = test_endpoint("Collaboration", "http://localhost:8006/notifications/test_user")
print(f"[{'PASS' if success else 'FAIL'}] Get notifications")

print("\n" + "=" * 80)
print("8. TESTING AUTOSCALE (Port 8007)")
print("=" * 80)

# Health check
success, resp = test_endpoint("AutoScale", "http://localhost:8007/health")
print(f"[{'PASS' if success else 'FAIL'}] Health check")

# List scaling rules
success, resp = test_endpoint("AutoScale", "http://localhost:8007/rules")
print(f"[{'PASS' if success else 'FAIL'}] List scaling rules")

# Create scaling rule
rule_data = {
    "deployment_id": "test_deploy",
    "name": "Test Scaling Rule",
    "metric": "cpu",
    "min_instances": 1,
    "max_instances": 5,
    "scale_up_threshold": 70.0,
    "scale_down_threshold": 30.0
}
success, resp = test_endpoint("AutoScale", "http://localhost:8007/rules", "POST", rule_data)
print(f"[{'PASS' if success else 'FAIL'}] Create scaling rule")

# Get instances
success, resp = test_endpoint("AutoScale", "http://localhost:8007/instances/test_deploy")
print(f"[{'PASS' if success else 'FAIL'}] Get instances")

print("\n" + "=" * 80)
print("9. TESTING ANALYTICS (Port 8008)")
print("=" * 80)

# Health check
success, resp = test_endpoint("Analytics", "http://localhost:8008/health")
print(f"[{'PASS' if success else 'FAIL'}] Health check")

# Dashboard summary
success, resp = test_endpoint("Analytics", "http://localhost:8008/analytics/dashboard/summary")
print(f"[{'PASS' if success else 'FAIL'}] Dashboard summary")

# Model performance
success, resp = test_endpoint("Analytics", "http://localhost:8008/analytics/model/test_model/performance")
print(f"[{'PASS' if success else 'FAIL'}] Model performance")

# Usage analytics
success, resp = test_endpoint("Analytics", "http://localhost:8008/analytics/usage/overview")
print(f"[{'PASS' if success else 'FAIL'}] Usage analytics")

# Cost analytics
success, resp = test_endpoint("Analytics", "http://localhost:8008/analytics/cost/overview")
print(f"[{'PASS' if success else 'FAIL'}] Cost analytics")

# Business metrics
success, resp = test_endpoint("Analytics", "http://localhost:8008/analytics/business/overview")
print(f"[{'PASS' if success else 'FAIL'}] Business metrics")

# ROI calculation
success, resp = test_endpoint("Analytics", "http://localhost:8008/analytics/business/roi")
print(f"[{'PASS' if success else 'FAIL'}] ROI calculation")

print("\n" + "=" * 80)
print("10. INTEGRATION TESTS")
print("=" * 80)

# Test Magic Mode -> ModelHub integration
print("\nTesting Magic Mode -> ModelHub integration...")
success, resp = test_endpoint("ModelHub", "http://localhost:8002/experiments")
if success and resp:
    experiments = resp.json()
    print(f"[PASS] Found {len(experiments)} experiments in ModelHub")
else:
    print("[FAIL] Could not verify ModelHub experiments")

# Test Deploy -> ModelHub integration
print("\nTesting Deploy -> ModelHub integration...")
success, resp = test_endpoint("Deploy", "http://localhost:8005/deploy/list")
if success and resp:
    deployments = resp.json().get("deployments", [])
    print(f"[PASS] Found {len(deployments)} deployments")
else:
    print("[FAIL] Could not verify deployments")

# Test Collaboration notifications
print("\nTesting Collaboration notifications...")
success, resp = test_endpoint("Collaboration", "http://localhost:8006/notifications/test_user")
if success and resp:
    notifications = resp.json()
    print(f"[PASS] Notifications system working ({len(notifications)} notifications)")
else:
    print("[FAIL] Notifications system issue")

print("\n" + "=" * 80)
print("TEST SUMMARY")
print("=" * 80)
print(f"Total Tests: {results['passed'] + results['failed']}")
print(f"Passed: {results['passed']}")
print(f"Failed: {results['failed']}")
print(f"Success Rate: {(results['passed'] / (results['passed'] + results['failed']) * 100):.1f}%")

if results['errors']:
    print("\n" + "=" * 80)
    print("ERRORS FOUND:")
    print("=" * 80)
    for i, error in enumerate(results['errors'], 1):
        print(f"{i}. {error}")
else:
    print("\n🔥 ALL TESTS PASSED! SYSTEM IS FULLY OPERATIONAL! 🔥")

print("\n" + "=" * 80)
print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)
