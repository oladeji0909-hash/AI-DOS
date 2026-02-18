#!/usr/bin/env python3
"""
AI-DOS CLI - Command-line interface for AI-DOS
"""

import sys
import argparse
import requests
import json
from typing import Dict

API_URL = "http://localhost:8000"
MAGIC_URL = "http://localhost:8003"
DATAFORGE_URL = "http://localhost:8001"
MODELHUB_URL = "http://localhost:8002"
DEPLOY_URL = "http://localhost:8005"
COLLAB_URL = "http://localhost:8006"
AUTOSCALE_URL = "http://localhost:8007"
ANALYTICS_URL = "http://localhost:8008"

def magic_create(args):
    """Create ML pipeline with Magic Mode"""
    print(f"🪄 Creating: {args.prompt}")
    print("⏳ Please wait...")
    
    try:
        response = requests.post(
            f"{MAGIC_URL}/magic/create",
            json={
                "prompt": args.prompt,
                "user_id": args.user or "cli-user",
                "auto_deploy": not args.no_deploy
            }
        )
        result = response.json()
        
        print("\n✅ Success!")
        print(f"📦 Dataset ID: {result['dataset_id']}")
        print(f"🧪 Experiment ID: {result['experiment_id']}")
        print(f"🤖 Model ID: {result['model_id']}")
        if result.get('api_endpoint'):
            print(f"🌐 API Endpoint: {result['api_endpoint']}")
        
        if args.show_code:
            print(f"\n📝 Generated Code:\n{result['code']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def dataset_create(args):
    """Create new dataset"""
    print(f"📦 Creating dataset: {args.name}")
    
    try:
        response = requests.post(
            f"{DATAFORGE_URL}/datasets",
            json={
                "name": args.name,
                "description": args.description or "",
                "owner_id": args.user or "cli-user",
                "data_type": args.type
            }
        )
        result = response.json()
        
        print(f"✅ Dataset created!")
        print(f"ID: {result['id']}")
        print(f"Name: {result['name']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def dataset_list(args):
    """List all datasets"""
    try:
        response = requests.get(f"{DATAFORGE_URL}/datasets")
        datasets = response.json()
        
        print(f"\n📦 Datasets ({len(datasets)}):\n")
        for ds in datasets:
            print(f"  • {ds['name']} (ID: {ds['id']})")
            print(f"    Type: {ds['data_type']} | Samples: {ds['num_samples']}")
            print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def experiment_create(args):
    """Create new experiment"""
    print(f"🧪 Creating experiment: {args.name}")
    
    try:
        response = requests.post(
            f"{MODELHUB_URL}/experiments",
            json={
                "name": args.name,
                "description": args.description or "",
                "project_id": args.project or "default",
                "user_id": args.user or "cli-user",
                "tags": args.tags.split(",") if args.tags else []
            }
        )
        result = response.json()
        
        print(f"✅ Experiment created!")
        print(f"ID: {result['id']}")
        print(f"Name: {result['name']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def experiment_list(args):
    """List all experiments"""
    try:
        response = requests.get(f"{MODELHUB_URL}/experiments")
        experiments = response.json()
        
        print(f"\n🧪 Experiments ({len(experiments)}):\n")
        for exp in experiments:
            print(f"  • {exp['name']} (ID: {exp['id']})")
            print(f"    Status: {exp['status']} | Tags: {', '.join(exp.get('tags', []))}")
            print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def status(args):
    """Check AI-DOS status"""
    services = [
        ("API Gateway", f"{API_URL}/health"),
        ("DataForge", f"{DATAFORGE_URL}/health"),
        ("ModelHub", f"{MODELHUB_URL}/health"),
        ("Magic Mode", f"{MAGIC_URL}/health"),
        ("Marketplace", "http://localhost:8004/health"),
        ("Deploy", f"{DEPLOY_URL}/health"),
        ("Collaboration", f"{COLLAB_URL}/health"),
        ("AutoScale", f"{AUTOSCALE_URL}/health"),
        ("Analytics", f"{ANALYTICS_URL}/health"),
    ]
    
    print("\nAI-DOS Status:\n")
    for name, url in services:
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                print(f"  [OK] {name}: Running")
            else:
                print(f"  [ERROR] {name}: Error")
        except:
            print(f"  [DOWN] {name}: Not running")
    print()

def deploy_create(args):
    """Deploy a model"""
    print(f"🚀 Deploying: {args.name}")
    
    try:
        response = requests.post(
            f"{DEPLOY_URL}/deploy/create",
            json={
                "experiment_id": args.experiment_id,
                "name": args.name,
                "description": args.description or ""
            }
        )
        result = response.json()
        
        print(f"✅ Deployed!")
        print(f"Deployment ID: {result['deployment_id']}")
        print(f"Endpoint: {result['endpoint_url']}")
        print(f"Status: {result['status']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def deploy_list(args):
    """List all deployments"""
    try:
        response = requests.get(f"{DEPLOY_URL}/deploy/list")
        result = response.json()
        deployments = result.get('deployments', [])
        
        print(f"\n🚀 Deployments ({result.get('total', 0)}):\n")
        for dep in deployments:
            print(f"  • {dep['name']} (ID: {dep['deployment_id']})")
            print(f"    Status: {dep['status']} | Endpoint: {dep['endpoint_url']}")
            print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def deploy_metrics(args):
    """Get deployment metrics"""
    try:
        response = requests.get(f"{DEPLOY_URL}/deploy/{args.deployment_id}/metrics")
        result = response.json()
        
        print(f"\n📊 Metrics for {args.deployment_id}:\n")
        print(f"  Status: {result['status']}")
        print(f"  Uptime: {result['uptime_seconds']:.1f}s")
        print(f"  Total Requests: {result['metrics']['total_requests']}")
        print(f"  Successful: {result['metrics']['successful_requests']}")
        print(f"  Failed: {result['metrics']['failed_requests']}")
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def team_create(args):
    """Create a team"""
    print(f"👥 Creating team: {args.name}")
    
    try:
        response = requests.post(
            f"{COLLAB_URL}/teams",
            json={
                "name": args.name,
                "description": args.description or "",
                "owner_id": args.user or "cli-user"
            }
        )
        result = response.json()
        
        print(f"✅ Team created!")
        print(f"Team ID: {result['id']}")
        print(f"Name: {result['name']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def share_resource(args):
    """Share a resource"""
    print(f"🤝 Sharing {args.resource_type} {args.resource_id} with {args.user_id}")
    
    try:
        response = requests.post(
            f"{COLLAB_URL}/share",
            json={
                "resource_type": args.resource_type,
                "resource_id": args.resource_id,
                "shared_by": args.shared_by or "cli-user",
                "shared_with": args.user_id,
                "role": args.role,
                "message": args.message
            }
        )
        result = response.json()
        
        print(f"✅ Shared successfully!")
        print(f"Share ID: {result['id']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def autoscale_create(args):
    """Create auto-scaling rule"""
    print(f"⚡ Creating scaling rule for {args.deployment_id}")
    
    try:
        response = requests.post(
            f"{AUTOSCALE_URL}/rules",
            json={
                "deployment_id": args.deployment_id,
                "name": args.name or "CLI Scaling Rule",
                "metric": args.metric,
                "min_instances": args.min,
                "max_instances": args.max,
                "scale_up_threshold": args.up,
                "scale_down_threshold": args.down
            }
        )
        result = response.json()
        
        print(f"✅ Scaling rule created!")
        print(f"Rule ID: {result['id']}")
        print(f"Min: {result['min_instances']}, Max: {result['max_instances']}")
        print(f"Scale up at {result['scale_up_threshold']}%, down at {result['scale_down_threshold']}%")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def autoscale_cost(args):
    """Get cost analytics"""
    try:
        response = requests.get(f"{AUTOSCALE_URL}/cost/{args.deployment_id}")
        result = response.json()
        
        print(f"\n💰 Cost Analytics for {args.deployment_id}:\n")
        print(f"  Total Cost: ${result['total_cost']}")
        print(f"  Without AutoScale: ${result['cost_without_autoscale']}")
        print(f"  Savings: ${result['savings']} ({result['savings_percent']}%)")
        print(f"  Avg Instances: {result['avg_instances']}")
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def analytics_dashboard(args):
    """Get dashboard summary"""
    try:
        response = requests.get(f"{ANALYTICS_URL}/analytics/dashboard/summary")
        result = response.json()
        
        print(f"\n📊 AI-DOS Dashboard:\n")
        print(f"  Total Models: {result['total_models']}")
        print(f"  Total Experiments: {result['total_experiments']}")
        print(f"  Total Deployments: {result['total_deployments']}")
        print(f"  Predictions Today: {result['total_predictions_today']}")
        print(f"  Avg Model Accuracy: {result['avg_model_accuracy']}")
        print(f"  Total Revenue: ${result['total_revenue']}")
        print(f"  Active Users: {result['active_users']}")
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def analytics_roi(args):
    """Calculate ROI"""
    try:
        response = requests.get(f"{ANALYTICS_URL}/analytics/business/roi")
        result = response.json()
        
        print(f"\n💼 ROI Analysis:\n")
        print(f"  Total Investment: ${result['total_investment']}")
        print(f"  Total Revenue: ${result['total_revenue']}")
        print(f"  Net Profit: ${result['net_profit']}")
        print(f"  ROI: {result['roi_percentage']}%")
        print(f"  Payback Period: {result['payback_period_months']} months")
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def analytics_model(args):
    """Get model performance"""
    try:
        response = requests.get(f"{ANALYTICS_URL}/analytics/model/{args.model_id}/performance")
        result = response.json()
        
        print(f"\n📈 Model Performance for {args.model_id}:\n")
        print(f"  Total Predictions: {result['total_predictions']}")
        print(f"  Avg Response Time: {result['avg_response_time']}ms")
        print(f"  Error Rate: {result['error_rate']*100}%")
        print(f"  Accuracy Trend: {len(result['accuracy_trend'])} data points")
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="AI-DOS CLI - Build ML models from the command line",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Magic Mode
  aidos magic "Build a sentiment analyzer for tweets"
  aidos magic "Create image classifier for cats vs dogs" --show-code
  
  # Datasets
  aidos dataset create "My Dataset" --type text
  aidos dataset list
  
  # Experiments
  aidos experiment create "My Experiment" --project my-project
  aidos experiment list
  
  # Deploy
  aidos deploy create exp_123 "My API"
  aidos deploy list
  aidos deploy metrics deploy_123
  
  # Teams & Collaboration
  aidos team create "ML Team" --description "Building models"
  aidos share experiment exp_123 user_002 --role editor
  
  # Auto-Scaling
  aidos autoscale create deploy_123 --min 1 --max 10 --up 70 --down 30
  aidos autoscale cost deploy_123
  
  # Analytics
  aidos analytics dashboard
  aidos analytics roi
  aidos analytics model model_123
  
  # Status
  aidos status
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Magic command
    magic_parser = subparsers.add_parser('magic', help='Create ML pipeline with Magic Mode')
    magic_parser.add_argument('prompt', help='What to build (in plain English)')
    magic_parser.add_argument('--user', help='User ID')
    magic_parser.add_argument('--no-deploy', action='store_true', help='Skip deployment')
    magic_parser.add_argument('--show-code', action='store_true', help='Show generated code')
    magic_parser.set_defaults(func=magic_create)
    
    # Dataset commands
    dataset_parser = subparsers.add_parser('dataset', help='Manage datasets')
    dataset_sub = dataset_parser.add_subparsers(dest='dataset_command')
    
    dataset_create_parser = dataset_sub.add_parser('create', help='Create dataset')
    dataset_create_parser.add_argument('name', help='Dataset name')
    dataset_create_parser.add_argument('--description', help='Description')
    dataset_create_parser.add_argument('--type', default='text', help='Data type')
    dataset_create_parser.add_argument('--user', help='User ID')
    dataset_create_parser.set_defaults(func=dataset_create)
    
    dataset_list_parser = dataset_sub.add_parser('list', help='List datasets')
    dataset_list_parser.set_defaults(func=dataset_list)
    
    # Experiment commands
    exp_parser = subparsers.add_parser('experiment', help='Manage experiments')
    exp_sub = exp_parser.add_subparsers(dest='experiment_command')
    
    exp_create_parser = exp_sub.add_parser('create', help='Create experiment')
    exp_create_parser.add_argument('name', help='Experiment name')
    exp_create_parser.add_argument('--description', help='Description')
    exp_create_parser.add_argument('--project', help='Project ID')
    exp_create_parser.add_argument('--tags', help='Tags (comma-separated)')
    exp_create_parser.add_argument('--user', help='User ID')
    exp_create_parser.set_defaults(func=experiment_create)
    
    exp_list_parser = exp_sub.add_parser('list', help='List experiments')
    exp_list_parser.set_defaults(func=experiment_list)
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Check AI-DOS status')
    status_parser.set_defaults(func=status)
    
    # Deploy commands
    deploy_parser = subparsers.add_parser('deploy', help='Manage deployments')
    deploy_sub = deploy_parser.add_subparsers(dest='deploy_command')
    
    deploy_create_parser = deploy_sub.add_parser('create', help='Deploy a model')
    deploy_create_parser.add_argument('experiment_id', help='Experiment ID')
    deploy_create_parser.add_argument('name', help='Deployment name')
    deploy_create_parser.add_argument('--description', help='Description')
    deploy_create_parser.set_defaults(func=deploy_create)
    
    deploy_list_parser = deploy_sub.add_parser('list', help='List deployments')
    deploy_list_parser.set_defaults(func=deploy_list)
    
    deploy_metrics_parser = deploy_sub.add_parser('metrics', help='Get deployment metrics')
    deploy_metrics_parser.add_argument('deployment_id', help='Deployment ID')
    deploy_metrics_parser.set_defaults(func=deploy_metrics)
    
    # Team commands
    team_parser = subparsers.add_parser('team', help='Manage teams')
    team_sub = team_parser.add_subparsers(dest='team_command')
    
    team_create_parser = team_sub.add_parser('create', help='Create team')
    team_create_parser.add_argument('name', help='Team name')
    team_create_parser.add_argument('--description', help='Description')
    team_create_parser.add_argument('--user', help='Owner user ID')
    team_create_parser.set_defaults(func=team_create)
    
    # Share command
    share_parser = subparsers.add_parser('share', help='Share resource')
    share_parser.add_argument('resource_type', help='Resource type (experiment, dataset, model)')
    share_parser.add_argument('resource_id', help='Resource ID')
    share_parser.add_argument('user_id', help='User to share with')
    share_parser.add_argument('--role', default='viewer', help='Role (owner, editor, viewer)')
    share_parser.add_argument('--message', help='Message')
    share_parser.add_argument('--shared-by', help='Sharing user ID')
    share_parser.set_defaults(func=share_resource)
    
    # AutoScale commands
    autoscale_parser = subparsers.add_parser('autoscale', help='Manage auto-scaling')
    autoscale_sub = autoscale_parser.add_subparsers(dest='autoscale_command')
    
    autoscale_create_parser = autoscale_sub.add_parser('create', help='Create scaling rule')
    autoscale_create_parser.add_argument('deployment_id', help='Deployment ID')
    autoscale_create_parser.add_argument('--name', help='Rule name')
    autoscale_create_parser.add_argument('--metric', default='cpu', help='Metric (cpu, memory, request_rate)')
    autoscale_create_parser.add_argument('--min', type=int, default=1, help='Min instances')
    autoscale_create_parser.add_argument('--max', type=int, default=10, help='Max instances')
    autoscale_create_parser.add_argument('--up', type=float, default=70.0, help='Scale up threshold')
    autoscale_create_parser.add_argument('--down', type=float, default=30.0, help='Scale down threshold')
    autoscale_create_parser.set_defaults(func=autoscale_create)
    
    autoscale_cost_parser = autoscale_sub.add_parser('cost', help='Get cost analytics')
    autoscale_cost_parser.add_argument('deployment_id', help='Deployment ID')
    autoscale_cost_parser.set_defaults(func=autoscale_cost)
    
    # Analytics commands
    analytics_parser = subparsers.add_parser('analytics', help='View analytics')
    analytics_sub = analytics_parser.add_subparsers(dest='analytics_command')
    
    analytics_dashboard_parser = analytics_sub.add_parser('dashboard', help='Dashboard summary')
    analytics_dashboard_parser.set_defaults(func=analytics_dashboard)
    
    analytics_roi_parser = analytics_sub.add_parser('roi', help='Calculate ROI')
    analytics_roi_parser.set_defaults(func=analytics_roi)
    
    analytics_model_parser = analytics_sub.add_parser('model', help='Model performance')
    analytics_model_parser.add_argument('model_id', help='Model ID')
    analytics_model_parser.set_defaults(func=analytics_model)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
