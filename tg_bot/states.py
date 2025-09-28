from dataclasses import dataclass, field
from typing import List


@dataclass
class UserState:
    occasion: str = None
    budget: str = None
    color_scheme: str = None
    color_scheme_set: bool = False
    excluded_flowers: List[int] = field(default_factory=list)
    current_bouquet_index: int = 0
    filtered_bouquets: List = field(default_factory=list)
    phone: str = None
    order_address: str = None
    delivery_date: str = None
    delivery_time: str = None
    comment: str = ""
    waiting_custom_occasion: bool = False
    consultation_mode: bool = False
    order_bouquet_pk: int = None
    custom_occasion: str = None
