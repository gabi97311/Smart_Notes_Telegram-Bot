import os
import tempfile
import uuid
from pathlib import Path
from typing import Optional
from aiogram import Bot

class FileManager:

    @staticmethod
    async def generate_voice_file(bot: Bot, file_id: str) -> str:

        temp_file_path = os.path.join(
            tempfile.gettempdir(), f"voice_{uuid.uuid4().hex}.ogg"
        )
        file = await bot.get_file(file_id)
        await bot.download_file(file.file_path, destination=temp_file_path)
        return temp_file_path

    @staticmethod
    def delete_file(file_path: Optional[str]) -> bool:

        if not file_path:
            return False

        path = Path(file_path)
        try:
            if path.exists():
                path.unlink()
                return True
        except Exception as e:

            print(f"[FileManager] Не удалось удалить файл {file_path}: {e}")

        return False
