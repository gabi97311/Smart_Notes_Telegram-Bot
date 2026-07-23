from src.raw_inputs.raw_inputs_scheme import RawInputsScheme
from src.raw_inputs.raw_inputs_repo import RawInputsRepo
from src.raw_inputs.raw_inputs_model import RawInputsModel

class RawInputsService:
    def __init__(self, raw_input_repo: RawInputsRepo) -> RawInputsModel | None:
        self.raw_input_repo = raw_input_repo
        
    async def get_user_by_id(self, user_id: int):

        pass
        
    async def create_raw_input(self, raw_scheme:RawInputsScheme):
        
        if await self.raw_input_repo.get_message_by_id(raw_scheme.message_id):
            return 
        
        if raw_scheme.voice_file_id is not None:
            pass
        
        if (raw_input := await self.raw_input_repo.create_raw_input(raw_scheme)) is None:
            return None
        
        return raw_input
        
    async def get_recent_entries(self, user_id:int):
        
    
        entries = self.raw_input_repo