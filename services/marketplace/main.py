from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import hashlib

app = FastAPI(title="AI-DOS Marketplace", description="Buy and sell trained ML models")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (replace with database in production)
models_db = {}
purchases_db = {}

class ModelListing(BaseModel):
    name: str
    description: str
    task_type: str  # sentiment, classification, generation, etc.
    price: float  # in USD
    seller_id: str
    model_url: str
    accuracy: Optional[float] = None
    tags: List[str] = []

class ModelListingResponse(BaseModel):
    id: str
    name: str
    description: str
    task_type: str
    price: float
    seller_id: str
    model_url: str
    accuracy: Optional[float]
    tags: List[str]
    rating: float
    sales_count: int
    created_at: str

class PurchaseRequest(BaseModel):
    model_id: str
    buyer_id: str

class PurchaseResponse(BaseModel):
    purchase_id: str
    model_id: str
    buyer_id: str
    api_endpoint: str
    status: str
    message: str

@app.post("/marketplace/list", response_model=ModelListingResponse)
async def list_model(listing: ModelListing):
    """List a trained model for sale"""
    model_id = hashlib.md5(f"{listing.name}{listing.seller_id}{datetime.now()}".encode()).hexdigest()
    
    model_data = {
        "id": model_id,
        "name": listing.name,
        "description": listing.description,
        "task_type": listing.task_type,
        "price": listing.price,
        "seller_id": listing.seller_id,
        "model_url": listing.model_url,
        "accuracy": listing.accuracy,
        "tags": listing.tags,
        "rating": 0.0,
        "sales_count": 0,
        "created_at": datetime.now().isoformat()
    }
    
    models_db[model_id] = model_data
    
    return ModelListingResponse(**model_data)

@app.get("/marketplace/models", response_model=List[ModelListingResponse])
async def get_models(
    task_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_rating: Optional[float] = None
):
    """Browse available models"""
    results = list(models_db.values())
    
    # Filter by task type
    if task_type:
        results = [m for m in results if m["task_type"] == task_type]
    
    # Filter by price
    if min_price is not None:
        results = [m for m in results if m["price"] >= min_price]
    if max_price is not None:
        results = [m for m in results if m["price"] <= max_price]
    
    # Filter by rating
    if min_rating is not None:
        results = [m for m in results if m["rating"] >= min_rating]
    
    # Sort by rating and sales
    results.sort(key=lambda x: (x["rating"], x["sales_count"]), reverse=True)
    
    return [ModelListingResponse(**m) for m in results]

@app.get("/marketplace/models/{model_id}", response_model=ModelListingResponse)
async def get_model(model_id: str):
    """Get details of a specific model"""
    if model_id not in models_db:
        raise HTTPException(status_code=404, detail="Model not found")
    
    return ModelListingResponse(**models_db[model_id])

@app.post("/marketplace/purchase", response_model=PurchaseResponse)
async def purchase_model(purchase: PurchaseRequest):
    """Purchase a model and get instant API access"""
    if purchase.model_id not in models_db:
        raise HTTPException(status_code=404, detail="Model not found")
    
    model = models_db[purchase.model_id]
    purchase_id = hashlib.md5(f"{purchase.model_id}{purchase.buyer_id}{datetime.now()}".encode()).hexdigest()
    
    # Create API endpoint for buyer
    api_endpoint = f"https://api.ai-dos.io/marketplace/{purchase_id}/predict"
    
    # Record purchase
    purchase_data = {
        "purchase_id": purchase_id,
        "model_id": purchase.model_id,
        "buyer_id": purchase.buyer_id,
        "api_endpoint": api_endpoint,
        "purchased_at": datetime.now().isoformat(),
        "price_paid": model["price"]
    }
    purchases_db[purchase_id] = purchase_data
    
    # Update sales count
    models_db[purchase.model_id]["sales_count"] += 1
    
    return PurchaseResponse(
        purchase_id=purchase_id,
        model_id=purchase.model_id,
        buyer_id=purchase.buyer_id,
        api_endpoint=api_endpoint,
        status="completed",
        message=f"✅ Model purchased! Your API is ready at {api_endpoint}"
    )

@app.get("/marketplace/my-purchases/{buyer_id}")
async def get_my_purchases(buyer_id: str):
    """Get all purchases by a buyer"""
    purchases = [p for p in purchases_db.values() if p["buyer_id"] == buyer_id]
    return {"purchases": purchases, "count": len(purchases)}

@app.get("/marketplace/my-sales/{seller_id}")
async def get_my_sales(seller_id: str):
    """Get all sales by a seller"""
    models = [m for m in models_db.values() if m["seller_id"] == seller_id]
    total_revenue = sum(m["sales_count"] * m["price"] * 0.8 for m in models)  # 80% to seller
    
    return {
        "models": models,
        "total_sales": sum(m["sales_count"] for m in models),
        "total_revenue": total_revenue
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "marketplace"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
