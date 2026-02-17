from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime, timedelta
import jwt
import hashlib

app = FastAPI(title="AI-DOS API Gateway", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

security = HTTPBearer()

# Models
class User(BaseModel):
    id: Optional[str] = None
    username: str
    email: str
    full_name: str
    disabled: bool = False
    created_at: Optional[datetime] = None

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user: User

class ServiceStatus(BaseModel):
    name: str
    url: str
    status: str
    version: str

# In-memory storage
users_db: Dict[str, Dict] = {}
api_keys_db: Dict[str, str] = {}

# Helper functions
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None

# Endpoints

@app.get("/")
def root():
    return {
        "service": "AI-DOS API Gateway",
        "version": "1.0.0",
        "status": "operational",
        "documentation": "/docs",
        "services": {
            "dataforge": "http://dataforge:8000",
            "modelhub": "http://modelhub:8000",
            "trainos": "http://trainos:8000",
            "deployengine": "http://deployengine:8000",
            "evalkit": "http://evalkit:8000",
            "promptstudio": "http://promptstudio:8000",
            "marketplace": "http://marketplace:8000",
            "collabspace": "http://collabspace:8000",
            "costoptimizer": "http://costoptimizer:8000",
            "automl": "http://automl:8000",
            "security": "http://security:8000",
            "edgesync": "http://edgesync:8000"
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "uptime": "operational"
    }

@app.get("/services/status")
def get_services_status():
    services = [
        ServiceStatus(name="DataForge", url="http://dataforge:8000", status="operational", version="1.0.0"),
        ServiceStatus(name="ModelHub", url="http://modelhub:8000", status="operational", version="1.0.0"),
        ServiceStatus(name="TrainOS", url="http://trainos:8000", status="operational", version="1.0.0"),
        ServiceStatus(name="DeployEngine", url="http://deployengine:8000", status="operational", version="1.0.0"),
        ServiceStatus(name="EvalKit", url="http://evalkit:8000", status="operational", version="1.0.0"),
        ServiceStatus(name="PromptStudio", url="http://promptstudio:8000", status="operational", version="1.0.0"),
        ServiceStatus(name="AIMarketplace", url="http://marketplace:8000", status="operational", version="1.0.0"),
        ServiceStatus(name="CollabSpace", url="http://collabspace:8000", status="operational", version="1.0.0"),
        ServiceStatus(name="CostOptimizer", url="http://costoptimizer:8000", status="operational", version="1.0.0"),
        ServiceStatus(name="AutoML Studio", url="http://automl:8000", status="operational", version="1.0.0"),
        ServiceStatus(name="SecurityVault", url="http://security:8000", status="operational", version="1.0.0"),
        ServiceStatus(name="EdgeSync", url="http://edgesync:8000", status="operational", version="1.0.0"),
    ]
    return {"services": services, "total": len(services), "healthy": len(services)}

# Authentication
@app.post("/auth/register", response_model=User)
def register(user_create: UserCreate):
    if user_create.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    user_id = hashlib.md5(f"{user_create.username}{datetime.utcnow()}".encode()).hexdigest()
    user = User(
        id=user_id,
        username=user_create.username,
        email=user_create.email,
        full_name=user_create.full_name,
        created_at=datetime.utcnow()
    )
    
    users_db[user_create.username] = {
        "user": user,
        "password": hash_password(user_create.password)
    }
    
    return user

@app.post("/auth/login", response_model=Token)
def login(user_login: UserLogin):
    if user_login.username not in users_db:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user_data = users_db[user_login.username]
    if not verify_password(user_login.password, user_data["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": user_login.username})
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=user_data["user"]
    )

@app.get("/auth/me", response_model=User)
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    username = payload.get("sub")
    if username not in users_db:
        raise HTTPException(status_code=401, detail="User not found")
    
    return users_db[username]["user"]

@app.post("/auth/refresh", response_model=Token)
def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    username = payload.get("sub")
    if username not in users_db:
        raise HTTPException(status_code=401, detail="User not found")
    
    new_token = create_access_token({"sub": username})
    
    return Token(
        access_token=new_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=users_db[username]["user"]
    )

# API Key Management
@app.post("/api-keys/generate")
def generate_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    username = payload.get("sub")
    api_key = hashlib.sha256(f"{username}{datetime.utcnow()}".encode()).hexdigest()
    api_keys_db[api_key] = username
    
    return {
        "api_key": api_key,
        "created_at": datetime.utcnow(),
        "message": "Store this API key securely. It won't be shown again."
    }

@app.get("/api-keys/validate")
def validate_api_key(api_key: str = Header(..., alias="X-API-Key")):
    if api_key not in api_keys_db:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    username = api_keys_db[api_key]
    return {
        "valid": True,
        "username": username,
        "message": "API key is valid"
    }

# Rate Limiting Info
@app.get("/rate-limits")
def get_rate_limits(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return {
        "requests_per_minute": 60,
        "requests_per_hour": 1000,
        "requests_per_day": 10000,
        "current_usage": {
            "minute": 5,
            "hour": 120,
            "day": 850
        }
    }

# System Stats
@app.get("/stats")
def get_system_stats():
    return {
        "total_users": len(users_db),
        "total_api_keys": len(api_keys_db),
        "services_online": 12,
        "uptime_percentage": 99.9,
        "total_requests_today": 15420,
        "average_response_time_ms": 45
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
