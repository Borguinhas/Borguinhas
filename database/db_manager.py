
import sqlite3
import os
from datetime import datetime, timedelta
from config.constants import DATABASE_NAME, DATABASE_PURGE_DAYS
from models.price import Price

class DatabaseManager:
    def __init__(self, db_path=None):
        if db_path is None:
            # Place the database file in the project root or a data folder
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            db_path = os.path.join(project_root, DATABASE_NAME)
        
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        """Creates the necessary tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS market_prices (
                    item_id TEXT,
                    quality INTEGER,
                    city TEXT,
                    sell_price INTEGER,
                    buy_price INTEGER,
                    avg_24h INTEGER,
                    timestamp DATETIME,
                    PRIMARY KEY (item_id, quality, city)
                )
            """)
            conn.commit()

    def save_price(self, price: Price):
        """Inserts or replaces a price entry in the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO market_prices (item_id, quality, city, sell_price, buy_price, avg_24h, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (price.item_id, price.quality, price.city, price.sell_price, price.buy_price, price.avg_24h, price.timestamp))
            conn.commit()

    def get_price(self, item_id: str, quality: int, city: str) -> Price | None:
        """Retrieves a price entry from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT item_id, quality, city, sell_price, buy_price, avg_24h, timestamp
                FROM market_prices
                WHERE item_id = ? AND quality = ? AND city = ?
            """, (item_id, quality, city))
            row = cursor.fetchone()
            if row:
                return Price(*row)
            return None

    def purge_old_data(self):
        """Deletes entries older than the configured purge period."""
        purge_threshold = datetime.now() - timedelta(days=DATABASE_PURGE_DAYS)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM market_prices WHERE timestamp < ?", (purge_threshold,))
            conn.commit()
