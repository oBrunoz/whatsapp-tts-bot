from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncAttrs

Base = declarative_base(cls=AsyncAttrs)