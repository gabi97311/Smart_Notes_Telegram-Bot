from src.core import setting
from google import genai
from google.genai import types
from datetime import datetime
import json

from src.gpt_annotations.gpt_annotataion_scheme import GptAnnatataionSchemeCreate
from src.gpt_annotations.gpt_annotataion_repo import GptAnnotataionRepo
from src.gpt_annotations.gpt_annotations_model import GptAnnotationsModel

class GptAnnotataionService:
    def __init__(self, gpt_annatation_repo: GptAnnotataionRepo):
        self.repo = gpt_annatation_repo

    async def create_gpt_annatation(self, raw_input_id: int, raw_input: str) -> GptAnnotationsModel | None:
        if not (gemini_data := self._gemini_request(raw_input)):
            return None
        
        gpt_scheme  = GptAnnatataionSchemeCreate(
            raw_input_id=raw_input_id,
            **gemini_data,
            target_date=datetime.today().isoformat(),
        )
        
        gpt_annatation = await self.repo.create_gpt_annatation(gpt_scheme)
        
        if gpt_annatation is None:
            return None
        
        return gpt_annatation
    
    
    def _gemini_request(self, raw_input: str):
        client = genai.Client(api_key=setting.GEMINI_API_KEY)
        system_instruction = f"""
            Ты — интеллектуальный помощник. Твоя задача — переформулировать текст для сохранения в блокнот и извлечь метаданные для кластеризации.

            Верни ответ СТРОГО в виде чистого JSON, без markdown-разметки (не используй ```json) и без какого-либо дополнительного текста. 

            Ключи JSON:
            - "transcribed_text" (строка): красиво переформулированный и грамматически верный текст пользователя.
            - "extracted_intent" (строка): выбери строго одно слово из списка: [задача, идея, встреча, покупка, заметка].
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
        try:
            gemini_data = json.loads(response.text)
            return gemini_data
        except json.JSONDecodeError as e:
            print(f"Gemini вернул сломанный JSON: {e}\nТекст: {response.text}")
        return None
