from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import TelegramAPIError
from config import TOKEN_API, HELP_MESSAGE, START_MESSAGE, UNKNOWN_MESSAGE, ERROR_MESSAGE, RES_PREP, PICS_MESSAGE, INPUT_MESSAGE, NOTFOUND_MESSAGE, RES_GEN, resource_kb
from parser import get_imgs_yandex, get_imgs_lexica, get_imgs_tenor, get_videos_cover
import enum
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

bot = Bot(TOKEN_API)
disp = Dispatcher(bot)
chat_states = dict()

class ResourceType(enum.IntEnum):
    YANDEX = 0
    LEXICA = 1
    TENOR = 2
    COVER = 3

@disp.message_handler(commands=['start'])
async def handle_start_command(message: types.Message):
    await message.answer(text=START_MESSAGE, parse_mode='HTML', reply_markup=resource_kb)
    await message.delete()

@disp.message_handler(commands=['help'])
async def handle_start_command(message: types.Message):
    await message.answer(text=HELP_MESSAGE, parse_mode='HTML')
    await message.delete()

@disp.message_handler(commands=['yandex'])
async def handle_start_command(message: types.Message):
    chat_states[message.chat.id] = ResourceType.YANDEX
    await message.answer(text=INPUT_MESSAGE, reply_markup=ReplyKeyboardRemove())
    await message.delete()

@disp.message_handler(commands=['lexica'])
async def handle_start_command(message: types.Message):
    chat_states[message.chat.id] = ResourceType.LEXICA
    await message.answer(text=INPUT_MESSAGE, reply_markup=ReplyKeyboardRemove())
    await message.delete()

@disp.message_handler(commands=['tenor'])
async def handle_start_command(message: types.Message):
    chat_states[message.chat.id] = ResourceType.TENOR
    await message.answer(text=INPUT_MESSAGE, reply_markup=ReplyKeyboardRemove())
    await message.delete()

@disp.message_handler(commands=['cover'])
async def handle_start_command(message: types.Message):
    chat_states[message.chat.id] = ResourceType.COVER
    await message.answer(text=INPUT_MESSAGE, reply_markup=ReplyKeyboardRemove())
    await message.delete()

@disp.message_handler()
async def handle_message(message: types.Message):
    if message.chat.id not in chat_states:
        return await message.reply(text=UNKNOWN_MESSAGE, parse_mode='HTML')

    if chat_states[message.chat.id] == ResourceType.YANDEX:
        media = await get_imgs_yandex(message.text)
    elif chat_states[message.chat.id] == ResourceType.LEXICA:
        media = await get_imgs_lexica(message.text)
    elif chat_states[message.chat.id] == ResourceType.TENOR:
        media = await get_imgs_tenor(message.text)
    elif chat_states[message.chat.id] == ResourceType.COVER:
        media = await get_videos_cover(message.text)

    if media == None:
        return await message.reply(text=ERROR_MESSAGE, parse_mode="HTML")
    if len(media) == 0:
        return await message.reply(text=NOTFOUND_MESSAGE.substitute(res=RES_GEN[int(chat_states[message.chat.id])]), parse_mode="HTML")

    await bot.send_message(chat_id=message.chat.id, text=PICS_MESSAGE.substitute(res=RES_PREP[int(chat_states[message.chat.id])], query=message.text), reply_markup=resource_kb)

    if chat_states[message.chat.id] == ResourceType.TENOR:
        return await bot.send_animation(chat_id=message.chat.id, animation=media[0])
    elif chat_states[message.chat.id] == ResourceType.COVER:
        return await bot.send_document(chat_id=message.chat.id, document=media[0])
    else:
        media_group = types.MediaGroup()
        for ph in media:
            media_group.attach_photo(ph)
    await bot.send_media_group(chat_id=message.chat.id, media=media_group)

@disp.errors_handler()
async def error_handle(update: types.Update, exception):
    await bot.send_message(chat_id=update.message.chat.id, text=ERROR_MESSAGE, reply_markup=resource_kb)
    return True

if __name__ == "__main__":
    executor.start_polling(disp, skip_updates=True)