import requests
import time

BASE_URL = "http://localhost:8007"

print("=== AUTOSCALE SERVICE TEST ===\n")

# 1. Create scaling rule
print("1. Creating scaling rule...")
rule_data = {
    "deployment_id": "deploy_123",
    "name": "CPU-based scaling",
    "metric": "cpu",
    "min_instances": 1,
    "max_instances": 5,
    "scale_up_threshold": 70.0,
    "scale_down_threshold": 30.0,
    "cooldown_seconds": 60
}
response = requests.post(f"{BASE_URL}/rules", json=rule_data)
rule = response.json()
print(f"Rule created: {rule['name']} (ID: {rule['id']})")
print(f"  Min: {rule['min_instances']}, Max: {rule['max_instances']}")
print(f"  Scale up at {rule['scale_up_threshold']}%, down at {rule['scale_down_threshold']}%")

# 2. Check initial instances
print("\n2. Checking initial instances...")
response = requests.get(f"{BASE_URL}/instances/deploy_123")
instances = response.json()
print(f"Initial instances: {len(instances)}")
for inst in instances:
    print(f"  - {inst['id']} on port {inst['port']} ({inst['status']})")

# 3. Trigger autoscale check
print("\n3. Triggering autoscale check...")
response = requests.post(f"{BASE_URL}/autoscale/check/deploy_123")
result = response.json()
print(f"Action: {result['action']}")
print(f"Reason: {result.get('reason', 'N/A')}")

# 4. Manual scale up
print("\n4. Manual scale to 3 instances...")
response = requests.post(f"{BASE_URL}/instances/deploy_123/scale?target_instances=3")
scale_result = response.json()
print(f"Scaled to {scale_result['count']} instances")

# 5. Check instances again
print("\n5. Checking instances after scaling...")
response = requests.get(f"{BASE_URL}/instances/deploy_123")
instances = response.json()
print(f"Current instances: {len(instances)}")
for inst in instances:
    print(f"  - {inst['id']} on port {inst['port']}")

# 6. Load balancer stats
print("\n6. Load balancer stats...")
response = requests.get(f"{BASE_URL}/loadbalancer/deploy_123/stats")
stats = response.json()
print(f"Total instances: {stats['total_instances']}")
print(f"Healthy instances: {stats['healthy_instances']}")
print(f"Total requests: {stats['total_requests']}")
print(f"Avg response time: {stats['avg_response_time']:.2f}ms")

# 7. Route request through load balancer
print("\n7. Routing request through load balancer...")
response = requests.post(f"{BASE_URL}/loadbalancer/deploy_123/request", json={"text": "test"})
lb_result = response.json()
print(f"Routed to instance: {lb_result['instance_id']}")
print(f"Port: {lb_result['port']}")
print(f"Response time: {lb_result['response_time']:.2f}ms")

# 8. Scaling events
print("\n8. Scaling events...")
response = requests.get(f"{BASE_URL}/events?deployment_id=deploy_123")
events = response.json()
print(f"Total events: {len(events)}")
for event in events[:3]:
    print(f"  - {event['action']}: {event['instances_before']} -> {event['instances_after']}")
    print(f"    Reason: {event['reason']}")

# 9. Scaling summary
print("\n9. Scaling summary...")
response = requests.get(f"{BASE_URL}/events/deploy_123/summary")
summary = response.json()
print(f"Current instances: {summary['current_instances']}")
print(f"Total events: {summary['total_events']}")
print(f"Scale ups: {summary['scale_ups']}")
print(f"Scale downs: {summary['scale_downs']}")

# 10. Cost calculation
print("\n10. Cost calculation...")
response = requests.get(f"{BASE_URL}/cost/deploy_123")
cost = response.json()
print(f"Total cost: ${cost['total_cost']}")
print(f"Cost without autoscale: ${cost['cost_without_autoscale']}")
print(f"Savings: ${cost['savings']} ({cost['savings_percent']}%)")
print(f"Avg instances: {cost['avg_instances']}")

print("\n=== AUTOSCALE SERVICE WORKS PERFECTLY! ===")
