from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy import Boolean
from sqlalchemy import Float


Base = declarative_base()
table_name = "app"


class Application(Base):
    __tablename__ = table_name

    STATUS_BASE = 0
    STATUS_CREATED = 1
    STATUS_WAITING = 2
    STATUS_EXECUTING = 3
    STATUS_SUCCESS = 4
    STATUS_ERROR = 5

    id = Column(Integer, primary_key=True)
    app_name = Column(String)
    app_id = Column(Integer, unique=True)
    app_sku = Column(String, unique=True)
    bundle = Column(String)
    bundle_ios = Column(String)
    api_key = Column(String)
    push_key = Column(String)
    google_map = Column(String)
    google_map_ios = Column(String)
    metrica_key = Column(String)
    tenant_id = Column(Integer)
    autocomplete = Column(Integer)
    reverse_radius = Column(Float)
    theme = Column(Integer)
    client_url = Column(String)
    geo_url = Column(String)
    country = Column(String)
    default_language = Column(String)
    status = Column(Integer, nullable=False)

    use_photo = Column(Boolean)
    photo_type = Column(String)

    use_calls = Column(Boolean)
    use_calls_office = Column(Boolean)
    use_calls_driver = Column(Boolean)

    use_flat = Column(Boolean)
    use_porch = Column(Boolean)
    use_street = Column(Boolean)
    use_comment = Column(Boolean)

    use_pre_orders = Column(Boolean)
    use_wishes = Column(Boolean)
    use_detail = Column(Boolean)

    use_one_address = Column(Boolean)
    use_search = Column(Boolean)

    lang = Column(String)

    use_calendars = Column(Boolean)
    default_calendar = Column(String)

    use_cars = Column(Boolean)
    use_country = Column(Boolean)
    use_referral = Column(Boolean)
    is_demo = Column(Boolean)
    is_full_splash = Column(Boolean)
    use_review_block = Column(Boolean)
    max_one_address = Column(Boolean)
    with_edit_order = Column(Boolean)
    shown_client_id = Column(Boolean)
    use_review_detail = Column(Boolean)
    use_review_for_rejected = Column(Boolean)
    use_profile_data = Column(Boolean)
    use_multi_callcost = Column(Boolean)
    is_let_reject_after_assigned = Column(Boolean)
    use_courier_form = Column(Boolean)

    with_show_cars = Column(Boolean)
    car_radius = Column(Integer)

    use_public_transport = Column(Boolean)
    web_application_url = Column(String)
    web_application_title = Column(String)
    use_web_application = Column(Boolean)

    use_google = Column(Boolean)
    use_google_hybrid = Column(Boolean)
    use_yandex_map = Column(Boolean)
    use_osm_map = Column(Boolean)
    use_gis_map = Column(Boolean)
    default_map = Column(String)

    use_payment_card = Column(Boolean)
    use_payment_corp = Column(Boolean)
    use_payment_cash = Column(Boolean)
    use_payment_bonus = Column(Boolean)
    use_payment_personal = Column(Boolean)
    show_company_balance = Column(Boolean)


    def __init__(self,
                 app_name='', app_id='', app_sku='', bundle='', api_key='', push_key='', metrica_key='', theme='',
                 tenant_id='', autocomplete='', client_url='', geo_url='', country='', google_map='', reverse_radius='',
                 use_photo='', photo_type='', bundle_ios='', google_map_ios='',
                 use_calls='', use_calls_office='', use_calls_driver='',
                 use_flat='', use_porch='', use_street='', use_comment='',
                 use_pre_orders='', use_wishes='', use_detail='',
                 use_one_address='', use_search='', default_language='',
                 lang='',use_courier_form='',
                 use_calendars='', default_calendar='',
                 use_cars='', use_country='', is_demo='', use_referral='', use_review_block='', is_full_splash='',
                 max_one_address='', with_edit_order='', shown_client_id='', use_review_detail='',
                 use_review_for_rejected='', use_public_transport='', web_application_url='', web_application_title='',
                 use_web_application='', use_profile_data='', use_multi_callcost='', is_let_reject_after_assigned='',

                 use_google='', use_google_hybrid='', use_yandex_map='', use_osm_map='', use_gis_map='', default_map='',
                 with_show_cars='', car_radius='',

                 use_payment_card='', use_payment_corp='', use_payment_cash='', use_payment_bonus='',
                 use_payment_personal='', show_company_balance=''):
        self.tenant_id = tenant_id
        self.theme = theme
        self.metrica_key = metrica_key
        self.google_map = google_map
        self.push_key = push_key
        self.api_key = api_key
        self.bundle = bundle
        self.bundle_ios = bundle_ios
        self.app_id = app_id
        self.app_name = app_name
        self.app_sku = app_sku
        self.client_url = client_url
        self.geo_url = geo_url
        self.country = country
        self.status = Application.STATUS_BASE
        self.autocomplete = autocomplete
        self.reverse_radius = reverse_radius
        self.google_map_ios = google_map_ios
        self.use_profile_data = use_profile_data
        self.default_language = default_language

        self.use_photo = use_photo
        self.photo_type = photo_type

        self.use_calls = use_calls
        self.use_calls_office = use_calls_office
        self.use_calls_driver = use_calls_driver

        self.use_flat = use_flat
        self.use_porch = use_porch
        self.use_street = use_street
        self.use_comment = use_comment

        self.use_pre_orders = use_pre_orders
        self.use_wishes = use_wishes
        self.use_detail = use_detail

        self.use_one_address = use_one_address
        self.use_search = use_search

        self.lang = lang

        self.use_calendars = use_calendars
        self.default_calendar = default_calendar

        self.with_show_cars = with_show_cars
        self.car_radius = car_radius

        self.is_full_splash = is_full_splash
        self.use_cars = use_cars
        self.is_demo = is_demo
        self.use_referral = use_referral
        self.use_country = use_country
        self.use_review_block = use_review_block
        self.max_one_address = max_one_address
        self.with_edit_order = with_edit_order
        self.shown_client_id = shown_client_id
        self.use_review_detail = use_review_detail
        self.use_review_for_rejected = use_review_for_rejected

        self.use_public_transport = use_public_transport
        self.web_application_url = web_application_url
        self.web_application_title = web_application_title
        self.use_web_application = use_web_application
        self.use_multi_callcost = use_multi_callcost
        self.is_let_reject_after_assigned = is_let_reject_after_assigned
        self.use_courier_form = use_courier_form

        self.use_google = use_google
        self.use_google_hybrid = use_google_hybrid
        self.use_yandex_map = use_yandex_map
        self.use_osm_map = use_osm_map
        self.use_gis_map = use_gis_map
        self.default_map = default_map

        self.use_payment_card = use_payment_card
        self.use_payment_corp = use_payment_corp
        self.use_payment_cash = use_payment_cash
        self.use_payment_bonus = use_payment_bonus
        self.use_payment_personal = use_payment_personal
        self.show_company_balance = show_company_balance


    def __str__(self):
        return self.lang


    def __iter__(self):
        yield self


    def set_id(self, app_id):
        self.id = app_id


    def get_simple_dist(self):
        return {"id": self.id, "app_name": self.app_name, "bundle": self.bundle}


    def get_status_dist(self):
        return {"id": self.id, "app_name": self.app_name, "status": self.status}


    def dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
