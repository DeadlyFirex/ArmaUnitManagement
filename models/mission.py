from uuid import uuid4
from services.database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, PickleType, Boolean, ForeignKey


class Mission(Base):
    """
    Model representing a mission.

    This is what the attendance marker uses, and the campaign status.
    They are linked to the campaign, example below;
    """
    __tablename__ = 'mission'
    # Mission-specific information
    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True, default=str(uuid4()))
    title = Column(String(100), nullable=False, unique=True, default="New Mission")
    description = Column(Text, nullable=False, default="No description provided.")
    from_date = Column(DateTime, nullable=False)
    to_date = Column(DateTime, nullable=False)

    # Linking data
    campaign_uuid = Column(String(36), ForeignKey("campaigns.uuid"), nullable=False)
    organizer_uuid = Column(String(36), ForeignKey("members.uuid"), nullable=False)

    # Event-based data
    briefing = Column(Text, nullable=False, default="No briefing provided.")
    attended = Column(PickleType, nullable=False, default=[])
    completed = Column(Boolean, nullable=False, default=False)

    # Ingame-based data
    ingame_time = Column(DateTime, nullable=True, default=None)
    map = Column(String(100), nullable=True, default=None)

    def __repr__(self):
        return f"<Mission {self.title}>"
