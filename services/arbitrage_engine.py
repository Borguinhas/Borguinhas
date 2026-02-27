
import math
import logging
from typing import List, Dict, Optional
from datetime import datetime
from config.constants import BLACK_MARKET_CITY_ID, BLACK_MARKET_TRASH_RATE, PREMIUM_TAX_RATE, NON_PREMIUM_TAX_RATE, MIN_ROI_PERCENTAGE, MIN_SPREAD_PERCENTAGE, MIN_VOLUME, MOUNT_CAPACITY
from models.price import Price
from models.trade import Trade
from models.item import Item

class ArbitrageEngine:
    def __init__(self, use_premium_tax: bool = True):
        self.tax_rate = PREMIUM_TAX_RATE if use_premium_tax else NON_PREMIUM_TAX_RATE

    def calculate_trade(self, item: Item, buy_price_info: Price, sell_price_info: Price) -> Optional[Trade]:
        """Calculates potential profit and ROI for a trade."""
        
        # Validation based on calculation rules
        if buy_price_info.buy_price == 0 or sell_price_info.sell_price == 0:
            return None
        
        # Determine the correct sell price (Black Market uses buy_price_max)
        sell_price = sell_price_info.sell_price
        if sell_price_info.city == "Black Market" or sell_price_info.city == BLACK_MARKET_CITY_ID:
            sell_price = sell_price_info.buy_price # buy_price_max from the API is what we sell to the BM for
        
        # Setup Fee (estimated at 1.5% for sell orders, 0 for direct sells)
        setup_fee = 0 # Assume direct sell for simplicity or adjust as needed
        
        # Unit Profit calculation
        unit_profit = (sell_price * (1 - self.tax_rate)) - (buy_price_info.sell_price + setup_fee)
        
        # Apply Trash Rate for Black Market
        if sell_price_info.city == "Black Market" or sell_price_info.city == BLACK_MARKET_CITY_ID:
            unit_profit = unit_profit * (1 - BLACK_MARKET_TRASH_RATE)
            
        # ROI calculation
        roi = unit_profit / buy_price_info.sell_price if buy_price_info.sell_price > 0 else 0
        
        # Spread calculation
        spread = (sell_price - buy_price_info.sell_price) / buy_price_info.sell_price if buy_price_info.sell_price > 0 else 0
        
        # Rejection criteria
        if roi < MIN_ROI_PERCENTAGE or spread < MIN_SPREAD_PERCENTAGE:
            return None
            
        # Trip Profit and Silver per KG
        item_weight = item.weight if item.weight > 0 else 0.1 # Default small weight
        trip_profit = math.floor(MOUNT_CAPACITY / item_weight) * unit_profit
        silver_per_kg = unit_profit / item_weight
        
        return Trade(
            item_id=item.item_id,
            quality=buy_price_info.quality,
            city_buy=buy_price_info.city,
            city_sell=sell_price_info.city,
            buy_price=buy_price_info.sell_price,
            sell_price=sell_price,
            unit_profit=unit_profit,
            roi=roi,
            trip_profit=trip_profit,
            silver_per_kg=silver_per_kg,
            timestamp=datetime.now()
        )
