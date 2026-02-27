
import logging
import time
from typing import Dict, Optional
from datetime import datetime, timedelta
from config.constants import NOTIFICATION_COOLDOWN_MINUTES, MIN_ROI_PERCENTAGE
from models.trade import Trade
# win10toast is for Windows only, we'll use a placeholder if it's not available
try:
    from win10toast import ToastNotifier
except ImportError:
    ToastNotifier = None

class NotificationService:
    def __init__(self):
        self.notifier = ToastNotifier() if ToastNotifier else None
        self.cooldown_dict: Dict[str, datetime] = {}

    def notify_trade(self, trade: Trade):
        """Triggers a notification for a profitable trade."""
        if trade.roi < MIN_ROI_PERCENTAGE:
            return

        item_key = f"{trade.item_id}_{trade.quality}_{trade.city_buy}_{trade.city_sell}"
        now = datetime.now()

        # Check cooldown
        if item_key in self.cooldown_dict:
            last_notified = self.cooldown_dict[item_key]
            if now - last_notified < timedelta(minutes=NOTIFICATION_COOLDOWN_MINUTES):
                return

        # Prepare notification content
        title = f"Arbitrage Alert: {trade.item_id}"
        message = (f"Buy: {trade.city_buy} ({trade.buy_price})\n"
                   f"Sell: {trade.city_sell} ({trade.sell_price})\n"
                   f"ROI: {trade.roi:.2%}, Profit: {trade.unit_profit:.0f}")

        # Send notification
        if self.notifier:
            try:
                self.notifier.show_toast(title, message, duration=10)
                logging.info(f"Notification sent for {item_key}: {title}")
                self.cooldown_dict[item_key] = now
            except Exception as e:
                logging.error(f"Failed to send notification: {e}")
        else:
            logging.info(f"Notification (Simulation): {title} - {message}")
            self.cooldown_dict[item_key] = now
