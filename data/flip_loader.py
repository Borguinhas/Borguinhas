
import json
import os
from typing import List, Dict

class FlipLoader:
    def __init__(self, data_dir=None):
        if data_dir is None:
            self.data_dir = os.path.dirname(__file__)
        else:
            self.data_dir = data_dir
        
        self.flips_path = os.path.join(self.data_dir, "flips.json")
        self.flips: List[Dict] = []

    def load_flips(self):
        """Loads configured flip pairs (City -> Black Market)."""
        if not os.path.exists(self.flips_path):
            # Default flip configuration if not exists
            self.flips = [
                {"city_buy": "Thetford", "city_sell": "Black Market"},
                {"city_buy": "Lymhurst", "city_sell": "Black Market"},
                {"city_buy": "Bridgewatch", "city_sell": "Black Market"},
                {"city_buy": "Martlock", "city_sell": "Black Market"},
                {"city_buy": "Fort Sterling", "city_sell": "Black Market"},
                {"city_buy": "Caerleon", "city_sell": "Black Market"}
            ]
            self.save_flips()
        else:
            with open(self.flips_path, "r", encoding="utf-8") as f:
                self.flips = json.load(f)

    def save_flips(self):
        """Saves current flip pairs to a JSON file."""
        with open(self.flips_path, "w", encoding="utf-8") as f:
            json.dump(self.flips, f, indent=4)

    def add_flip(self, city_buy: str, city_sell: str):
        """Adds a new flip pair to the configuration."""
        if not any(f["city_buy"] == city_buy and f["city_sell"] == city_sell for f in self.flips):
            self.flips.append({"city_buy": city_buy, "city_sell": city_sell})
            self.save_flips()

    def remove_flip(self, city_buy: str, city_sell: str):
        """Removes a flip pair from the configuration."""
        self.flips = [f for f in self.flips if not (f["city_buy"] == city_buy and f["city_sell"] == city_sell)]
        self.save_flips()
