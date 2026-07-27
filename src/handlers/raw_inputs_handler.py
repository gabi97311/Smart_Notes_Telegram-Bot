import traceback
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command

from src.middlewares import ServiceConteiner
from src.raw_inputs.raw_inputs_scheme import CreateRawInput

router = Router(name="raw_inputs_handler")

@router.message(F.text)
async def create_raw_input(message: Message, bot: Bot , services: ServiceConteiner):

    raw_scheme = CreateRawInput(
        telegram_user_id=message.from_user.id,
        message_id=message.message_id,
        content_type=message.content_type,
        raw_text=message.text,
        create_at=message.date,
    )
    await _process_raw_input(message, services, raw_scheme, bot)


@router.message(F.voice)
async def create_raw_input_voice(message: Message, bot: Bot, services: ServiceConteiner):

    raw_scheme = CreateRawInput(
        telegram_user_id=message.from_user.id,
        message_id=message.message_id,
        content_type=message.content_type,
        voice_file_id=message.voice.file_id,
        create_at=message.date,
    )
    await _process_raw_input(message, services, raw_scheme, bot)


async def _process_raw_input(
    message: Message, services: ServiceConteiner, raw_scheme: CreateRawInput, bot: Bot
):
    if (raw_input := await services.raw_inputs.create_raw_input(bot, raw_scheme)) is None:
        return await message.answer("Error 500")

    if (
        gpt_annotation := await services.gpt_annotation.create_gpt_annatation(
            raw_input.id, raw_input.raw_text
        )
    ) is None:
        return await message.answer("Error 500")

    return message.answer(gpt_annotation.transcribed_text)

