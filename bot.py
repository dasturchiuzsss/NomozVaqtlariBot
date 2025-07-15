import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import Config
from handlers import register_all_handlers
from middlewares import setup_middlewares
from database import create_tables, get_all_channels

# Configure logging
logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
	handlers=[
		logging.FileHandler("bot.log"),
		logging.StreamHandler(sys.stdout)
	]
)
logger = logging.getLogger(__name__)

async def main():
	# Load config
	config = Config()
	
	# Initialize bot and dispatcher
	# Yangi sintaksis bilan DefaultBotProperties ishlatamiz
	bot = Bot(
		token=config.BOT_TOKEN,
		default=DefaultBotProperties(parse_mode=ParseMode.HTML)
	)
	dp = Dispatcher(storage=MemoryStorage())
	
	# Create database tables
	await create_tables()
	
	# Debug: Check channels in database
	channels = await get_all_channels()
	logger.info(f"Found {len(channels)} channels in database")
	for channel in channels:
		logger.info(f"Channel: @{channel.channel_id} - {channel.channel_url}")
	
	# Register all handlers
	register_all_handlers(dp)
	
	# Setup middlewares
	setup_middlewares(dp, bot, config)
	
	# Log admin ID
	logger.info(f"Admin ID: {config.ADMIN_ID}")
	
	# Start polling
	logger.info("Starting bot...")
	await bot.delete_webhook(drop_pending_updates=True)
	await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
	try:
		asyncio.run(main())
	except (KeyboardInterrupt, SystemExit):
		logger.info("Bot stopped!")
	except Exception as e:
		logger.error(f"Unhandled exception: {e}", exc_info=True)

