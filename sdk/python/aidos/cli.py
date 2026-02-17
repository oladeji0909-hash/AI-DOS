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
    ]
    
    print("\n🔍 AI-DOS Status:\n")
    for name, url in services:
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                print(f"  ✅ {name}: Running")
            else:
                print(f"  ❌ {name}: Error")
        except:
            print(f"  ❌ {name}: Not running")
    print()

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
