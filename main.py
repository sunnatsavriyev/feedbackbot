import os
import django
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_polling
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from asgiref.sync import sync_to_async
from apscheduler.schedulers.asyncio import AsyncIOScheduler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from feedback.models import Feedback

load_dotenv()  # Load environment variables from a .env file
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

# Configure logging
logging.basicConfig(level=logging.INFO)

class FeedbackStates(StatesGroup):
    waiting_for_feedback = State()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(
        "Salom! Fikr va mulohazalaringizni qabul qilamiz. Fikr va mulohazalaringizni yuboring:"
    )
    await FeedbackStates.waiting_for_feedback.set()


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    help_text = (
        "Botdan foydalanish bo'yicha yordam:\n"
        "/start - Botni ishga tushirish va fikr va mulohazalarni yuborish\n"
        "Fikr va mulohazalaringizni qayta yuborish uchun 'Ha' tugmasini bosing va, "
        "Yuborilgan fikr va mulohazalaringiz qabul qilinadi va saqlanadi.\n "
        "Agar 'Yo'q' tugmasini bossangiz, fikr va mulohazalaringiz qabul qilinmaydi. Keyingi gal start tugmasi bilan yuborasiz"
    )
    await message.reply(help_text)


@dp.message_handler(state=FeedbackStates.waiting_for_feedback)
async def handle_feedback(message: types.Message, state: FSMContext):
    feedback_text = message.text

    await sync_to_async(Feedback.objects.create)(feedback=feedback_text)

    # Create buttons for "Ha" and "Yo'q"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Ha", callback_data="yes"))
    markup.add(types.InlineKeyboardButton("Yo'q", callback_data="no"))

    # Send confirmation message with buttons
    await message.reply(
        "Fikr va mulohazangiz qabul qilindi, Raxmat! \n Yana fikr va mulohazalaringiz bormi?",
        reply_markup=markup
    )
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'yes')
async def process_callback_yes(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Fikr va mulohazalaringizni yuboring:")
    await FeedbackStates.waiting_for_feedback.set()

@dp.callback_query_handler(lambda c: c.data == 'no')
async def process_callback_no(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Raxmat! Yana fikr va mulohazalaringizni kutamiz.(/start orqali)")

async def on_startup(dp):
    logging.info("Bot ishga tushdi...")

async def on_shutdown(dp):
    logging.info("Bot to'xtadi...")

if __name__ == '__main__':
    # Start polling
    start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
