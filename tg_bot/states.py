from dataclasses import dataclass, field
from typing import List


@dataclass
class UserState:
    # Состояния для подбора букетов
    occasion: str = None
    budget: str = None
    color_scheme: str = None
    color_scheme_set: bool = False
    excluded_flowers: List[int] = field(default_factory=list)
    current_bouquet_index: int = 0
    filtered_bouquets: List = field(default_factory=list)
    
    # Состояния для заказа
    order_state: str = None  # 'name', 'phone', 'address', 'date', 'time', 'comment'
    order_bouquet_pk: int = None
    order_name: str = None
    phone: str = None
    order_address: str = None
    delivery_date: str = None
    delivery_time: str = None
    comment: str = ""
    
    # Состояния для консультации
    consultation_mode: bool = False
    waiting_custom_occasion: bool = False
    custom_occasion: str = None