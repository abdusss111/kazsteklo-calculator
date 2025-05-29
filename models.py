from pydantic import BaseModel

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


class PasswordCheckRequest(BaseModel):
    password: str
