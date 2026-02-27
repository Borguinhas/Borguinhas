
import customtkinter
import threading
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Optional
from ui.table_view import TableView
from services.api_client import APIClient
from services.arbitrage_engine import ArbitrageEngine
from services.notification_service import NotificationService
from data.metadata_loader import MetadataLoader
from data.flip_loader import FlipLoader
from database.db_manager import DatabaseManager
from models.item import Item
from models.price import Price
from models.trade import Trade
from datetime import datetime

class MainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Albion Market Master - Europe Server")
        self.geometry("1200x800")

        # Initialization
        self.metadata_loader = MetadataLoader()
        self.flip_loader = FlipLoader()
        self.db_manager = DatabaseManager()
        self.api_client = APIClient()
        self.arbitrage_engine = ArbitrageEngine()
        self.notification_service = NotificationService()
        self.executor = ThreadPoolExecutor(max_workers=5)

        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Albion MM", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)

        self.refresh_button = customtkinter.CTkButton(self.sidebar_frame, text="Refresh Data", command=self.start_refresh)
        self.refresh_button.grid(row=1, column=0, padx=20, pady=10)

        self.progress_bar = customtkinter.CTkProgressBar(self.sidebar_frame)
        self.progress_bar.grid(row=2, column=0, padx=20, pady=10)
        self.progress_bar.set(0)

        # Main View
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.table_view = TableView(self.main_frame)
        self.table_view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Start background sync
        threading.Thread(target=self.initial_sync, daemon=True).start()

    def initial_sync(self):
        """Runs at startup to sync metadata and flips."""
        self.metadata_loader.sync_metadata()
        self.flip_loader.load_flips()
        self.db_manager.purge_old_data()
        logging.info("Initial sync completed.")

    def start_refresh(self):
        """Starts the price refresh process in a separate thread."""
        self.refresh_button.configure(state="disabled")
        threading.Thread(target=self.refresh_data, daemon=True).start()

    def refresh_data(self):
        """Fetches new prices and updates the table."""
        try:
            # Example: Fetching a subset of items for demonstration
            # In a real scenario, this would be more comprehensive
            item_ids = list(self.metadata_loader.items.keys())[:500] # Limit for demo
            locations = ["Thetford", "Lymhurst", "Bridgewatch", "Martlock", "Fort Sterling", "Caerleon", "Black Market"]
            qualities = [1, 2, 3]

            all_trades = []
            batch_size = 200
            total_batches = (len(item_ids) + batch_size - 1) // batch_size

            for i in range(0, len(item_ids), batch_size):
                batch = item_ids[i:i + batch_size]
                self.progress_bar.set((i / len(item_ids)))
                
                prices_data = self.api_client.fetch_prices(batch, locations, qualities)
                
                # Process prices and calculate trades
                trades = self.process_prices(prices_data)
                all_trades.extend(trades)

            # Update UI in main thread
            self.after(0, lambda: self.update_ui(all_trades))
            
        except Exception as e:
            logging.error(f"Error during refresh: {e}")
        finally:
            self.after(0, lambda: self.refresh_button.configure(state="normal"))
            self.after(0, lambda: self.progress_bar.set(1))

    def process_prices(self, prices_data: List[Dict]) -> List[Trade]:
        """Processes raw API data and returns a list of profitable trades."""
        trades = []
        # Group prices by item and quality for easier comparison
        price_map = {}
        for p in prices_data:
            key = (p["item_id"], p["quality"])
            if key not in price_map:
                price_map[key] = {}
            price_map[key][p["city"]] = Price(
                item_id=p["item_id"],
                quality=p["quality"],
                city=p["city"],
                sell_price=p["sell_price_min"],
                buy_price=p["buy_price_max"], # sell_price_max is also available
                avg_24h=0, # Not provided in this API call
                timestamp=datetime.now()
            )

        # Calculate arbitrage for each item/quality
        for (item_id, quality), cities_prices in price_map.items():
            item_info = self.metadata_loader.get_item_info(item_id)
            if not item_info:
                continue
            
            item_obj = Item(
                item_id=item_id,
                item_name=item_info["LocalizedName"] or item_id,
                item_type=item_info["Category"],
                weight=item_info["Weight"],
                tier=item_info["Tier"],
                enchantment=0, # Simplified
                max_stack_size=1,
                craftable=True,
                salvageable=True,
                equipable=True
            )

            # Check flips (City -> Black Market)
            if "Black Market" in cities_prices:
                sell_price_info = cities_prices["Black Market"]
                for city, buy_price_info in cities_prices.items():
                    if city == "Black Market":
                        continue
                    
                    trade = self.arbitrage_engine.calculate_trade(item_obj, buy_price_info, sell_price_info)
                    if trade:
                        trades.append(trade)
                        self.notification_service.notify_trade(trade)
        
        return trades

    def update_ui(self, trades: List[Trade]):
        """Updates the table with the new trade data."""
        table_data = []
        for t in trades:
            item_info = self.metadata_loader.get_item_info(t.item_id)
            item_name = item_info["LocalizedName"] if item_info else t.item_id
            table_data.append((
                item_name,
                t.quality,
                t.city_buy,
                t.city_sell,
                f"{t.buy_price:,}",
                f"{t.sell_price:,}",
                f"{t.unit_profit:,.0f}",
                f"{t.roi:.2%}",
                f"{t.trip_profit:,.0f}",
                f"{t.silver_per_kg:,.2f}"
            ))
        
        # Sort by ROI descending
        table_data.sort(key=lambda x: float(x[7].strip('%')), reverse=True)
        self.table_view.update_table(table_data)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
