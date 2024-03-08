# from aiogram import Bot,Dispatcher,types,exceptions
# from config import token
# import logging,aioschedule,asyncio

# bot = Bot(token=token)
# dp = Dispatcher(bot)
# logging.basicConfig(level=logging.INFO)
# @dp.message_handler(commands="start")
# async def start(message:types.Message):
#     await message.answer("привет")
 
# async def send_message():
#     await bot.send_message(-4000645080,"Привет")

# async def scheduler():
#     aioschedule.every(2).seconds.do(send_message)
#     while True:
#         await aioschedule.run_pending()
#         await asyncio.create_task(scheduler())

# executor.start_polling(dp,skip_upates=True,on_startup=on_startup)

from aiogram import Bot, Dispatcher, types, executor
from config import token
import logging, aioschedule, asyncio, requests

bot = Bot(token=token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

BITCOIN_API_URL = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer("Привет!")

async def send_bitcoin_price():
    response = requests.get(BITCOIN_API_URL)
    if response.status_code == 200:
        bitcoin_data = response.json()
        price = bitcoin_data["bpi"]["USD"]["rate"]
        await bot.send_message(-4000645080, f"Текущая стоимость биткоина: {price}")
    else:
        await bot.send_message(-4000645080, "Не удалось получить текущую стоимость биткоина")

async def scheduler():
    aioschedule.every(2).seconds.do(send_bitcoin_price)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(parameter):
    asyncio.create_task(scheduler())

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
