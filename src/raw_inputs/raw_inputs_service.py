from aiogram import Bot

from src.utils import get_text, FileManager

from src.raw_inputs.raw_inputs_scheme import RawInputsScheme
from src.raw_inputs.raw_inputs_repo import RawInputsRepo
from src.raw_inputs.raw_inputs_model import RawInputsModel


class RawInputsService:
    def __init__(self, raw_input_repo: RawInputsRepo):
        self.raw_input_repo = raw_input_repo

    async def get_user_by_id(self, user_id: int):

        pass

    async def create_raw_input(
        self, bot: Bot, raw_scheme: RawInputsScheme
    ) -> RawInputsModel | None:

        if await self.raw_input_repo.get_message_by_id(raw_scheme.message_id):
            return

        if raw_scheme.voice_file_id is not None:
            temp_file_path = None
            try:
                temp_file_path = await FileManager.generate_voice_file(
                    bot, raw_scheme.voice_file_id
                )
                text = await get_text(temp_file_path)
                raw_scheme.raw_text = text
            finally:
                FileManager.delete_file(temp_file_path)

        if (
            raw_input := await self.raw_input_repo.create_raw_input(raw_scheme)
        ) is None:
            return

        return raw_input

    async def get_recent_entries(self, user_id: int):

        entries = self.raw_input_repo
