
class Application:

    STATUS_BASE = 0
    STATUS_CREATED = 1
    STATUS_WAITING = 2
    STATUS_EXECUTING = 3
    STATUS_SUCCESS = 4
    STATUS_ERROR = 5

    def __init__(self,
                 id=0, app_name='', app_id='', app_sku='', bundle='', api_key='', push_key='', metrica_key='', theme='',
                 tenant_id='', client_url='', country='', google_map='', autocomplete='', geo_url="", reverse_radius='',
                 use_photo='', photo_type='', bundle_ios='', google_map_ios='',
                 use_calls='', use_calls_office='', use_calls_driver='',
                 use_flat='', use_porch='', use_street='', use_comment='',
                 use_pre_orders='', use_wishes='', use_detail='',
                 use_one_address='', use_search='',
                 lang='',
                 use_calendars='', default_calendar='',
                 use_cars='', use_country='', is_demo='', use_referral='', use_review_block='', is_full_splash='',
                 max_one_address='', with_edit_order='', shown_client_id='', use_review_detail='',
                 use_review_for_rejected='', use_public_transport='', web_application_url='', web_application_title='',
                 use_web_application='', use_profile_data='', default_language='',

                 use_google='', use_google_hybrid='', use_yandex_map='', use_osm_map='', use_gis_map='', default_map='',
                 with_show_cars='', car_radius='', use_multi_callcost='',is_let_reject_after_assigned='',
                 use_courier_form='',

                 use_payment_card='', use_payment_corp='', use_payment_cash='', use_payment_bonus='',
                 show_company_balance='', use_payment_personal=''):
        self.tenant_id = tenant_id
        self.theme = theme
        self.metrica_key = metrica_key
        self.google_map = google_map
        self.google_map_ios = google_map_ios
        self.push_key = push_key
        self.api_key = api_key
        self.bundle = bundle
        self.bundle_ios = bundle_ios
        self.app_id = app_id
        self.app_name = app_name
        self.app_sku = app_sku
        self.client_url = client_url
        self.geo_url = geo_url
        self.autocomplete = autocomplete
        self.reverse_radius = reverse_radius
        self.country = country
        self.id = id

        self.use_photo = use_photo
        self.photo_type = photo_type

        self.use_calls = use_calls
        self.use_calls_office = use_calls_office
        self.use_calls_driver = use_calls_driver

        self.with_show_cars = with_show_cars
        self.car_radius = car_radius

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

        self.use_cars = use_cars
        self.is_demo = is_demo
        self.is_full_splash = is_full_splash
        self.use_referral = use_referral
        self.use_country = use_country
        self.use_review_block = use_review_block
        self.max_one_address = max_one_address
        self.with_edit_order = with_edit_order
        self.shown_client_id = shown_client_id
        self.use_review_detail = use_review_detail
        self.use_review_for_rejected = use_review_for_rejected
        self.use_profile_data = use_profile_data
        self.default_language = default_language
        self.use_multi_callcost = use_multi_callcost
        self.is_let_reject_after_assigned = is_let_reject_after_assigned
        self.use_courier_form = use_courier_form

        self.use_google = use_google
        self.use_google_hybrid = use_google_hybrid
        self.use_yandex_map = use_yandex_map
        self.use_osm_map = use_osm_map
        self.use_gis_map = use_gis_map
        self.default_map = default_map

        self.use_public_transport = use_public_transport
        self.web_application_url = web_application_url
        self.web_application_title = web_application_title
        self.use_web_application = use_web_application

        self.use_payment_card = use_payment_card
        self.use_payment_corp = use_payment_corp
        self.use_payment_cash = use_payment_cash
        self.use_payment_bonus = use_payment_bonus
        self.show_company_balance = show_company_balance
        self.use_payment_personal = use_payment_personal
        self.status = 0
