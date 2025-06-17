# main.py
from fastapi import FastAPI, Request, HTTPException, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from app.logic import calculate_price
from app.models import ShowerRequest, AuthRequest
from starlette.status import HTTP_401_UNAUTHORIZED
from apscheduler.schedulers.background import BackgroundScheduler
from data.glass_price import load_glass_prices
from data.furniture_price import load_furniture_prices
from app.auth import validate_credentials, create_token, get_current_user, validate_manager_credentials
import logging
app = FastAPI(title="Shower Calculator API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

@app.post("/calculate")
def calculate(request: ShowerRequest, user: str = Depends(get_current_user)):
    try:
        result = calculate_price(request.dict())
        return result
    except Exception as e:
        return {"error": f"Calculation error: {str(e)}"}

@app.post("/calculate/physical")
def calculate_physical(request: ShowerRequest = Body(...)):
    try:
        # Override customer_type to ensure it is always "физлицо"
        request_dict = request.dict()
        request_dict["customer_type"] = "физлицо"

        result = calculate_price(request_dict)
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
    return {"access_token": token, "token_type": "bearer", "user": "legal"}

@app.post("/login/manager")
def login_manager(data: AuthRequest):
    if not validate_manager_credentials(data.username, data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(data.username)
    return {"access_token": token, "token_type": "bearer", "user": "manager"}

@app.get("/furniture-list")
def get_furniture_list():
    try:
        from data.furniture_price import get_furniture_price_legal
        return get_furniture_price_legal()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading furniture list: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

