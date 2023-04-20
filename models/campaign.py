from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import relationship

from services.database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, PickleType, Boolean, ForeignKey


class Campaign(Base):
    """
    Model representing an campaign.
    The campaign serves as the category for missions, example below;
    """
    __tablename__ = 'campaigns'
    # Mission-specific information
    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True, default=str(uuid4()))
    title = Column(String(100), nullable=False, unique=True, default="New Campaign")
    description = Column(Text, nullable=False, default="No description provided")

    # Linking data
    organizer_uuid = Column(String(36), ForeignKey("members.uuid"), nullable=False)

    # Event-based data
    date_started = Column(DateTime, nullable=False, default=datetime.utcnow())
    briefing = Column(Text, nullable=False, default="No briefing provided.")
    mission_uuid = Column(PickleType, nullable=False, default=[])
    mission_count = Column(Integer, nullable=False, default=0)
    completed = Column(Boolean, nullable=False, default=False)

    # Relationships
    mission_list = relationship("Mission")

    def __repr__(self):
        return f"<Campaign {self.title}>"
