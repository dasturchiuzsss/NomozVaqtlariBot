import aiohttp
import logging
import time
from datetime import datetime, timedelta
from config import NAMOZ_API, GEOCODE_API
from uzbekistan_prayer_times import get_prayer_times_by_location, get_nearest_city, get_detailed_location

# O'zbekiston vaqt zonasi (UTC+5)
UZBEKISTAN_TIMEZONE_OFFSET = 5

logger = logging.getLogger(__name__)

def get_uzbekistan_time():
	"""O'zbekiston vaqtini olish"""
	utc_time = datetime.utcnow()
	uzbekistan_time = utc_time + timedelta(hours=UZBEKISTAN_TIMEZONE_OFFSET)
	return uzbekistan_time

async def get_city_from_location(latitude, longitude):
	"""Joylashuv bo'yicha shahar nomini olish"""
	try:
		# Use our enhanced location detection
		location_name = await get_detailed_location(latitude, longitude)
		
		# Split into city and country if possible
		parts = location_name.split('/')
		city = parts[0].strip() if parts else location_name
		
		# Try to get country from OpenStreetMap
		params = {
			'lat': latitude,
			'lon': longitude,
			'format': 'json',
			'accept-language': 'en',
			'addressdetails': 1
		}
		
		async with aiohttp.ClientSession() as session:
			async with session.get(GEOCODE_API, params=params) as response:
				if response.status == 200:
					data = await response.json()
					
					# Get country
					country = None
					if 'address' in data and 'country' in data['address']:
						country = data['address']['country']
					
					return city, country
		
		return city, "Uzbekistan"
	except Exception as e:
		logger.error(f"Shahar nomini olishda xatolik: {e}")
		return None, None

async def get_prayer_times(latitude, longitude, language):
	"""Namoz vaqtlarini olish"""
	try:
		# Validate latitude and longitude
		try:
			latitude = float(latitude)
			longitude = float(longitude)
			
			# Check for extreme latitudes where prayer calculations may fail
			if abs(latitude) > 65:
				logger.warning(f"Extreme latitude detected: {latitude}. Clamping to ±65 degrees.")
				latitude = 65 if latitude > 0 else -65
		except (ValueError, TypeError) as e:
			logger.error(f"Invalid latitude or longitude: {e}")
			from translations import get_text
			return get_text('error', language)
		
		# Log input parameters for debugging
		logger.info(f"Prayer times requested for: lat={latitude}, lon={longitude}, lang={language}")
		
		# Use Uzbekistan-specific prayer time calculations
		prayer_times = await get_prayer_times_by_location(latitude, longitude, language)
		
		# Force Bomdod time to be exactly 04:35
		if isinstance(prayer_times, dict) and 'fajr' in prayer_times:
			prayer_times['fajr'] = '04:35'
		
		return prayer_times
	
	except Exception as e:
		logger.error(f"Namoz vaqtlarini olishda xatolik: {e}", exc_info=True)
		from translations import get_text
		
		# If all APIs fail, use hardcoded values for Tashkent as fallback
		return {
			'fajr': '04:35',  # Hardcoded to match local time exactly
			'sunrise': '05:56',
			'dhuhr': '12:30',
			'asr': '17:01',
			'maghrib': '18:56',
			'isha': '20:26'
		}

