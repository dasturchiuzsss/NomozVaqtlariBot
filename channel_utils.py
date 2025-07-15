import os
from database import get_all_channels

async def get_required_channels():
	"""Majburiy obuna kanallari ro'yxatini olish"""
	# Ma'lumotlar bazasidan kanallarni olish
	channels = []
	try:
		channels = await get_all_channels()
	except Exception as e:
		print(f"Kanallarni olishda xatolik: {e}")
	
	# Kanallar ro'yxatini qaytarish
	return channels

async def check_user_subscribed(user_id, bot):
	"""Foydalanuvchi kanallarga a'zo bo'lganligini tekshirish"""
	# Kanallar ro'yxatini olish
	channels = await get_required_channels()  # await bilan kutib olish kerak
	
	# Agar kanallar bo'lmasa, True qaytarish
	if not channels:
		return True
	
	# Har bir kanal uchun a'zolikni tekshirish
	for channel in channels:
		try:
			member = await bot.get_chat_member(f"@{channel.channel_id}", user_id)
			if member.status in ["left", "kicked", "banned"]:
				# Agar foydalanuvchi kanalga a'zo bo'lmasa, False qaytarish
				return False
		except Exception as e:
			# Xatolik yuz berganda, bu kanalni o'tkazib yuborish
			print(f"Kanal a'zoligini tekshirishda xatolik: {e}")
			continue
	
	# Barcha kanallarga a'zo bo'lsa, True qaytarish
	return True

