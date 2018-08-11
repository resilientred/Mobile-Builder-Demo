from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
table_name = "theme"


class Theme(Base):
    __tablename__ = table_name

    id = Column(Integer, primary_key=True)
    hash = Column(String)
    splash_bg = Column(String)
    accent_bg = Column(String)
    accent_text = Column(String)
    menu_bg = Column(String)
    menu_text = Column(String)
    menu_stroke = Column(String)
    content_bg = Column(String)
    content_text = Column(String)
    content_stroke = Column(String)
    content_icon_bg = Column(String)
    content_icon_stroke = Column(String)
    map_marker_bg = Column(String)
    map_marker_bg_stroke = Column(String)
    map_marker_text = Column(String)
    map_car_bg = Column(String)
    accent_bg_tariff = Column(String)


    def __init__(self, hash='', splash_bg='', accent_bg='', accent_text='', menu_bg='', menu_text='', menu_stroke='',
                 content_bg='', content_text='', content_stroke='', content_icon_bg='', content_icon_stroke='',
                 map_marker_bg='', map_marker_bg_stroke='', map_marker_text='', map_car_bg='', accent_bg_tariff=''):
        self.hash = hash
        self.splash_bg = splash_bg
        self.accent_bg = accent_bg
        self.accent_text = accent_text
        self.menu_bg = menu_bg
        self.menu_text = menu_text
        self.menu_stroke = menu_stroke
        self.content_bg = content_bg
        self.content_text = content_text
        self.content_stroke = content_stroke
        self.content_icon_bg = content_icon_bg
        self.content_icon_stroke = content_icon_stroke
        self.map_marker_bg = map_marker_bg
        self.map_marker_bg_stroke = map_marker_bg_stroke
        self.map_marker_text = map_marker_text
        self.map_car_bg = map_car_bg
        self.accent_bg_tariff = accent_bg_tariff


    def dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
