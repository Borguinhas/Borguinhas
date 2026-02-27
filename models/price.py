
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Price:
    item_id: str
    quality: int
    city: str
    sell_price: int
    buy_price: int
    avg_24h: int
    timestamp: datetime
