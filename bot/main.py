import asyncio
import aiogram
import logging
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from config import settings as cfg


dp = Dispatcher()
bot = Bot(token=cfg.TOKEN_BOT)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("error.log"),
        logging.StreamHandler()
    ]
)
async def main():
    try:
        
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)


    except Exception as e:
        if "400" in str(e):
            logging.error("Ошибка инициализации бота. Проверьте правильность токена.", filename= "error.log")
        else:
            print(e)


@dp.message(CommandStart())
async def start(message):
    await message.answer("Привет! я бот")
    
@dp.message(F.text.in_(["узнать айди", "узнать id", "id"]))
async def get_id(message: Message):
    await message.answer(f"Ваш ID: {message.from_user.id}")
    
if __name__ == '__main__':
    asyncio.run(main())