from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from services.config import Config

from bcrypt import hashpw, gensalt

config = Config().get_config()
engine = create_engine(config.database.type + config.database.absolute_path, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    from models import member
    member = member.Member(first_name="Deadly", last_name="Alden", username="224744826581549057", admin=True,
                           email="admin@administrator.com", password=hashpw(b'admin', gensalt()).decode("UTF-8"), country="NL")
    Base.metadata.create_all(bind=engine)
    db_session.add_all([member])
    db_session.commit()
