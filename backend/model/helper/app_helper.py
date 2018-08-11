import logging

from backend.model.entity.app import Application
from std.error import data_error
from std.error.data_error import DataError
from std.std import obj_to_bool, validate_field

FIELD_ID = "id"
VALIDATE_FIELDS = ['app_name', 'app_id', 'bundle', 'api_key', 'push_key', 'google_map', 'metrica_key', 'autocomplete',
                   'tenant_id', 'client_url', 'country', 'use_photo', 'photo_type', 'use_calls',
                   'use_calls_office', 'use_calls_driver', 'use_flat', 'use_porch', 'use_street', 'use_comment', 'use_pre_orders',
                   'shown_client_id', 'use_review_detail',
                   'use_wishes', 'use_detail', 'use_one_address', 'use_search', 'lang', 'use_calendars', 'use_cars', 'is_full_splash', 'max_one_address',
                   'default_calendar', 'use_country', 'use_referral', 'use_review_block', 'use_payment_cash',
                   'use_payment_card', 'use_payment_corp', 'is_demo', 'use_payment_bonus', 'show_company_balance', 'use_payment_personal',
                   'use_public_transport', 'web_application_url', 'web_application_title', 'use_web_application', "with_show_cars", 'car_radius']


def validate_app_fields(form: dict, check_id: bool=False) -> None:
    for filed in VALIDATE_FIELDS:
        if not form[filed]:
            raise DataError(DataError.not_found, DataError.data_invalid_mes % filed)
    if check_id and not form[FIELD_ID]:
        raise DataError(DataError.not_found, DataError.data_invalid_mes % FIELD_ID)


def validate_bundle(bundle: str) -> bool:
    if len(str(bundle).strip()) >= 5:
        return True
    return False


def parse_sku(bundle: str) -> str:
    if not validate_bundle(bundle):
        raise DataError(DataError.bundle_invalid, DataError.bundle_invalid_mes % bundle)
    return str(bundle).split('.')[2].lower()


def parse_language(languages: str) -> str:
    langs = languages.replace("\'", "\"").replace("[", "{").replace("]", "}")
    if len(langs) < 3:
        raise DataError(DataError.not_found, DataError.data_invalid_langs)
    return langs


def parse_app_by_json(app: dict) -> Application:
    parsed_json = validate_field(app)

    app_name = validate_field(parsed_json['app_name'])
    app_id = validate_field(parsed_json['app_id'])
    app_sku = validate_field(parsed_json['app_sku'])
    bundle = validate_field(parsed_json['bundle'])
    bundle_ios = validate_field(parsed_json['bundle_ios'])
    api_key = validate_field(parsed_json['api_key'])
    push_key = validate_field(parsed_json['push_key'])
    metrica_key = validate_field(parsed_json['metrica_key'])
    google_map = validate_field(parsed_json['google_map'])
    google_map_ios = validate_field(parsed_json['google_map_ios'])
    client_url = validate_field(parsed_json['client_url'])
    geo_url = validate_field(parsed_json['geo_url'])
    tenant_id = validate_field(parsed_json['tenant_id'])
    autocomplete = validate_field(parsed_json['autocomplete'])
    reverse_radius = validate_field(parsed_json['reverse_radius'])
    theme = validate_field(parsed_json['theme'])
    country = validate_field(parsed_json['country'])
    default_language = validate_field(parsed_json['default_language'])

    use_photo = validate_field(parsed_json['use_photo'])
    photo_type = validate_field(parsed_json['photo_type'])

    use_calls = validate_field(parsed_json['use_calls'])
    use_calls_office = validate_field(parsed_json['use_calls_office'])
    use_calls_driver = validate_field(parsed_json['use_calls_driver'])

    use_flat = validate_field(parsed_json['use_flat'])
    use_porch = validate_field(parsed_json['use_porch'])
    use_street = validate_field(parsed_json['use_street'])
    use_comment = validate_field(parsed_json['use_comment'])

    use_pre_orders = validate_field(parsed_json['use_pre_orders'])
    use_wishes = validate_field(parsed_json['use_wishes'])
    use_detail = validate_field(parsed_json['use_detail'])

    with_show_cars = validate_field(parsed_json['with_show_cars'])
    car_radius = validate_field(parsed_json['car_radius'])

    use_one_address = validate_field(parsed_json['use_one_address'])
    use_search = validate_field(parsed_json['use_search'])

    lang = validate_field(parsed_json['lang'])
    use_calendars = validate_field(parsed_json['use_calendars'])
    default_calendar = validate_field(parsed_json['default_calendar'])

    use_cars = validate_field(parsed_json['use_cars'])
    use_country = validate_field(parsed_json['use_country'])
    use_referral = validate_field(parsed_json['use_referral'])
    is_demo = validate_field(parsed_json['is_demo'])
    is_full_splash = validate_field(parsed_json['is_full_splash'])
    use_review_block = validate_field(parsed_json['use_review_block'])
    max_one_address = validate_field(parsed_json['max_one_address'])
    with_edit_order = validate_field(parsed_json['with_edit_order'])
    shown_client_id = validate_field(parsed_json['shown_client_id'])
    use_review_detail = validate_field(parsed_json['use_review_detail'])
    use_review_for_rejected = validate_field(parsed_json['use_review_for_rejected'])
    use_profile_data = validate_field(parsed_json['use_profile_data'])
    use_multi_callcost = validate_field(parsed_json['use_multi_callcost'])
    is_let_reject_after_assigned = validate_field(parsed_json['is_let_reject_after_assigned'])
    use_courier_form = validate_field(parsed_json['use_courier_form'])

    use_google = validate_field(parsed_json['use_google'])
    use_google_hybrid = validate_field(parsed_json['use_google_hybrid'])
    use_yandex_map = validate_field(parsed_json['use_yandex_map'])
    use_osm_map = validate_field(parsed_json['use_osm_map'])
    use_gis_map = validate_field(parsed_json['use_gis_map'])
    default_map = validate_field(parsed_json['default_map'])

    use_public_transport = validate_field(parsed_json['use_public_transport'])
    web_application_url = validate_field(parsed_json['web_application_url'])
    web_application_title = validate_field(parsed_json['web_application_title'])
    use_web_application = validate_field(parsed_json['use_web_application'])

    use_payment_card = validate_field(parsed_json['use_payment_card'])
    use_payment_corp = validate_field(parsed_json['use_payment_corp'])
    use_payment_cash = validate_field(parsed_json['use_payment_cash'])
    use_payment_bonus = validate_field(parsed_json['use_payment_bonus'])
    use_payment_personal = validate_field(parsed_json['use_payment_personal'])
    show_company_balance = validate_field(parsed_json['show_company_balance'])

    return Application(app_name=app_name, app_id=app_id, app_sku=app_sku, bundle=bundle, api_key=api_key,
                       push_key=push_key, metrica_key=metrica_key, client_url=client_url, theme=theme, geo_url=geo_url,
                       tenant_id=tenant_id, country=country, google_map=google_map, autocomplete=autocomplete,
                       reverse_radius=reverse_radius,bundle_ios=bundle_ios, google_map_ios=google_map_ios,
                       use_photo=use_photo, photo_type=photo_type,

                       use_calls=use_calls, use_calls_office=use_calls_office, use_calls_driver=use_calls_driver,

                       use_flat=use_flat, use_porch=use_porch, use_street=use_street, use_comment=use_comment,

                       use_pre_orders=use_pre_orders, use_wishes=use_wishes, use_detail=use_detail,

                       use_one_address=use_one_address, use_search=use_search, default_language=default_language,

                       lang=lang,

                       use_calendars=use_calendars, default_calendar=default_calendar,

                       use_cars=use_cars, use_country=use_country, is_demo=is_demo, is_full_splash=is_full_splash,
                       use_referral=use_referral, use_review_block=use_review_block, max_one_address=max_one_address,
                       with_edit_order=with_edit_order, shown_client_id=shown_client_id, use_review_detail=use_review_detail,
                       use_review_for_rejected=use_review_for_rejected, use_public_transport=use_public_transport,
                       web_application_url=web_application_url, web_application_title=web_application_title,
                       use_web_application=use_web_application, use_profile_data=use_profile_data, use_multi_callcost=use_multi_callcost,
                       is_let_reject_after_assigned=is_let_reject_after_assigned,

                       use_google=use_google, use_google_hybrid=use_google_hybrid, use_yandex_map=use_yandex_map,
                       use_osm_map=use_osm_map, use_gis_map=use_gis_map, default_map=default_map,
                       with_show_cars=with_show_cars, car_radius=car_radius,use_courier_form=use_courier_form,

                       use_payment_card=use_payment_card, use_payment_corp=use_payment_corp,
                       use_payment_cash=use_payment_cash, use_payment_bonus=use_payment_bonus,
                       show_company_balance=show_company_balance, use_payment_personal=use_payment_personal)


# Generate JSON app by request
def generate_app_json(form, hash_theme: str) -> dict:
    sku = parse_sku(form["bundle"])

    result = {
        "app_name": form["app_name"],
        "app_id": form["app_id"],
        "app_sku": sku,
        "bundle": form["bundle"],
        "bundle_ios": form["bundle_ios"],
        "api_key": form["api_key"],
        "tenant_id": form["tenant_id"],
        "autocomplete": form["autocomplete"],
        "reverse_radius": form["reverse_radius"],
        "client_url": form["client_url"],
        "geo_url": form["geo_url"],
        "push_key": form["push_key"],
        "metrica_key": form["metrica_key"],
        "google_map": form["google_map"],
        "google_map_ios": form["google_map_ios"],
        "theme": hash_theme,
        "country": form["country"],
        "default_language": form["default_language"],

        "use_photo": obj_to_bool(form["use_photo"]),
        "photo_type": (form["photo_type"]),

        "use_calls": obj_to_bool(form["use_calls"]),
        "use_calls_office": obj_to_bool(form["use_calls_office"]),
        "use_calls_driver": obj_to_bool(form["use_calls_driver"]),

        "use_flat": obj_to_bool(form["use_flat"]),
        "use_porch": obj_to_bool(form["use_porch"]),
        "use_street": obj_to_bool(form["use_street"]),
        "use_comment": obj_to_bool(form["use_comment"]),

        "use_pre_orders": obj_to_bool(form["use_pre_orders"]),
        "use_wishes": obj_to_bool(form["use_wishes"]),
        "use_detail": obj_to_bool(form["use_detail"]),

        "with_show_cars": obj_to_bool(form["with_show_cars"]),
        "car_radius": form["car_radius"],

        "use_one_address": obj_to_bool(form["use_one_address"]),
        "use_search": obj_to_bool(form["use_search"]),

        "use_calendars": obj_to_bool(form["use_calendars"]),
        "default_calendar": (form["default_calendar"]),

        "lang": parse_language(str(form.getlist("lang"))),

        "use_cars": obj_to_bool(form["use_cars"]),
        "use_country": obj_to_bool(form["use_country"]),
        "use_referral": obj_to_bool(form["use_referral"]),
        "is_demo": obj_to_bool(form["is_demo"]),
        "is_full_splash": obj_to_bool(form["is_full_splash"]),
        "use_review_block": obj_to_bool(form["use_review_block"]),
        "max_one_address": obj_to_bool(form["max_one_address"]),
        "with_edit_order": obj_to_bool(form["with_edit_order"]),
        "shown_client_id": obj_to_bool(form["shown_client_id"]),
        "use_review_detail": obj_to_bool(form["use_review_detail"]),
        "use_review_for_rejected": obj_to_bool(form["use_review_for_rejected"]),

        "use_public_transport": obj_to_bool(form["use_public_transport"]),
        "web_application_url": form["web_application_url"],
        "web_application_title": form["web_application_title"],
        "use_web_application": obj_to_bool(form["use_web_application"]),
        "use_profile_data": obj_to_bool(form["use_profile_data"]),
        "use_multi_callcost": obj_to_bool(form["use_multi_callcost"]),
        "is_let_reject_after_assigned": obj_to_bool(form["is_let_reject_after_assigned"]),
        "use_courier_form": obj_to_bool(form["use_courier_form"]),

        "use_google": obj_to_bool(form["use_google"]),
        "use_google_hybrid": obj_to_bool(form["use_google_hybrid"]),
        "use_yandex_map": obj_to_bool(form["use_yandex_map"]),
        "use_osm_map": obj_to_bool(form["use_osm_map"]),
        "use_gis_map": obj_to_bool(form["use_gis_map"]),
        "default_map": form["default_map"],

        "use_payment_card": obj_to_bool(form["use_payment_card"]),
        "use_payment_corp": obj_to_bool(form["use_payment_corp"]),
        "use_payment_cash": obj_to_bool(form["use_payment_cash"]),
        "use_payment_bonus": obj_to_bool(form["use_payment_bonus"]),
        "use_payment_personal": obj_to_bool(form["use_payment_personal"]),
        "show_company_balance": obj_to_bool(form["show_company_balance"])
    }

    logging.info(result)
    return result
