from src.core import setting
from google import genai
from google.genai import types
from datetime import datetime

from src.gpt_annotations.gpt_annatataion_scheme import GptAnnatataionSchemeCreate
from src.gpt_annotations.gpt_annotataion_repo import GptAnnotataionRepo


class GptAnnatataionService:
    def __init__(self, gpt_annatation_repo: GptAnnotataionRepo):
        self.repo = gpt_annatation_repo

    async def create_gpt_annatation(self, raw_input_id: int, raw_input: str):
        if not (response := self._gemini_request(raw_input)):
            return
        gpt_annatation = GptAnnatataionSchemeCreate(
            raw_input_id=raw_input_id,
            **response,
            target_date=datetime.today().isoformat(),
        )
        await self.repo.create_gpt_annatation()

    def _gemini_request(self, raw_input: str):
        client = genai.Client(api_key=setting.GEMINI_API_KEY)
        system_instruction = f"""
            Ты — интеллектуальный помощник. Твоя задача — переформулировать текст для сохранения в блокнот и извлечь метаданные для кластеризации.

            Верни ответ СТРОГО в формате JSON с ключами:
            - "transcribed_text" (строка): красиво переформулированный и грамматически верный текст пользователя.
            - "extracted_intent" (строка): одно слово-категория для кластеризации (например: задача, идея, встреча, покупка, дневник).
            - "extracted_keywords" (массив строк): 3-5 ключевых слов в именительном падеже.
            """

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=raw_input,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                temperature=0.2,
            ),
        )
        return response
