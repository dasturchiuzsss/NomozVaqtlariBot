import asyncio
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware, Dispatcher, Bot
from aiogram.types import TelegramObject, User, Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from config import Config
from database import get_user, get_all_channels
from translations import get_text
from keyboards import get_subscription_markup, get_main_menu_keyboard
from channel_utils import check_user_subscribed

class UserLanguageMiddleware(BaseMiddleware):
	async def __call__(
		  self,
		  handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
		  event: TelegramObject,
		  data: Dict[str, Any]
	) -> Any:
		user: User = data.get("event_from_user")
		
		if user:
			# Get user from database
			db_user = await get_user(user.id)
			
			# Set language for this user
			if db_user and db_user.language:
				data["user_language"] = db_user.language
			else:
				data["user_language"] = "uz"  # Default language
		else:
			data["user_language"] = "uz"  # Default language
		
		return await handler(event, data)

class SubscriptionCheckMiddleware(BaseMiddleware):
	def __init__(self, bot: Bot):
		self.bot = bot
		super().__init__()
	
	
	async def __call__(
		  self,
		  handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
		  event: TelegramObject,
		  data: Dict[str, Any]
	) -> Any:
		# Start buyrug'ini tekshirmasdan o'tkazib yuborish
		if isinstance(event, Message) and event.text and event.text.startswith("/start"):
			return await handler(event, data)
		
		# Admin buyruqlarini tekshirmasdan o'tkazib yuborish
		if isinstance(event, Message) and event.text and (
			  event.text.startswith("/admin") or event.text.startswith("/panel")):
			config = Config()
			user: User = data.get("event_from_user")
			if user and user.id == config.ADMIN_ID:
				return await handler(event, data)
		
		# A'zolikni tekshirish callback ni tekshirmasdan o'tkazib yuborish
		if isinstance(event, CallbackQuery) and event.data and event.data == "check_subscription":
			return await handler(event, data)
		
		# Language tanlash callback ni tekshirmasdan o'tkazib yuborish
		if isinstance(event, CallbackQuery) and event.data and event.data.startswith("language:"):
			return await handler(event, data)
		
		user: User = data.get("event_from_user")
		
		if not user:
			return await handler(event, data)
		
		# Adminni tekshirmasdan o'tkazib yuborish
		config = Config()
		if user.id == config.ADMIN_ID:
			return await handler(event, data)
		
		# Foydalanuvchini ma'lumotlar bazasidan olish
		db_user = await get_user(user.id)
		if not db_user:
			return await handler(event, data)
		
		# Ro'yxatdan o'tish jarayonidagi foydalanuvchilarni tekshirmasdan o'tkazib yuborish
		# Til, telefon va joylashuv kiritish jarayonida tekshirmaslik
		from aiogram.fsm.context import FSMContext
		state = data.get("state")
		if state:
			current_state = await state.get_state()
			if current_state:  # Agar holat mavjud bo'lsa
				return await handler(event, data)
		
		# Foydalanuvchi kanalga a'zo bo'lganligini tekshirish
		is_subscribed = await check_user_subscribed(user.id, self.bot)
		
		if not is_subscribed:
			# Kanallar ro'yxatini olish
			channels = await get_all_channels()
			
			if channels and len(channels) > 0:
				# Foydalanuvchi tilini olish
				user_language = db_user.language if db_user else "uz"
				
				# A'zo bo'lish haqida xabar yuborish
				if isinstance(event, Message):
					await event.answer(
						get_text("subscription_required", user_language),
						reply_markup=get_subscription_markup(channels, user_language)
					)
				elif isinstance(event, CallbackQuery):
					await event.message.answer(
						get_text("subscription_required", user_language),
						reply_markup=get_subscription_markup(channels, user_language)
					)
					await event.answer(get_text("subscription-needed", user_language), show_alert=True)
				
				# Handlerni to'xtatish
				return None
		
		# Barcha tekshiruvlardan o'tgan bo'lsa, handlerni chaqirish
		return await handler(event, data)

def setup_middlewares(dp: Dispatcher, bot: Bot, config: Config):
	# Register user language middleware
	dp.update.middleware(UserLanguageMiddleware())
	
	# Register subscription check middleware
	dp.update.middleware(SubscriptionCheckMiddleware(bot))

