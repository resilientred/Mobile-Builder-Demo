from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy import Boolean
from sqlalchemy import DateTime
import datetime


Base = declarative_base()
table_name = "build"


class Build(Base):
    __tablename__ = table_name

    STATUS_WAITING = 0
    STATUS_EXECUTING = 1
    STATUS_SUCCESS = 2
    STATUS_ERROR = 3

    id = Column(Integer, primary_key=True)
    app_id = Column(Integer)
    theme_id = Column(Integer)
    is_build = Column(Boolean)
    is_create = Column(Boolean)
    is_clear = Column(Boolean)
    default_bundle = Column(Boolean)
    version_code = Column(Integer)
    version_name = Column(String)
    email = Column(String)
    build_type = Column(String)
    time_created = Column(DateTime, default=datetime.datetime.utcnow)
    priority = Column(Integer)
    status = Column(Integer)

    def __init__(self,
                 app_id='', theme_id=theme_id, is_build='', is_create='', is_clear='', default_bundle='',
                 version_code='', version_name='', email='', build_type='', time_created='', priority='', status=''):
        self.app_id = app_id
        self.theme_id = theme_id
        self.is_build = is_build
        self.is_create = is_create
        self.is_clear = is_clear
        self.default_bundle = default_bundle
        self.version_code = version_code
        self.version_name = version_name
        self.email = email
        self.build_type = build_type
        self.time_created = time_created
        self.priority = priority
        self.status = status


    def dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
