import asyncio
import os
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

from handlers import start, handle_callback, handle_wallet

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create bot instance with HTML parse mode
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

# Create Dispatcher with in-memory storage
dp = Dispatcher(storage=MemoryStorage())

# Register handlers
dp.message.register(start, F.text == "/start")
dp.callback_query.register(handle_callback)
dp.message.register(handle_wallet)

# Run the bot
async def main():
    print("Bot is starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())