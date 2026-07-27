from sqlalchemy.ext.asyncio import AsyncSession


class NotesRepo:
    def __init__(self,session: AsyncSession):
        self._session = session

    async def get_ideas(self):
        pass