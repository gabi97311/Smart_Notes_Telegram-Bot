from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.gpt_annotations.gpt_annotations_model import GptAnnotationsModel
from src.gpt_annotations.gpt_annotataion_scheme import GptAnnatataionSchemeCreate

class GptAnnotataionRepo:
    def __init__(self, session: AsyncSession):
        self._session = session
        
    async def create_gpt_annatation(self, gpt_scheme: GptAnnatataionSchemeCreate) -> GptAnnotationsModel | None: 
        gpt_model = GptAnnotationsModel(**gpt_scheme.model_dump())
        self._session.add(gpt_model)
        try: 
            await self._session.commit()
            await self._session.refresh(gpt_model)
            return gpt_model
        except SQLAlchemyError as e:
            await self._session.rollback()
            print(e)
            return None