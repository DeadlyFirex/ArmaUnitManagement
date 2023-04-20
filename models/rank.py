from uuid import uuid4

from sqlalchemy.orm import relationship

from services.database import Base
from sqlalchemy import Boolean, Column, Integer, String, Text


class Rank(Base):
    """
    Model representing a database-rank of a member.
    Comparisons are possible, to check which person is superior.

    This does not grant or limit access to endpoints. This is basically decor!
    And example can be found below;
    """
    __tablename__ = 'ranks'
    # Rank-specific information
    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True, default=str(uuid4()))
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False, default="A new rank")
    abbreviation = Column(String(10), nullable=False, unique=True)

    # Hierarchy-based date
    code = Column(String(10), nullable=False, unique=True)
    level = Column(Integer, nullable=False, unique=True)
    leadership = Column(Boolean, nullable=False, default=False)

    # Relationships
    member_list = relationship("Member")
    defaults_list = relationship("Position")

    def __lt__(self, other):
        if not isinstance(other, Rank):
            raise TypeError("Excepted rank")
        return self.level < other.level

    def __gt__(self, other):
        if not isinstance(other, Rank):
            raise TypeError("Excepted rank")
        return self.level > other.level

    def __eq__(self, other):
        if not isinstance(other, Rank):
            raise TypeError("Excepted rank")
        return self.level == other.level

    def __repr__(self):
        return f"<Rank {self.abbreviation} - {self.name} ({self.code})>"