# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from logic import calculate_price

app = FastAPI(title="Shower Calculator API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ShowerRequest(BaseModel):
    shower_type: str = "П-образная"
    customer_type: str = "физлицо"
    glass_type: str = "Стекло Ритм"
    frame_type: str = "Квадратная труба"
    hardware_color: str = "Бронза"
    length: float = 2
    height: float = 2
    mount_type: str = "На П-профиле"
    connector_type: str = "Коннектор П-образный"
    handle_type: str = "Скоба"
    bottom_element: str = "Порожек"
    binding_type: str = "По периметру"
    door_count: str = "Две"
    door_position: str = "С боку"
    magnet_seal_type: str = "Без магнитного уплотнителя"
    binding_position: str = "Обвязка над стеклом"
    seal_type: str = "Полусфера"
    rigid_element_type: str = "Труба круглая"
    curtain_type: str = "Распашное"
    city: str = "Алматы"

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

from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

PASSWORD = "kazsteklo-legal"  # Replace with a secure password or load from env

class PasswordCheckRequest(BaseModel):
    password: str

@app.post("/auth/password-check")
def password_check(data: PasswordCheckRequest):
    if data.password == PASSWORD:
        return {"authorized": True}
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid password")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

