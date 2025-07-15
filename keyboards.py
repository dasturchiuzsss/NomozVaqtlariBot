from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from translations import get_text

def get_main_menu(language: str = "uz") -> ReplyKeyboardMarkup:
	"""Asosiy menyu tugmalarini yaratish"""
	keyboard = ReplyKeyboardMarkup(
		keyboard=[
			[KeyboardButton(text=get_text("about-bot", language))]
		],
		resize_keyboard=True
	)
	return keyboard

# Проверим, что функция get_main_menu_keyboard правильно создает клавиатуру

def get_main_menu_keyboard(language: str = "uz") -> ReplyKeyboardMarkup:
	"""Asosiy menyu tugmalarini yaratish"""
	keyboard = ReplyKeyboardMarkup(
		keyboard=[
			[KeyboardButton(text="🕌 " + get_text("prayer_times", language))],
			[KeyboardButton(text="🧭 " + get_text("qibla_button", language)),
			 KeyboardButton(text="📖 " + get_text("quran_button", language))],
			[KeyboardButton(text="📿 " + get_text("tasbeh_button", language)),
			 KeyboardButton(text="🧠 " + get_text("organ_button", language))],
			[KeyboardButton(text="📍 " + get_text("location_button", language)),
			 KeyboardButton(text=get_text("change_language", language))]
		],
		resize_keyboard=True
	)
	return keyboard

def get_admin_menu() -> ReplyKeyboardMarkup:
	"""Admin menyu tugmalarini yaratish (eski versiya)"""
	keyboard = ReplyKeyboardMarkup(
		keyboard=[
			[KeyboardButton(text="📊 Statistika"), KeyboardButton(text="📢 Majburiy kanallar")],
			[KeyboardButton(text="📨 Xabar yuborish")]
		],
		resize_keyboard=True
	)
	return keyboard

def get_admin_menu_inline() -> InlineKeyboardMarkup:
	"""Admin menyu tugmalarini inline versiyasi"""
	keyboard = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(text="📊 Statistika", callback_data="admin:statistics"),
				InlineKeyboardButton(text="📢 Majburiy kanallar", callback_data="admin:channels")
			],
			[
				InlineKeyboardButton(text="📨 Xabar yuborish", callback_data="admin:broadcast"),
				InlineKeyboardButton(text="👤 Foydalanuvchilar", callback_data="admin:users")
			],
			[
				InlineKeyboardButton(text="🕌 Namoz vaqtlari", callback_data="admin:prayer_times")
			]
		]
	)
	return keyboard

def get_admin_statistics_menu() -> InlineKeyboardMarkup:
	"""Admin statistika menyusi"""
	keyboard = InlineKeyboardMarkup(
		inline_keyboard=[
			[InlineKeyboardButton(text="📅 Oy/Kunlar", callback_data="admin:period_stats")],
			[InlineKeyboardButton(text="🔙 Orqaga", callback_data="admin:back")]
		]
	)
	return keyboard

def get_admin_channels_menu_inline() -> InlineKeyboardMarkup:
	"""Admin kanallar menyusi (inline versiya)"""
	keyboard = InlineKeyboardMarkup(
		inline_keyboard=[
			[InlineKeyboardButton(text="➕ Kanal qo'shish", callback_data="admin:add_channel")],
			[InlineKeyboardButton(text="📋 Kanallar ro'yxati", callback_data="admin:list_channels")],
			[InlineKeyboardButton(text="🔙 Orqaga", callback_data="admin:back")]
		]
	)
	return keyboard

def get_admin_users_menu_inline() -> InlineKeyboardMarkup:
	"""Admin foydalanuvchilar menyusi (inline versiya)"""
	keyboard = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(text="🆔 Chat ID orqali", callback_data="admin:user_by_chat_id"),
				InlineKeyboardButton(text="🔢 Bot ID orqali", callback_data="admin:user_by_bot_id")
			],
			[InlineKeyboardButton(text="🔙 Orqaga", callback_data="admin:back")]
		]
	)
	return keyboard

def get_admin_broadcast_menu_inline() -> InlineKeyboardMarkup:
	"""Admin xabar yuborish menyusi (inline versiya)"""
	keyboard = InlineKeyboardMarkup(
		inline_keyboard=[
			[
				InlineKeyboardButton(text="📝 Oddiy xabar", callback_data="admin:regular_message"),
				InlineKeyboardButton(text="↪️ Forward xabar", callback_data="admin:forward_message")
			],
			[InlineKeyboardButton(text="🔙 Orqaga", callback_data="admin:back")]
		]
	)
	return keyboard

def get_admin_broadcast_menu() -> ReplyKeyboardMarkup:
	"""Admin xabar yuborish menyusi (eski versiya)"""
	keyboard = ReplyKeyboardMarkup(
		keyboard=[
			[KeyboardButton(text="📝 Oddiy xabar"), KeyboardButton(text="↪️ Forward xabar")],
			[KeyboardButton(text="🔙 Orqaga")]
		],
		resize_keyboard=True
	)
	return keyboard

def get_channel_list_markup(channels) -> InlineKeyboardMarkup:
	"""Kanallar ro'yxati uchun inline tugmalar"""
	keyboard = InlineKeyboardMarkup(inline_keyboard=[])
	
	for channel in channels:
		keyboard.inline_keyboard.append([
			InlineKeyboardButton(
				text=channel.channel_url,
				url=f"https://t.me/{channel.channel_url.replace('@', '')}" if channel.channel_url.startswith(
					'@') else channel.channel_url
			),
			InlineKeyboardButton(
				text="❌ O'chirish",
				callback_data=f"admin:remove_channel:{channel.channel_id}"
			)
		])
	
	# Orqaga qaytish tugmasini qo'shamiz
	keyboard.inline_keyboard.append([
		InlineKeyboardButton(text="🔙 Orqaga", callback_data="admin:channels")
	])
	
	return keyboard

def get_subscription_markup(channels, language: str = "uz") -> InlineKeyboardMarkup:
	"""A'zolik tekshirish uchun inline tugmalar"""
	keyboard = []
	
	# Har bir kanal uchun alohida tugma qo'shamiz
	for channel in channels:
		channel_url = f"https://t.me/{channel.channel_id}" if not channel.channel_id.startswith(
			'@') else f"https://t.me/{channel.channel_id[1:]}"
		keyboard.append([
			InlineKeyboardButton(
				text=f"➕ {channel.channel_id}",
				url=channel_url
			)
		])
	
	# Tekshirish tugmasini qo'shamiz
	keyboard.append([
		InlineKeyboardButton(
			text="✅ Tekshirish",
			callback_data="check_subscription"
		)
	])
	
	return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_cancel_button() -> ReplyKeyboardMarkup:
	"""Bekor qilish tugmasi"""
	keyboard = ReplyKeyboardMarkup(
		keyboard=[
			[KeyboardButton(text="❌ Bekor qilish")]
		],
		resize_keyboard=True
	)
	return keyboard

def get_cancel_button_inline() -> InlineKeyboardMarkup:
	"""Bekor qilish tugmasi (inline versiya)"""
	keyboard = InlineKeyboardMarkup(
		inline_keyboard=[
			[InlineKeyboardButton(text="❌ Bekor qilish", callback_data="admin:cancel")]
		]
	)
	return keyboard

def get_location_keyboard(language: str) -> ReplyKeyboardMarkup:
	"""Joylashuv yuborish klaviaturasini yaratish"""
	keyboard = [
		[KeyboardButton(text=get_text("location_button", language), request_location=True)]
	]
	return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)

def get_prayer_times_keyboard(language: str, latitude: float, longitude: float) -> InlineKeyboardMarkup:
	"""Namoz vaqtlari uchun inline klaviatura"""
	keyboard = [
		[InlineKeyboardButton(text=get_text("nearby_mosques", language),
		                      web_app=WebAppInfo(
			                      url=f"https://www.google.com/maps/search/mosque/@{latitude},{longitude},14z"))],
		[InlineKeyboardButton(text=get_text("developer_button", language),
		                      web_app=WebAppInfo(url="https://roobotmee.uz"))],
		[InlineKeyboardButton(text=get_text("feedback_button", language), url="https://t.me/roobotmee")]
	]
	return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_qibla_keyboard(language: str, qibla_url: str) -> InlineKeyboardMarkup:
	"""Qibla yo'nalishi uchun inline klaviatura"""
	keyboard = [
		[InlineKeyboardButton(text=get_text("open_qibla", language), web_app=WebAppInfo(url=qibla_url))],
		[
			InlineKeyboardButton(text=get_text("developer_button", language),
			                     web_app=WebAppInfo(url="https://roobotmee.uz")),
			InlineKeyboardButton(text=get_text("feedback_button", language), url="https://t.me/roobotmee")
		]
	]
	return InlineKeyboardMarkup(inline_keyboard=keyboard)

