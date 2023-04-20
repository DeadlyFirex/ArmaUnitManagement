from uuid import uuid4
from services.database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, PickleType, Boolean, ForeignKey


class Attendance(Base):
    """
    Model representing an attendance mark of a member.
    Linked to their owners, mission and user by UUID.

    Members who do have not an entry in the table to the proper missions are simply marked by the APi
    as "did-not-respond".
    Members who do not have confirmed attendance are marked as "not-attending".
    """
    __tablename__ = 'attendances'
    # Attendance-specific information
    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True, default=str(uuid4()))
    attending = Column(Boolean, nullable=False, default=True)
    reason = Column(Text, nullable=True, default=None)
    attended = Column(Boolean, nullable=False, default=False)

    # User-based data
    user_uuid = Column(String(36), ForeignKey("members.uuid"), nullable=False)

    # Event-based data
    mission_uuid = Column(String(36), ForeignKey("missions.uuid"), nullable=False)

    # Tracking-based data
    created = Column(DateTime, nullable=False, default=datetime.utcnow())
    last_changed = Column(DateTime, nullable=True, default=None)
    log_changed = Column(PickleType, nullable=True, default={})

    def add_change(self, status: bool):
        self.log_changed.update({datetime.utcnow(): status})
        self.last_changed = datetime.utcnow()

    def __repr__(self):
        return f"<Attendance {self.user_uuid} ({self.status})>"
