from builder.lib.model.entity.app import Application
from std.std import validate_field


def parse_app_by_json(app: dict) -> Application:
    parsed_json = validate_field(app)

    id = validate_field(parsed_json['id'])
    app_name = validate_field(parsed_json['app_name'])
    app_id = validate_field(parsed_json['app_id'])
    app_sku = validate_field(parsed_json['app_sku'])
    bundle = validate_field(parsed_json['bundle'])
    bundle_ios = validate_field(parsed_json['bundle_ios'])
    api_key = validate_field(parsed_json['api_key'])
    push_key = validate_field(parsed_json['push_key'])
    google_map_ios = validate_field(parsed_json['google_map_ios'])
    metrica_key = validate_field(parsed_json['metrica_key'])
    google_map = validate_field(parsed_json['google_map'])
    client_url = validate_field(parsed_json['client_url'])
    geo_url = validate_field(parsed_json['geo_url'])
    tenant_id = validate_field(parsed_json['tenant_id'])
    theme = validate_field(parsed_json['theme'])
    country = validate_field(parsed_json['country'])
    autocomplete = validate_field(parsed_json['autocomplete'])
    reverse_radius = validate_field(parsed_json['reverse_radius'])

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
    default_language = validate_field(parsed_json['default_language'])

    with_show_cars = validate_field(parsed_json['with_show_cars'])
    car_radius = validate_field(parsed_json['car_radius'])

    use_public_transport = validate_field(parsed_json['use_public_transport'])
    web_application_url = validate_field(parsed_json['web_application_url'])
    web_application_title = validate_field(parsed_json['web_application_title'])
    use_web_application = validate_field(parsed_json['use_web_application'])
    use_multi_callcost = validate_field(parsed_json['use_multi_callcost'])
    is_let_reject_after_assigned = validate_field(parsed_json['is_let_reject_after_assigned'])
    use_courier_form = validate_field(parsed_json['use_courier_form'])

    use_google = validate_field(parsed_json['use_google'])
    use_google_hybrid = validate_field(parsed_json['use_google_hybrid'])
    use_yandex_map = validate_field(parsed_json['use_yandex_map'])
    use_osm_map = validate_field(parsed_json['use_osm_map'])
    use_gis_map = validate_field(parsed_json['use_gis_map'])
    default_map = validate_field(parsed_json['default_map'])

    use_payment_card = validate_field(parsed_json['use_payment_card'])
    use_payment_corp = validate_field(parsed_json['use_payment_corp'])
    use_payment_cash = validate_field(parsed_json['use_payment_cash'])
    use_payment_bonus = validate_field(parsed_json['use_payment_bonus'])
    use_payment_personal = validate_field(parsed_json['use_payment_personal'])
    show_company_balance = validate_field(parsed_json['show_company_balance'])

    return Application(id=id, app_name=app_name, app_id=app_id, app_sku=app_sku, bundle=bundle, api_key=api_key,
                       push_key=push_key, metrica_key=metrica_key, client_url=client_url, theme=theme, geo_url=geo_url,
                       reverse_radius=reverse_radius, bundle_ios=bundle_ios, google_map_ios=google_map_ios,
                       tenant_id=tenant_id, country=country, google_map=google_map, autocomplete=autocomplete,
                       use_photo=use_photo, photo_type=photo_type,

                       use_calls=use_calls, use_calls_office=use_calls_office, use_calls_driver=use_calls_driver,

                       use_flat=use_flat, use_porch=use_porch, use_street=use_street, use_comment=use_comment,

                       use_pre_orders=use_pre_orders, use_wishes=use_wishes, use_detail=use_detail,

                       use_one_address=use_one_address, use_search=use_search, default_language=default_language,

                       lang=lang,

                       use_calendars=use_calendars, default_calendar=default_calendar,

                       use_cars=use_cars, use_country=use_country, is_demo=is_demo,
                       use_referral=use_referral, use_review_block=use_review_block, is_full_splash=is_full_splash,
                       max_one_address=max_one_address, shown_client_id=shown_client_id, use_review_detail=use_review_detail,
                       use_review_for_rejected=use_review_for_rejected, with_edit_order=with_edit_order,
                       use_public_transport=use_public_transport, web_application_url=web_application_url,
                       web_application_title=web_application_title, use_web_application=use_web_application,
                       use_profile_data=use_profile_data,use_multi_callcost=use_multi_callcost,
                       is_let_reject_after_assigned=is_let_reject_after_assigned,

                       use_google=use_google, use_google_hybrid=use_google_hybrid, use_yandex_map=use_yandex_map,
                       use_osm_map=use_osm_map, use_gis_map=use_gis_map, default_map=default_map,
                       with_show_cars=with_show_cars, car_radius=car_radius, use_courier_form=use_courier_form,

                       use_payment_card=use_payment_card, use_payment_corp=use_payment_corp,
                       use_payment_cash=use_payment_cash, use_payment_bonus=use_payment_bonus,
                       show_company_balance=show_company_balance, use_payment_personal=use_payment_personal)
