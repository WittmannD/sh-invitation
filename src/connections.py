from pyrogram import Client

from src.config import current_config

bot = Client(current_config.TELEGRAM_SESSION, api_id=current_config.TELEGRAM_API_ID,
             api_hash=current_config.TELEGRAM_API_HASH, phone_number=current_config.TELEGRAM_PHONE_NUMBER)
