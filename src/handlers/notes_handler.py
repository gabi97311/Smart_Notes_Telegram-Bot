from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from src.middlewares import ServiceConteiner

router = Router(name="notes_handler")


@router.message(Command("ideas"))
async def get_ideas(message: Message, services: ServiceConteiner):
    telegram_id = message.from_user.id
