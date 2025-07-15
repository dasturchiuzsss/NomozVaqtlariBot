import aiohttp
import json
from typing import Optional, Dict, Any

async def get_location_name(latitude: float, longitude: float, language: str = "uz") -> Optional[str]:
	"""
	Kenglik va uzunlik koordinatalarini manzilga aylantirish
	"""
	# Nominatim API URL
	url = f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json&accept-language={language}"
	
	try:
		async with aiohttp.ClientSession() as session:
			async with session.get(url, headers={"User-Agent": "TelegramBot/1.0"}) as response:
				if response.status == 200:
					data = await response.json()
					return format_address(data)
				else:
					return None
	except Exception as e:
		print(f"Geocoding error: {e}")
		return None

def format_address(data: Dict[str, Any]) -> str:
	"""
	Nominatim API dan olingan ma'lumotlarni formatlash
	"""
	address = data.get("address", {})
	
	# Manzil qismlarini olish
	city = address.get("city", "")
	town = address.get("town", "")
	village = address.get("village", "")
	suburb = address.get("suburb", "")
	neighbourhood = address.get("neighbourhood", "")
	road = address.get("road", "")
	state = address.get("state", "")
	country = address.get("country", "")
	
	# Shahar/tuman
	location = city or town or village or ""
	
	# Mahalla/ko'cha
	sub_location = suburb or neighbourhood or ""
	
	# Manzilni formatlash
	formatted_address = ""
	
	if country:
		formatted_address += country
	
	if state and state != location:
		if formatted_address:
			formatted_address += ", "
		formatted_address += state
	
	if location:
		if formatted_address:
			formatted_address += ", "
		formatted_address += location
	
	if sub_location:
		if formatted_address:
			formatted_address += ", "
		formatted_address += sub_location
	
	if road:
		if formatted_address:
			formatted_address += ", "
		formatted_address += road
	
	return formatted_address or "Aniqlanmagan joylashuv"

