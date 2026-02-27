
# API Configuration
ALBION_API_BASE_URL = "https://west.albion-online-data.com/api/v2/"
ALBION_API_SERVER = "europe"
API_TIMEOUT = 5  # seconds
API_RETRIES = 3
API_BACKOFF_FACTOR = 0.5
MAX_ITEMS_PER_BATCH = 200

# Black Market Configuration
BLACK_MARKET_CITY_ID = "1007"
BLACK_MARKET_TRASH_RATE = 0.10
BLACK_MARKET_EQUIPMENT_CATEGORIES = ["weapon", "armor", "offhand"]

# Tax Configuration
PREMIUM_TAX_RATE = 0.04
NON_PREMIUM_TAX_RATE = 0.08

# Profit Calculation Thresholds
MIN_ROI_PERCENTAGE = 0.03  # 3%
MIN_SPREAD_PERCENTAGE = 0.03 # 3%
MIN_VOLUME = 10

# Database Configuration
DATABASE_NAME = "market.db"
DATABASE_PURGE_DAYS = 1  # 24 hours

# Notification Configuration
NOTIFICATION_COOLDOWN_MINUTES = 15

# Performance Targets (for reference)
STARTUP_TARGET_SECONDS = 2
API_BATCH_TARGET_SECONDS = 8
UI_RESPONSE_TARGET_MS = 100
MEMORY_USAGE_TARGET_MB = 200

# Other Constants
MOUNT_CAPACITY = 1000  # Example value, needs to be dynamic or configured
