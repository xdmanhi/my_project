from typing import Optional

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, class_mapper

engine = create_async_engine('sqlite+aiosqlite:///tasks.db')

new_session = async_sessionmaker(engine, expire_on_commit=False)
class Model(DeclarativeBase):
    pass

class TaskORM(Model):
    __tablename__ = 'tasks'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]] = None

    def to_dict(self):
        return {c.key: getattr(self, c.key)
                for c in class_mapper(self.__class__).columns}
    
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)  
        
async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
    
    


