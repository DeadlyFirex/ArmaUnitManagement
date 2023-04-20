from sqlalchemy import Boolean, DateTime, Column, Integer, String, PickleType, Text, ForeignKey
from sqlalchemy.orm import relationship

from services.utilities import Utilities
from services.database import Base

from dataclasses import dataclass
from uuid import uuid4
from datetime import datetime
from inspect import currentframe


@dataclass
class Member(Base):
    """
    Member model representing a member of the unit.
    This can be an admin, allowing to make changes to the microservice.
    """
    # TODO: Add methods to make database changes easier.
    __tablename__ = 'members'
    # Database specific information
    id: int = Column(Integer, primary_key=True, nullable=False, unique=True)
    uuid: str = Column(String(36), nullable=False, unique=True, default=str(uuid4()))

    # Member specific information
    first_name: str = Column(String(50), nullable=False, unique=False)
    nickname: str = Column(String(50), nullable=True, unique=True)
    last_name: str = Column(String(50), nullable=False, unique=False)
    discord: str = Column(String(18), nullable=False, unique=True)
    email: str = Column(String(50), nullable=False, unique=True)
    created_at: datetime = Column(DateTime, nullable=False, default=datetime.utcnow())
    country_iso: str = Column(String(2), nullable=False)
    country: str = Column(String(20), nullable=False)

    # Member information
    operator_level: int = Column(Integer, nullable=True, default=None)
    qualifications: list = Column(PickleType, nullable=False, default=[])
    title: str = Column(String(50), nullable=True, default=None)
    rank: str = Column(String(36), ForeignKey("ranks.uuid"), nullable=False)
    staff_shops: list = Column(PickleType, nullable=False, default=[])
    decorations: list = Column(PickleType, nullable=False, default=[])

    # Member in relation to unit information
    platoon: int = Column(String(36), ForeignKey("platoon.uuid"), nullable=False, default=6)
    team: str = Column(String(36), ForeignKey("squads.uuid"), nullable=True, default=None)
    team_index: int = Column(Integer, nullable=True, default=None)
    recruiter: bool = Column(Boolean, nullable=False, default=False)
    leadership: bool = Column(Boolean, nullable=False, default=False)

    # Moderation and conduct
    strikes: list = Column(PickleType, nullable=False, default=[])
    warnings: list = Column(PickleType, nullable=False, default=[])
    notes: str = Column(Text(5000), nullable=True, default=None)

    # Clearance/security/authentication
    flags: list = Column(PickleType, nullable=False, default=[])
    admin: bool = Column(Boolean, nullable=False, default=False)
    password: str = Column(String(200), nullable=False)
    secret: str = Column(String(50), nullable=True, unique=True, default=Utilities.generate_secret())
    token: str = Column(String(500), nullable=True, unique=True, default=None)
    tags: list = Column(PickleType, nullable=False, default=[])

    # Tracking
    active: bool = Column(Boolean, nullable=True, default=None)
    last_action_at: datetime = Column(DateTime, nullable=True, default=None)
    last_action_ip: str = Column(String(50), nullable=True, default=None)
    last_action: str = Column(String(50), nullable=True, default=None)
    last_login_at: datetime = Column(DateTime, nullable=True, default=None)
    last_login_ip: str = Column(String(50), nullable=True, default=None)
    login_count: int = Column(Integer, nullable=True, default=0)

    # Relationships
    attendance_list = relationship("Attendance")
    campaign_organizer_list = relationship("Campaign")
    mission_organizer_list = relationship("Mission")

    def get_fullname(self):
        return f"{self.first_name[0]}. {self._lastname}"

    def perform_tracking(self, source: str = None, address: str = "UNKNOWN", active: bool = True, login: bool = False):
        from services.database import db_session
        now = datetime.utcnow()

        if source is None:
            source = str(currentframe().f_back.f_code.co_name)

        if login:
            self.active = active
            self.login_count += 1
            self.last_login_at = now
            self.last_login_ip = address
        else:
            self.active = active
            self.last_action = source
            self.last_action_at = now
            self.last_action_ip = address

        db_session.commit()

    def __repr__(self):
        return f"<User {self.get_fullname()}>"
