from aidos import Deploy, ModelHub

# Create experiment
print("Creating experiment...")
mh = ModelHub()
exp = mh.create_experiment(
    name="Image Classifier v2",
    description="ResNet50 for product images",
    project_id="proj_002",
    user_id="user_002"
)
print(f"Experiment created: {exp['id']}")

# Deploy it
print("\nDeploying model...")
deploy = Deploy()
deployment = deploy.create(
    experiment_id=exp['id'],
    name="Product Classifier API",
    description="Production image classification"
)
print(f"Deployed at: {deployment['endpoint_url']}")
print(f"Deployment ID: {deployment['deployment_id']}")

# Make prediction
print("\nMaking prediction...")
result = deploy.predict(
    deployment['deployment_id'],
    {"image_url": "https://example.com/product.jpg"}
)
print(f"Prediction: {result['prediction']} (confidence: {result['confidence']})")

# Check metrics
print("\nChecking metrics...")
metrics = deploy.metrics(deployment['deployment_id'])
print(f"Total requests: {metrics['metrics']['total_requests']}")
print(f"Uptime: {metrics['uptime_seconds']:.1f}s")

# List all deployments
print("\nAll deployments:")
all_deploys = deploy.list()
for d in all_deploys['deployments']:
    print(f"  - {d['name']} ({d['status']}) -> {d['endpoint_url']}")

print("\nDEPLOY SERVICE WORKS PERFECTLY!")
