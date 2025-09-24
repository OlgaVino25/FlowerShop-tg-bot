from dataclasses import dataclass
from typing import List


@dataclass
class Role:
    pk: int
    title: str


@dataclass
class User:
    pk: int
    tg_id: int
    full_name: str
    role: Role
    address: str
    phone: str


@dataclass
class Flower:
    pk: int
    title: str
    color: str
    price: int


@dataclass
class ColorScheme:
    pk: int
    title: str


@dataclass
class Occasion:
    pk: int
    title: str


@dataclass
class Bouquet:
    pk: int
    title: str
    price: int
    budget_category: str
    image: str
    occasion: str
    meaning: str
    flowers: List[int]
    color_scheme: str


@dataclass
class Consultation:
    pk: int
    customer: int
    phone: str
    occasion: str
    budget: int
    preferred_colors: List[str]
    excluded_flowers: List[int]
    status: str
    created_at: str


@dataclass
class Order:
    pk: int
    customer: int
    bouquet: int
    address: str
    delivery_date: str
    delivery_time: str
    comment: str
    status: str