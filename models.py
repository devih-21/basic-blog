from typing import Optional
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base
import uuid
from sqlalchemy.sql import func
# from sqlalchemy.dialects.sqlite import UUID

    

class Blog(Base):
    __tablename__ = "blogs"
    id = Column(String, primary_key=True, unique=True)
    title = Column(String)
    body = Column(String)
    published = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), default=func.now())