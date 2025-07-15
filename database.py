import asyncio
import os
import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Float, Text, select, inspect, func, DateTime, text

from config import Config

config = Config()

# Create async engine for SQLite
engine = create_async_engine(config.database_url, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Create base model
Base = declarative_base()

class User(Base):
	__tablename__ = "users"
	
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, unique=True, nullable=False)
	first_name = Column(String(255))
	phone_number = Column(String(20))
	latitude = Column(Float, nullable=True)
	longitude = Column(Float, nullable=True)
	location_name = Column(String(255), nullable=True)
	language = Column(String(2), default="uz")
	created_at = Column(DateTime, default=datetime.datetime.utcnow)  # Qo'shilgan vaqt
	
	
	def __repr__(self):
		return f"<User(id={self.id}, user_id={self.user_id}, language={self.language})>"

class Channel(Base):
	__tablename__ = "channels"
	
	id = Column(Integer, primary_key=True)
	channel_id = Column(String(255), unique=True, nullable=False)
	channel_url = Column(String(255), nullable=False)
	
	
	def __repr__(self):
		return f"<Channel(id={self.id}, channel_id={self.channel_id})>"

async def create_tables():
	# Eski ma'lumotlar bazasini zaxiralash
	if os.path.exists(config.DATABASE_PATH):
		backup_path = f"{config.DATABASE_PATH}.backup"
		try:
			# Eski ma'lumotlar bazasini zaxiralash
			with open(config.DATABASE_PATH, 'rb') as src, open(backup_path, 'wb') as dst:
				dst.write(src.read())
			print(f"Ma'lumotlar bazasi zaxiralandi: {backup_path}")
		except Exception as e:
			print(f"Ma'lumotlar bazasini zaxiralashda xatolik: {e}")
	
	# Jadvallarni yaratish
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)
	
	# Agar location_name ustuni mavjud bo'lmasa, uni qo'shish
	await add_location_name_column()
	
	# Agar created_at ustuni mavjud bo'lmasa, uni qo'shish
	await add_created_at_column()

async def add_location_name_column():
	"""Ma'lumotlar bazasiga location_name ustunini qo'shish"""
	try:
		# SQLite uchun to'g'ridan-to'g'ri SQL so'rovni bajarish
		async with engine.connect() as conn:
			# Avval ustun mavjudligini tekshirish
			result = await conn.execute(text("PRAGMA table_info(users)"))
			columns = result.fetchall()
			column_names = [column[1] for column in columns]
			
			if "location_name" not in column_names:
				# Ustun mavjud bo'lmasa, uni qo'shish
				await conn.execute(text("ALTER TABLE users ADD COLUMN location_name VARCHAR(255)"))
				await conn.commit()
				print("location_name ustuni muvaffaqiyatli qo'shildi")
			else:
				print("location_name ustuni allaqachon mavjud")
	except Exception as e:
		print(f"location_name ustunini qo'shishda xatolik: {e}")

async def add_created_at_column():
	"""Ma'lumotlar bazasiga created_at ustunini qo'shish"""
	try:
		# SQLite uchun to'g'ridan-to'g'ri SQL so'rovni bajarish
		async with engine.connect() as conn:
			# Avval ustun mavjudligini tekshirish
			result = await conn.execute(text("PRAGMA table_info(users)"))
			columns = result.fetchall()
			column_names = [column[1] for column in columns]
			
			if "created_at" not in column_names:
				# Ustun mavjud bo'lmasa, uni qo'shish
				await conn.execute(text("ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"))
				await conn.commit()
				print("created_at ustuni muvaffaqiyatli qo'shildi")
			else:
				print("created_at ustuni allaqachon mavjud")
	except Exception as e:
		print(f"created_at ustunini qo'shishda xatolik: {e}")

async def get_session():
	async with async_session() as session:
		yield session

# User database operations
async def get_user(user_id: int):
	async with async_session() as session:
		result = await session.execute(select(User).where(User.user_id == user_id))
		return result.scalars().first()

async def get_user_by_id(user_id: int):
	"""ID bo'yicha foydalanuvchini olish"""
	async with async_session() as session:
		result = await session.execute(select(User).where(User.id == user_id))
		return result.scalars().first()

async def get_all_users():
	"""Barcha foydalanuvchilarni olish"""
	async with async_session() as session:
		result = await session.execute(select(User))
		return result.scalars().all()

async def create_user(user_id: int, first_name: str, language: str = "uz"):
	async with async_session() as session:
		# Check if user already exists
		existing_user = await get_user(user_id)
		if existing_user:
			return existing_user
		
		# Create new user
		user = User(user_id=user_id, first_name=first_name, language=language)
		session.add(user)
		await session.commit()
		await session.refresh(user)
		return user

async def update_user_language(user_id: int, language: str):
	async with async_session() as session:
		result = await session.execute(select(User).where(User.user_id == user_id))
		user = result.scalars().first()
		
		if user:
			user.language = language
			await session.commit()
			return True
		return False

async def update_user_phone(user_id: int, phone_number: str):
	async with async_session() as session:
		result = await session.execute(select(User).where(User.user_id == user_id))
		user = result.scalars().first()
		
		if user:
			user.phone_number = phone_number
			await session.commit()
			return True
		return False

async def update_user_location(user_id: int, latitude: float, longitude: float, location_name: str = None):
	async with async_session() as session:
		result = await session.execute(select(User).where(User.user_id == user_id))
		user = result.scalars().first()
		
		if user:
			user.latitude = latitude
			user.longitude = longitude
			if location_name:
				user.location_name = location_name
			await session.commit()
			return True
		return False

async def get_user_location(user_id: int):
	"""Foydalanuvchi joylashuvini olish"""
	async with async_session() as session:
		result = await session.execute(select(User).where(User.user_id == user_id))
		user = result.scalars().first()
		
		if user and user.latitude and user.longitude:
			return (user.latitude, user.longitude)
		return (None, None)

# Statistics operations
async def get_total_users_count():
	"""Jami foydalanuvchilar sonini olish"""
	async with async_session() as session:
		result = await session.execute(select(func.count()).select_from(User))
		return result.scalar()

async def get_users_count_by_period(days: int):
	"""Ma'lum davr ichida qo'shilgan foydalanuvchilar sonini olish"""
	async with async_session() as session:
		date_from = datetime.datetime.utcnow() - datetime.timedelta(days=days)
		result = await session.execute(
			select(func.count()).select_from(User).where(User.created_at >= date_from)
		)
		return result.scalar()

# Channel operations
async def add_channel(channel_id: str, channel_url: str):
	"""Yangi kanal qo'shish"""
	async with async_session() as session:
		# Check if channel already exists
		result = await session.execute(select(Channel).where(Channel.channel_id == channel_id))
		existing_channel = result.scalars().first()
		
		if existing_channel:
			# Update existing channel
			existing_channel.channel_url = channel_url
			await session.commit()
			return existing_channel
		
		# Create new channel
		channel = Channel(channel_id=channel_id, channel_url=channel_url)
		session.add(channel)
		await session.commit()
		await session.refresh(channel)
		return channel

async def get_all_channels():
	"""Barcha kanallarni olish"""
	async with async_session() as session:
		result = await session.execute(select(Channel))
		return result.scalars().all()

async def get_channel_by_id(channel_id: str):
	"""Kanal ID bo'yicha kanalini olish"""
	async with async_session() as session:
		result = await session.execute(select(Channel).where(Channel.channel_id == channel_id))
		return result.scalars().first()

async def delete_channel(channel_id: str):
	"""Kanalni o'chirish"""
	async with async_session() as session:
		result = await session.execute(select(Channel).where(Channel.channel_id == channel_id))
		channel = result.scalars().first()
		
		if channel:
			await session.delete(channel)
			await session.commit()
			return True
		return False

