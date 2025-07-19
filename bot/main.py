from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import os

# Initialize bot and dispatcher
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Optional: Register your handlers here
# Example: @dp.message(...)
# async def start_handler(message: Message):
#     await message.answer("Hello!")

# Webhook startup function
async def on_startup(app):
    await bot.set_webhook("https://telegram-wallet-bot-q611.onrender.com/webhook")

# Aiohttp app and webhook setup
app = web.Application()
app.on_startup.append(on_startup)

SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/webhook")
setup_application(app, dp)

# Run the app
if __name__ == "__main__":
    web.run_app(app, port=int(os.environ.get('PORT', 8080)))