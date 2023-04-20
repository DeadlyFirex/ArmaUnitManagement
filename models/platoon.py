from uuid import uuid4

from sqlalchemy.orm import relationship

from services.database import Base
from sqlalchemy import Column, Integer, String, Text, PickleType, ForeignKey


class Platoon(Base):
    """
    Model representing a database-platoon. Platoons are used to group squads.
    This data can be fetched and represented.
    """
    __tablename__ = 'platoons'
    # Squad-specific information
    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True, default=str(uuid4()))
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False, default="A new platoon")

    # Identification
    callsign = Column(String(10), nullable=False, unique=True)

    # Organization
    platoon = Column(String(36), ForeignKey("platoon.uuid"), nullable=True, default=None)
    squads = Column(PickleType, nullable=False, default=[])
    headquarters = Column(String(36), ForeignKey("squads.uuid"), nullable=True, default=None)

    # Relationships
    squads_list = relationship("Member")

    def __repr__(self):
        return f"<Squad {self.name}>"
