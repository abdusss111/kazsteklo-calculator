# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from logic import calculate_price
from models import ShowerRequest, PasswordCheckRequest
from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
from apscheduler.schedulers.background import BackgroundScheduler
from data.glass_price import load_glass_prices
from data.furniture_price import load_furniture_prices
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
    load_glass_data()
    load_furniture_data()

    scheduler.add_job(load_glass_data, "interval", hours=24)
    scheduler.add_job(load_furniture_data, "interval", hours=24)
    scheduler.start()


@app.get("/")
def read_root():
    return {"message": "Shower Calculator API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is working properly"}

@app.post("/calculate")
def calculate(request: ShowerRequest):
    try:
        result = calculate_price(request.dict())
        return result
    except Exception as e:
        return {"error": f"Calculation error: {str(e)}"}

@app.options("/calculate")
def options_calculate():
    return {"message": "CORS preflight handled"}

@app.post("/auth/password-check")
def password_check(data: PasswordCheckRequest):
    if data.password == PASSWORD:
        return {"authorized": True}
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid password")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

