import traceback

import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.model.entity.theme import Theme

pymysql.install_as_MySQLdb()


class ThemeRepository:

    def __init__(self, url: str):
        engine = create_engine(url)
        self.Session = sessionmaker(bind=engine)


    def get_theme_by_id(self, index: int) -> Theme:
        session = self.Session()
        try:
            theme = session.query(Theme).filter_by(id=index).first()
        except:
            traceback.print_exc()
            raise
        finally:
            session.close()
        return theme


    def get_theme_by_hash(self, theme_hash) -> Theme:
        print(theme_hash)
        session = self.Session()
        theme: Theme
        try:
            theme = session.query(Theme).filter_by(hash=theme_hash).first()
        except:
            traceback.print_exc()
        finally:
            session.close()
        return theme


    def create_theme(self, theme: Theme) -> bool:
        session = self.Session()
        try:
            session.add(theme)
            session.commit()
        except:
            traceback.print_exc()
            session.rollback()
            raise
        finally:
            session.close()
        return True


    def update_theme(self, theme: Theme) -> bool:
        session = self.Session()
        temp_theme = self.get_theme_by_hash(theme.hash)
        try:
            if not temp_theme:
                session.merge(theme)
                session.commit()
        except:
            session.rollback()
            traceback.print_exc()
        finally:
            session.close()
        return True
