# main_menu.py
# Asosiy menyu uchun kod

from telegram import ReplyKeyboardMarkup, KeyboardButton, Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import CallbackContext

def main_menu(update: Update, context: CallbackContext) -> None:
	"""Asosiy menyuni yuboradi"""
	keyboard = [
		[KeyboardButton("⏰ Namoz vaqtlari"), KeyboardButton("🧭 Qibla yo'nalishi")],
		[KeyboardButton("📿 Elektron tasbeh"), KeyboardButton("📜 Kunlik hadis")],
		[KeyboardButton("📖 Islomiy ma'lumotlar"), KeyboardButton("🤲 Duolar to'plami")],
		[KeyboardButton("💰 Ehson qilish"), KeyboardButton("📝 Fikr bildirish")]
	]
	
	reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
	
	update.message.reply_text(
		"Assalomu alaykum! Namoz vaqtlari botiga xush kelibsiz.\n"
		"Quyidagi menyudan kerakli bo'limni tanlang:",
		reply_markup=reply_markup
	)

def handle_donation_button(update: Update, context: CallbackContext) -> None:
	"""Ehson qilish tugmasi bosilganda ishga tushadi"""
	keyboard = [
		[
			InlineKeyboardButton(
				"💰 Ehson qilish",
				web_app=WebAppInfo(url="https://vaqf.uz")
			)
		],
		[
			InlineKeyboardButton(
				"👨‍💻 Dasturchi",
				url="https://t.me/roobotmee"
			)
		],
		[
			InlineKeyboardButton(
				"📝 Fikr bildirish",
				callback_data="feedback"
			)
		]
	]
	
	reply_markup = InlineKeyboardMarkup(keyboard)
	
	update.message.reply_text(
		"Botni rivojlantirish va qo'llab-quvvatlash uchun ehson qilishingiz mumkin:",
		reply_markup=reply_markup
	)

def handle_feedback_button(update: Update, context: CallbackContext) -> None:
	"""Fikr bildirish tugmasi bosilganda ishga tushadi"""
	update.message.reply_text(
		"Fikr va takliflaringizni yozib qoldiring. "
		"Sizning fikrlaringiz bot xizmatini yaxshilashga yordam beradi."
	)
	
	# Foydalanuvchi keyingi xabarini fikr sifatida qabul qilish uchun holat o'rnatamiz
	context.user_data["waiting_for_feedback"] = True

