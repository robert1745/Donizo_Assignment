"""Material DB with city modifiers and simple lookup functions."""
from typing import Dict

BASE_MATERIALS: Dict[str, Dict] = {
    "ceramic_floor_tile": {"unit": "m2", "base_price": 25.0},
    "wall_tile": {"unit": "m2", "base_price": 20.0},
    "vanity_unit": {"unit": "ea", "base_price": 150.0},
    "toilet_unit": {"unit": "ea", "base_price": 120.0},
    "plumbing_rework": {"unit": "job", "base_price": 200.0},
    "paint": {"unit": "litre", "base_price": 8.0},
    "adhesive_grout": {"unit": "m2", "base_price": 5.0},
}

CITY_MULTIPLIERS = {
    "marseille": 1.0,
    "paris": 1.35,
    "lyon": 1.08,
}

def get_material_price(key: str, quantity: float = 1.0, city: str = "marseille") -> float:
    """Return material subtotal for given key and quantity with city modifier."""
    city = city.lower()
    entry = BASE_MATERIALS.get(key)
    if not entry:
        raise KeyError(f"Material '{key}' not found in material DB")
    base = entry["base_price"] * quantity
    multiplier = CITY_MULTIPLIERS.get(city, 1.0)
    return round(base * multiplier, 2)

def list_materials():
    return BASE_MATERIALS.keys()