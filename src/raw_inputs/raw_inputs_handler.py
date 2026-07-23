import traceback
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

from src.middlewares import ServiceConteiner
from src.raw_inputs.raw_inputs_scheme import RawInputsScheme
from src.users import UserCreate

router = Router(name="raw_inputs_handler")


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
                first_name=message.from_user.first_name
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
    
@router.message(F.text)
async def create_raw_input(message: Message, services: ServiceConteiner):
    data_scheme = RawInputsScheme(
        telegram_user_id=message.from_user.id,
        message_id=message.message_id,
        content_type=message.content_type,
        raw_text=message.text,
        create_at=message.date,
    )

    if message.voice is not None:
        data_scheme.voice_file_id = message.voice.file_id

    if (raw_input := await services.raw_inputs.create_raw_input(data_scheme)) is None:
        return await message.answer("Error 500")

    if (
        gpt_annotation := await services.gpt_annotation.create_gpt_annatation(
            raw_input.id, raw_input.raw_text
        )
    ) is None:
        return await message.answer("Error 500")
    
    return message.answer(gpt_annotation.transcribed_text)

@router.message(Command('/ideas'))
async def get_ideas(message: Message,services: ServiceConteiner):
    ideas = await services.raw_inputs.get_recent_entries(message.from_user.id)
    