import os
import asyncio
from aiogram import Bot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = "https://telegram-wallet-bot-q611.onrender.com/webhook"

async def main():
    bot = Bot(token=BOT_TOKEN)
    try:
        await bot.set_webhook(WEBHOOK_URL)
        print("✅ Webhook set successfully!")
    finally:
        await bot.session.close()

asyncio.run(main())