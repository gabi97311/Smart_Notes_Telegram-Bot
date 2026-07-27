import asyncio
import whisper
from pathlib import Path

model = whisper.load_model("small")


async def get_text(local_filename: str) -> str:

    file_path = Path(local_filename).resolve()

    if not file_path.exists():
        return None

    result = await asyncio.to_thread(model.transcribe, str(file_path))
    text = result.get("text", "").strip()
    return text
