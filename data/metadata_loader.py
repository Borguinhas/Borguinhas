
import os
import requests
import json
import time
import logging
from typing import Dict, List
from config.constants import STARTUP_TARGET_SECONDS

class MetadataLoader:
    ITEMS_URL = "https://raw.githubusercontent.com/ao-data/ao-bin-dumps/master/formatted/items.json"
    WORLD_URL = "https://raw.githubusercontent.com/ao-data/ao-bin-dumps/master/formatted/world.json"
    
    def __init__(self, data_dir=None):
        if data_dir is None:
            # Place metadata files in the 'data' directory
            self.data_dir = os.path.dirname(__file__)
        else:
            self.data_dir = data_dir
        
        self.items_path = os.path.join(self.data_dir, "items.json")
        self.world_path = os.path.join(self.data_dir, "world.json")
        self.items: Dict = {}
        self.locations: Dict = {}

    def sync_metadata(self):
        """Downloads the latest metadata if it's missing or older than 7 days."""
        start_time = time.time()
        
        # Ensure the data directory exists
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        # Check and download items.json
        self._download_if_needed(self.ITEMS_URL, self.items_path)
        
        # Check and download world.json
        self._download_if_needed(self.WORLD_URL, self.world_path)

        # Load into memory
        self._load_metadata()
        
        elapsed_time = time.time() - start_time
        logging.info(f"Metadata synced in {elapsed_time:.2f} seconds.")
        if elapsed_time > STARTUP_TARGET_SECONDS:
            logging.warning(f"Startup time ({elapsed_time:.2f}s) exceeded target ({STARTUP_TARGET_SECONDS}s).")

    def _download_if_needed(self, url: str, path: str):
        """Downloads a file if it doesn't exist or is older than 7 days."""
        needs_download = False
        if not os.path.exists(path):
            needs_download = True
        else:
            file_age_days = (time.time() - os.path.getmtime(path)) / (24 * 3600)
            if file_age_days > 7:
                needs_download = True
        
        if needs_download:
            logging.info(f"Downloading latest metadata from {url}...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            with open(path, "w", encoding="utf-8") as f:
                json.dump(response.json(), f)

    def _load_metadata(self):
        """Parses metadata files into memory-efficient dictionaries."""
        with open(self.items_path, "r", encoding="utf-8") as f:
            items_data = json.load(f)
            # Optimize items: item_id as key
            for item in items_data:
                self.items[item["UniqueName"]] = {
                    "LocalizedName": item.get("LocalizedNames", {}).get("PT-BR") or item.get("LocalizedNames", {}).get("EN-US"),
                    "Weight": item.get("Weight", 0.0),
                    "Category": item.get("ItemCategory", ""),
                    "Tier": item.get("Tier", 0)
                }
        
        with open(self.world_path, "r", encoding="utf-8") as f:
            world_data = json.load(f)
            # Optimize locations: Index as key
            for loc in world_data:
                self.locations[loc["Index"]] = loc["UniqueName"]

    def get_item_info(self, item_id: str) -> Dict | None:
        return self.items.get(item_id)

    def get_location_name(self, location_id: str) -> str | None:
        return self.locations.get(location_id)
