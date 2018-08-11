import logging
import traceback

import pymysql
from pymysql import IntegrityError
from sqlalchemy import create_engine, or_
from sqlalchemy import desc
from sqlalchemy.orm import sessionmaker

from backend.model.entity.app import Application


pymysql.install_as_MySQLdb()


class ApplicationRepository:
    def __init__(self, url: str):
        engine = create_engine(url, encoding='utf8')
        self.Session = sessionmaker(bind=engine)


    def get_all_apps(self):
        session = self.Session()
        try:
            apps = session.query(Application).order_by(desc(Application.id)).all()
        except:
            traceback.print_exc()
            raise
        finally:
            session.close()
        return apps


    def get_all_apps_desc(self):
        session = self.Session()
        try:
            apps = session.query(Application).order_by(desc(Application.id)).all()
            result = [dict(app.dict()) for app in apps]
        except:
            traceback.print_exc()
            raise
        finally:
            session.close()
        logging.info(result)
        return result


    def get_app_by_id(self, index: int) -> Application:
        session = self.Session()
        try:
            app = session.query(Application).filter_by(id=index).first()
        except:
            traceback.print_exc()
            raise
        finally:
            session.close()
        return app


    def get_active_apps(self):
        session = self.Session()
        try:
            app = session.query(Application) \
                .filter(Application.status > Application.STATUS_BASE) \
                .filter(Application.status < Application.STATUS_SUCCESS) \
                .all()
        except:
            traceback.print_exc()
            raise
        finally:
            session.close()
        return app


    def get_app_by_bundle(self, bundle) -> Application:
        session = self.Session()
        try:
            user = session.query(Application) \
                .filter(or_(
                    Application.bundle == bundle,
                    Application.bundle_ios == bundle))\
                .first()
        except:
            traceback.print_exc()
            raise
        finally:
            session.close()
        return user


    def update_app(self, app: Application) -> bool:
        session = self.Session()
        try:
            session.merge(app)
            session.commit()
        except:
            session.rollback()
            traceback.print_exc()
        finally:
            session.close()
        return True


    def create_app(self, app: Application) -> bool:
        session = self.Session()
        try:
            session.add(app)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            traceback.print_exc()
            raise e
        finally:
            session.close()
        return True


    def update_app_state(self, app: Application) -> bool:
        session = self.Session()
        try:
            session.merge(app)
            session.commit()
        except:
            session.rollback()
            traceback.print_exc()
        finally:
            session.close()
        return True


    def delete_app(self, app: Application) -> bool:
        session = self.Session()
        try:
            session.delete(app)
            session.commit()
        except:
            session.rollback()
            traceback.print_exc()
        finally:
            session.close()
        return True
