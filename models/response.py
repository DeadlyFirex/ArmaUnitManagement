from sqlalchemy import DateTime, Column, Integer, String, PickleType

from services.database import Base

from dataclasses import dataclass
from uuid import uuid4
from datetime import datetime


@dataclass
class Response(Base):
    __tablename__ = 'responses'
    id: int = Column(Integer, primary_key=True, nullable=False, unique=True)
    uuid: str = Column(String(36), nullable=False, unique=True, default=str(uuid4()))
    responseId: str = Column(String(71), nullable=False, unique=True)
    createTime: str = Column(DateTime, default=datetime.utcnow(), nullable=False)
    lastSubmittedTime: str = Column(DateTime, default=datetime.utcnow(), nullable=False)
    count: int = Column(Integer, nullable=False)
    answers: dict = Column(PickleType, nullable=False, default={})
