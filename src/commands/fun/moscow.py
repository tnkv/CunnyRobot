from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from random import triangular

router = Router()

mkad_latitude_range = (55.62, 55.86)
mkad_longitude_range = (37.40, 37.79)


@router.message(Command(commands=['moscow', 'москва']))
async def command_moscow(message: Message) -> None:
    latitude, longitude = generate_location()
    await message.reply(text=f'Найдено потрясающее место где можно встретиться!\n'
                             f'Координаты: <code>{latitude} {longitude}\n</code>'
                             f'<a href=\'https://yandex.ru/maps/?ll={longitude},{latitude}&z=16&l=map\'>Яндекс карты</a>',
                        disable_web_page_preview=True)
    await message.answer_location(latitude=latitude, longitude=longitude)


def generate_location() -> tuple[float, float]:
    latitude = round(triangular(mkad_latitude_range[0], mkad_latitude_range[1]), 6)
    longitude = round(triangular(mkad_longitude_range[0], mkad_longitude_range[1]), 6)

    return latitude, longitude
