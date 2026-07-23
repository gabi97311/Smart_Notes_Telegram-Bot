from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.exc import SQLAlchemyError
from src.raw_inputs.raw_inputs_scheme import RawInputsScheme
from src.raw_inputs.raw_inputs_model import RawInputsModel

class RawInputsRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def create_raw_input(self, raw_scheme: RawInputsScheme) -> RawInputsModel | None:
        raw_model = RawInputsModel(**raw_scheme.model_dump())
        self.session.add(raw_model)
        try:
            await self.session.commit()
            await self.session.refresh(raw_model)
            return raw_model
        except SQLAlchemyError as e:
            await self.session.rollback()
            print(e)
            return None
    
    async def get_user_by_id(self, user_id:int):
        pass
    
    async def get_message_by_id(self, message_id: int):
        return await self.session.get(RawInputsModel, message_id)
    
    async def get_recent_entries(self):
        pass
    