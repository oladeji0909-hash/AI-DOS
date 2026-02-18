"""
AI-DOS Python SDK
Build ML models in seconds with plain English.
"""

import requests
from typing import Dict, Optional, List
import json

class AIDOS:
    """Main AI-DOS client"""
    
    def __init__(self, api_url: str = "http://localhost:8000", api_key: Optional[str] = None):
        self.api_url = api_url
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    
    def login(self, username: str, password: str) -> str:
        """Login and get access token"""
        response = requests.post(
            f"{self.api_url}/auth/login",
            json={"username": username, "password": password}
        )
        data = response.json()
        self.api_key = data["access_token"]
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        return self.api_key
    
    def register(self, username: str, email: str, password: str, full_name: str) -> Dict:
        """Register new user"""
        response = requests.post(
            f"{self.api_url}/auth/register",
            json={
                "username": username,
                "email": email,
                "password": password,
                "full_name": full_name
            }
        )
        return response.json()


class Magic:
    """Magic Mode - Build ML pipelines from natural language"""
    
    def __init__(self, api_url: str = "http://localhost:8003"):
        self.api_url = api_url
    
    def create(self, prompt: str, user_id: str = "default", auto_deploy: bool = True) -> Dict:
        """
        Create ML pipeline from natural language
        
        Example:
            magic = Magic()
            result = magic.create("Build a sentiment analyzer for tweets")
            print(result['api_endpoint'])
        """
        response = requests.post(
            f"{self.api_url}/magic/create",
            json={
                "prompt": prompt,
                "user_id": user_id,
                "auto_deploy": auto_deploy
            }
        )
        return response.json()
    
    def status(self, job_id: str) -> Dict:
        """Get status of magic job"""
        response = requests.get(f"{self.api_url}/magic/status/{job_id}")
        return response.json()


class DataForge:
    """Dataset management and versioning"""
    
    def __init__(self, api_url: str = "http://localhost:8001"):
        self.api_url = api_url
    
    def create_dataset(self, name: str, description: str, owner_id: str, data_type: str) -> Dict:
        """Create new dataset"""
        response = requests.post(
            f"{self.api_url}/datasets",
            json={
                "name": name,
                "description": description,
                "owner_id": owner_id,
                "data_type": data_type
            }
        )
        return response.json()
    
    def list_datasets(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """List all datasets"""
        response = requests.get(f"{self.api_url}/datasets?skip={skip}&limit={limit}")
        return response.json()
    
    def get_dataset(self, dataset_id: str) -> Dict:
        """Get dataset by ID"""
        response = requests.get(f"{self.api_url}/datasets/{dataset_id}")
        return response.json()
    
    def create_version(self, dataset_id: str, version: str, changes: str, created_by: str) -> Dict:
        """Create new dataset version"""
        response = requests.post(
            f"{self.api_url}/datasets/{dataset_id}/versions",
            json={
                "version": version,
                "changes": changes,
                "created_by": created_by
            }
        )
        return response.json()


class ModelHub:
    """Experiment tracking and model registry"""
    
    def __init__(self, api_url: str = "http://localhost:8002"):
        self.api_url = api_url
    
    def create_experiment(self, name: str, description: str, project_id: str, user_id: str, tags: List[str] = None) -> Dict:
        """Create new experiment"""
        response = requests.post(
            f"{self.api_url}/experiments",
            json={
                "name": name,
                "description": description,
                "project_id": project_id,
                "user_id": user_id,
                "tags": tags or []
            }
        )
        return response.json()
    
    def list_experiments(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """List all experiments"""
        response = requests.get(f"{self.api_url}/experiments?skip={skip}&limit={limit}")
        return response.json()
    
    def create_run(self, experiment_id: str, name: str, parameters: Dict, user_id: str) -> Dict:
        """Create training run"""
        response = requests.post(
            f"{self.api_url}/runs",
            json={
                "experiment_id": experiment_id,
                "name": name,
                "parameters": parameters,
                "user_id": user_id
            }
        )
        return response.json()
    
    def log_metrics(self, run_id: str, metrics: Dict, step: int = 0) -> Dict:
        """Log metrics for a run"""
        response = requests.post(
            f"{self.api_url}/runs/{run_id}/metrics",
            json={
                "metrics": metrics,
                "step": step
            }
        )
        return response.json()


class Deploy:
    """Model deployment and inference"""
    
    def __init__(self, api_url: str = "http://localhost:8005"):
        self.api_url = api_url
    
    def create(self, experiment_id: str, name: str, description: str = None) -> Dict:
        """
        Deploy a model from experiment
        
        Example:
            deploy = Deploy()
            result = deploy.create("exp_123", "My API")
            print(result['endpoint_url'])
        """
        response = requests.post(
            f"{self.api_url}/deploy/create",
            json={
                "experiment_id": experiment_id,
                "name": name,
                "description": description
            }
        )
        return response.json()
    
    def list(self) -> Dict:
        """List all deployments"""
        response = requests.get(f"{self.api_url}/deploy/list")
        return response.json()
    
    def get(self, deployment_id: str) -> Dict:
        """Get deployment details"""
        response = requests.get(f"{self.api_url}/deploy/{deployment_id}")
        return response.json()
    
    def delete(self, deployment_id: str) -> Dict:
        """Stop deployment"""
        response = requests.delete(f"{self.api_url}/deploy/{deployment_id}")
        return response.json()
    
    def predict(self, deployment_id: str, data: Dict) -> Dict:
        """Make prediction"""
        response = requests.post(
            f"{self.api_url}/deploy/{deployment_id}/predict",
            json=data
        )
        return response.json()
    
    def metrics(self, deployment_id: str) -> Dict:
        """Get deployment metrics"""
        response = requests.get(f"{self.api_url}/deploy/{deployment_id}/metrics")
        return response.json()
    
    def logs(self, deployment_id: str, limit: int = 100) -> Dict:
        """Get deployment logs"""
        response = requests.get(f"{self.api_url}/deploy/{deployment_id}/logs?limit={limit}")
        return response.json()


class Collab:
    """Team collaboration and sharing"""
    
    def __init__(self, api_url: str = "http://localhost:8006"):
        self.api_url = api_url
    
    def create_team(self, name: str, description: str, owner_id: str) -> Dict:
        """Create a team"""
        response = requests.post(
            f"{self.api_url}/teams",
            json={"name": name, "description": description, "owner_id": owner_id}
        )
        return response.json()
    
    def add_member(self, team_id: str, user_id: str, role: str) -> Dict:
        """Add member to team"""
        response = requests.post(
            f"{self.api_url}/teams/{team_id}/members",
            json={"team_id": team_id, "user_id": user_id, "role": role}
        )
        return response.json()
    
    def share(self, resource_type: str, resource_id: str, shared_by: str, shared_with: str, role: str, message: str = None) -> Dict:
        """Share resource with user"""
        response = requests.post(
            f"{self.api_url}/share",
            json={
                "resource_type": resource_type,
                "resource_id": resource_id,
                "shared_by": shared_by,
                "shared_with": shared_with,
                "role": role,
                "message": message
            }
        )
        return response.json()
    
    def comment(self, resource_type: str, resource_id: str, user_id: str, text: str) -> Dict:
        """Add comment to resource"""
        response = requests.post(
            f"{self.api_url}/comments",
            json={
                "resource_type": resource_type,
                "resource_id": resource_id,
                "user_id": user_id,
                "text": text
            }
        )
        return response.json()
    
    def get_notifications(self, user_id: str, unread_only: bool = False) -> List[Dict]:
        """Get user notifications"""
        response = requests.get(f"{self.api_url}/notifications/{user_id}?unread_only={unread_only}")
        return response.json()
    
    def get_activity(self, user_id: str = None, limit: int = 50) -> List[Dict]:
        """Get activity feed"""
        params = {"limit": limit}
        if user_id:
            params["user_id"] = user_id
        response = requests.get(f"{self.api_url}/activity", params=params)
        return response.json()


# Convenience functions
def magic(prompt: str, user_id: str = "default") -> Dict:
    """Quick magic mode - one line to create ML pipeline"""
    m = Magic()
    return m.create(prompt, user_id)


def quick_start():
    """Quick start guide"""
    print("""
    🚀 AI-DOS Quick Start
    
    1. Magic Mode (Easiest):
       from aidos import magic
       result = magic("Build a sentiment analyzer for tweets")
       print(result['api_endpoint'])
    
    2. Full Control:
       from aidos import Magic, DataForge, ModelHub
       
       # Create dataset
       df = DataForge()
       dataset = df.create_dataset("My Dataset", "Description", "user123", "text")
       
       # Track experiment
       mh = ModelHub()
       exp = mh.create_experiment("My Experiment", "Description", "project1", "user123")
       
       # Magic Mode
       magic = Magic()
       result = magic.create("Build sentiment analyzer")
    
    3. Authentication:
       from aidos import AIDOS
       client = AIDOS()
       client.register("username", "email@example.com", "password", "Full Name")
       token = client.login("username", "password")
    
    📚 Full docs: https://docs.ai-dos.io
    """)


__version__ = "0.1.0"
__all__ = ["AIDOS", "Magic", "DataForge", "ModelHub", "Deploy", "Collab", "magic", "quick_start"]
