
from dataclasses import dataclass
from typing import Optional

@dataclass
class Item:
    item_id: str
    item_name: str
    item_type: str
    weight: float
    tier: int
    enchantment: int
    max_stack_size: int
    craftable: bool
    salvageable: bool
    equipable: bool
    description: Optional[str] = None
