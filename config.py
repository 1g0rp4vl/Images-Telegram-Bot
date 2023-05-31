from string import Template
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

TOKEN_API = "YOUR TOKEN"
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.5.751 Yowser/2.5 Safari/537.36"
}
yandex_url = "https://yandex.ru/images/search?text="
lexica_url = "https://lexica.art/?q="
tenor_url = "https://tenor.com/ru/search/"
cover_url = "https://coverr.co/s?q="

RES_PREP = ["Яндекс Картинках", "Lexica", "Tenor", "Cover"]
RES_GEN = ["Яндекс Картинок", "Lexica", "Tenor", "Cover"]

HELP_MESSAGE = """
Этот бот способен подгружать медиа-файлы из сторонних ресурсов по вашему запросу.
<b>Доступный функционал</b>:
<b>/start</b> - <em>запустить бота</em>
<b>/help</b> - <em>получить подсказки по использованию бота</em>
<b>/yandex</b> - <em>поиск в Яндекс Картинках</em>
<b>/lexica</b> - <em>поиск в Lexica (фотографии сгенерированные нейросетями)</em>
<b>/tenor</b> - <em>поиск в Tenor (gif-ки)</em>
<b>/cover</b> - <em>поиск в Cover (стоковые видео) (Внимание: короткие видео автоматически преобразуются телеграммом в Mpeg4 формат)</em>
"""

START_MESSAGE = """
Images Bot приветствует вас!
Для получения инструкций по использованию введите <em>/help</em>
"""

UNKNOWN_MESSAGE = """
Я вас не понимаю😔
Для поиска изображений введите /<em>ресурс</em>, подробнее - <em>/help</em>
"""

ERROR_MESSAGE = """
Что-то пошло не так🥶
Попробуйте еще раз, при повторной ошибке попробуйте позднее"""

PICS_MESSAGE = Template('Вот, что я нашел в $res по запросу $query')

INPUT_MESSAGE = "Введите запрос"

NOTFOUND_MESSAGE = Template('У $res не получилось ничего найти по вашему запросу')

resource_kb = ReplyKeyboardMarkup(resize_keyboard=True)
resource_kb.add(KeyboardButton(text='/help')).add(KeyboardButton(text='/yandex'), KeyboardButton(text='/lexica')).add(KeyboardButton(text='/tenor'), KeyboardButton(text='/cover'))

