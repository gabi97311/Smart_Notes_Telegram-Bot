import traceback
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from src.middlewares import ServiceConteiner
from src.users import UserCreate

router = Router(name="start_handler")


@router.message(CommandStart())
async def bot_start(message: Message, services: ServiceConteiner):

    try:
        user = await services.users.get_user_by_telegram_id(message.from_user.id)

        if user:
            await message.answer(
                f"С возвращением, {message.from_user.first_name}! 👋\n\n"
                "Я готов продолжать работу. Отправляй свои идеи и заметки!"
            )
            return

        user_scheme = UserCreate(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
        )

        await services.users.create_user(user_scheme)
        await message.answer(
            f"👋 Привет, {message.from_user.username}!\n\n"
            "Я помогу сохранять твои идеи, заметки и планы.\n"
            "Просто отправь мне текст или голосовое сообщение, "
            "а я структурирую его и сохраню."
        )
        return

    except Exception as e:
        print("=== ПОЛНЫЙ ЛОГ ОШИБКИ ===")
        traceback.print_exc()
        print("=========================")
        await message.answer(
            "Ой, что-то пошло не так при регистрации 😔\n"
            "Наши сервера немного устали. Пожалуйста, попробуй команду /start через пару минут!"
        )
        return
