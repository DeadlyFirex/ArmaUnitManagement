from uuid import uuid4

from sqlalchemy.orm import relationship

from services.database import Base
from sqlalchemy import Column, Integer, String, Text, PickleType, ForeignKey


class Squad(Base):
    """
    Model representing a database-squad. Squads are used to group player into squads.
    This data can be fetched and represented, but squads configure the squads-roles.
    """
    __tablename__ = 'squads'
    # Squad-specific information
    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True, default=str(uuid4()))
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False, default="A new squad")

    # Organization
    platoon = Column(String(36), ForeignKey("platoon.uuid"), nullable=True, default=None)
    callsign = Column(String(10), nullable=False, unique=True)
    members = Column(PickleType, nullable=False, default=[])
    positions = Column(PickleType, nullable=False, default=[])

    # Relationships
    member_list = relationship("Member")
    headquarter_list = relationship("Platoon")

    def __repr__(self):
        return f"<Squad {self.name}>"
