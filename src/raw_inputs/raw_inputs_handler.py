from aiogram import Router, F
from aiogram.types import Message

from src.middlewares import ServiceConteiner
from src.raw_inputs.raw_inputs_scheme import RawInputsScheme

router = Router(name="raw_inputs_handler")

@router.message()
async def create_raw_input(message: Message, services: ServiceConteiner):
    data_scheme = RawInputsScheme(
        telegram_user_id=message.from_user.id,
        message_id=message.message_id,
        content_type=message.content_type,
        raw_text=message.text,
        create_at=message.date
        )
    
    if message.voice is not None: 
        data_scheme.voice_file_id = message.voice.file_id 
    
    response_text = await services.raw_inputs.create_raw_input(data_scheme)
    
    if response_text is not None:
        await message.answer(response_text)
    
