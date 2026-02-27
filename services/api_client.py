
import requests
import time
import logging
from typing import List, Dict, Optional
from config.constants import ALBION_API_BASE_URL, ALBION_API_SERVER, API_TIMEOUT, API_RETRIES, API_BACKOFF_FACTOR, MAX_ITEMS_PER_BATCH

class APIClient:
    def __init__(self, base_url: str = ALBION_API_BASE_URL, server: str = ALBION_API_SERVER):
        self.base_url = base_url
        self.server = server
        self.session = requests.Session()

    def fetch_prices(self, item_ids: List[str], locations: List[str], qualities: List[int]) -> List[Dict]:
        """Fetches market prices for given items, locations, and qualities."""
        # Max items per batch is 200, but we need to consider locations and qualities too.
        # The API allows batching items, locations, and qualities in a single request.
        
        # Batching items in groups of MAX_ITEMS_PER_BATCH
        all_results = []
        for i in range(0, len(item_ids), MAX_ITEMS_PER_BATCH):
            batch_items = item_ids[i:i + MAX_ITEMS_PER_BATCH]
            results = self._fetch_batch(batch_items, locations, qualities)
            all_results.extend(results)
        
        return all_results

    def _fetch_batch(self, items: List[str], locations: List[str], qualities: List[int]) -> List[Dict]:
        """Fetches a single batch of market prices."""
        items_str = ",".join(items)
        locations_str = ",".join(locations)
        qualities_str = ",".join(map(str, qualities))
        
        url = f"{self.base_url}prices/{items_str}"
        params = {
            "locations": locations_str,
            "qualities": qualities_str,
            "server": self.server
        }
        
        for attempt in range(API_RETRIES):
            try:
                response = self.session.get(url, params=params, timeout=API_TIMEOUT)
                
                if response.status_code == 429:
                    logging.warning(f"Rate limit exceeded (429). Retrying in {API_BACKOFF_FACTOR * (2 ** attempt)}s...")
                    time.sleep(API_BACKOFF_FACTOR * (2 ** attempt))
                    continue
                
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.RequestException as e:
                logging.error(f"API request failed (attempt {attempt + 1}/{API_RETRIES}): {e}")
                if attempt < API_RETRIES - 1:
                    time.sleep(API_BACKOFF_FACTOR * (2 ** attempt))
                else:
                    return []
        
        return []
