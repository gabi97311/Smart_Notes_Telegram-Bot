from src.raw_inputs.raw_inputs_scheme import RawInputsScheme
from src.raw_inputs.raw_inputs_repo import RawInputsRepo

class RawInputsService:
    def __init__(self, raw_input_repo: RawInputsRepo):
        self.raw_input_repo = raw_input_repo
        
    async def create_raw_input(self, data:RawInputsScheme):
        
        if await self.raw_input_repo.get_message_by_id(data.message_id):
            return 
        
        if data.voice_file_id is not None:
            pass
        
        await self.raw_input_repo.create_raw_input(data)
        