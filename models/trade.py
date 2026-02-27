
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Trade:
    item_id: str
    quality: int
    city_buy: str
    city_sell: str
    buy_price: int
    sell_price: int
    unit_profit: float
    roi: float
    trip_profit: float
    silver_per_kg: float
    timestamp: datetime
