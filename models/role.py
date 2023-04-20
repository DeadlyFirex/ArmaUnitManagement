from uuid import uuid4
from services.database import Base
from sqlalchemy import Boolean, Column, Integer, String, Text


class Role(Base):
    """
    Model representing a database-role and thus clearance of a member.
    Comparisons are possible, to check which role is superior.

    Roles grant or deny access to endpoints or actions.
    And example can be found below;
    """
    __tablename__ = 'roles'
    # Role specific information
    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    uuid = Column(String, nullable=False, unique=True, default=str(uuid4()))
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=False, default="A new role")

    # Clearance-specific data
    level = Column(Integer, nullable=False, unique=True)
    mod = Column(Boolean, nullable=False, default=False)
    admin = Column(Boolean, nullable=False, default=False)

    def __lt__(self, other):
        if not isinstance(other, Role):
            raise TypeError("Excepted role")
        return self.level < other.level

    def __gt__(self, other):
        if not isinstance(other, Role):
            raise TypeError("Excepted role")
        return self.level > other.level

    def __eq__(self, other):
        if not isinstance(other, Role):
            raise TypeError("Excepted role")
        return self.level == other.level

    def __repr__(self):
        return f"<Rank {self.name} - {self.level}>"