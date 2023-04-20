from uuid import uuid4

from sqlalchemy.orm import relationship

from services.database import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean


class Position(Base):
    """
    Model representing a position with a Squad.
    This data can be fetched and represented.
    """
    __tablename__ = 'platoons'
    # Squad-specific information
    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True, default=str(uuid4()))
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False, default="A new position.")

    # Organization
    leader = Column(Boolean, nullable=False, default=False)
    index = Column(Integer, nullable=False, default=0)
    squad = Column(String(36), ForeignKey("squads.uuid"), nullable=False, default=[])
    default_rank = Column(String(36), ForeignKey("ranks.uuid"), nullable=False, default=None)
    certification = Column(String(36), ForeignKey("certifications.uuid"), nullable=True, default=None)

    def __repr__(self):
        return f"<Position {self.name}>"
