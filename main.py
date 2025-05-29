# main.py
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from logic import calculate_price
from models import ShowerRequest, AuthRequest
from starlette.status import HTTP_401_UNAUTHORIZED
from apscheduler.schedulers.background import BackgroundScheduler
from data.glass_price import load_glass_prices
from data.furniture_price import load_furniture_prices
from auth import validate_credentials, create_token, get_current_user
import logging
app = FastAPI(title="Shower Calculator API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler = BackgroundScheduler()

@app.on_event("startup")
def on_startup():
    print("🔄 Loading initial data...")
    load_glass_prices()
    load_furniture_prices()

    scheduler.add_job(load_glass_prices, "interval", hours=24)
    scheduler.add_job(load_furniture_prices, "interval", hours=24)
    scheduler.start()


@app.get("/")
def read_root():
    return {"message": "Shower Calculator API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is working properly"}

from auth import get_current_user

@app.post("/calculate")
def calculate(request: ShowerRequest, user: str = Depends(get_current_user)):
    try:
        result = calculate_price(request.dict())
        return result
    except Exception as e:
        return {"error": f"Calculation error: {str(e)}"}


@app.options("/calculate")
def options_calculate():
    return {"message": "CORS preflight handled"}

@app.post("/login")
def login(data: AuthRequest):
    if not validate_credentials(data.username, data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(data.username)
    return {"access_token": token, "token_type": "bearer"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

