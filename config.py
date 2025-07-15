import os
from pathlib import Path
from typing import ClassVar, List
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()

class Config(BaseSettings):
	# Bot settings
	BOT_TOKEN: str = os.getenv("BOT_TOKEN")
	
	# Admin settings
	ADMIN_ID: int = int(os.getenv("ADMIN_ID", "0"))
	
	# Channel settings
	REQUIRED_CHANNELS: ClassVar[List[str]] = [channel for channel in os.getenv("REQUIRED_CHANNELS", "").split(",") if
	                                          channel]
	
	# Path settings
	BASE_DIR: Path = Path(__file__).parent
	DATABASE_PATH: Path = BASE_DIR / "data.db"
	
	# Available languages - add ClassVar annotation
	LANGUAGES: ClassVar[List[str]] = ["uz", "ru", "kk", "ky", "en"]
	DEFAULT_LANGUAGE: ClassVar[str] = "uz"
	
	# API endpoints
	API_BASE: str = "https://api.example.com"
	NAMOZ_API: str = "https://api.aladhan.com/v1/timingsByCity"
	GEOCODE_API: str = "https://nominatim.openstreetmap.org/reverse"
	QIBLA_FINDER_URL: str = "https://qiblafinder.withgoogle.com/"
	
	# Bot version
	BOT_VERSION: str = "1.0.0"
	
	
	@property
	def database_url(self) -> str:
		return f"sqlite+aiosqlite:///{self.DATABASE_PATH}"

# Create a global instance
config = Config()

# Export constants for easy access
TOKEN = config.BOT_TOKEN
ADMIN_USER_ID = str(config.ADMIN_ID)
API_BASE = config.API_BASE
NAMOZ_API = config.NAMOZ_API
GEOCODE_API = config.GEOCODE_API
QIBLA_FINDER_URL = config.QIBLA_FINDER_URL
BOT_VERSION = config.BOT_VERSION

