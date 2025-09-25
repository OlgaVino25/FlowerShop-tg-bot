from dataclasses import dataclass
from typing import List

@dataclass
class UserState:
    occasion = None
    budget = None
    color_scheme = None
    excluded_flowers: List[int] = None
    current_bouquet_index: int = 0
    filtered_bouquets: List = None
    phone = None
    order_address = None
    delivery_date = None
    delivery_time = None
    comment: str = ""
    waiting_custom_occasion: bool = False
    consultation_mode: bool = False
    order_bouquet_pk: int = None
    custom_occasion: str = None
    
    def __post_init__(self):
        if self.excluded_flowers is None:
            self.excluded_flowers = []
        if self.filtered_bouquets is None:
            self.filtered_bouquets = []