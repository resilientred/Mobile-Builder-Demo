import json

from builder.lib.model.helper import theme_helper
from builder.lib.script.launcher.launcher_factory import LauncherFactory
from builder.lib.script.resource.ios_resource import IosResourceHelper
from std import config
from std.std import merge
from backend.model.helper import app_helper


file_path = "/Users/santa/Desktop/Code/Python/python-build-script/test/ios/assets/Info.plist"

app_json = '''
{"id": 57, "app_name": "Avalon", "app_id": 666, "app_sku": "avalonservice", "bundle":
"com.gootax.avalonservice", "api_key": "666", "push_key": "500889195991", "google_map":
"AIzaSyDtErekKTTCd7kDMPSQmMMntUvqyRJMI_Q", "metrica_key": "666",
"tenant_id": 666, "theme": "ca0f76a332099ca8b0e4bb293b7ba7cd", "client_url": "666",
"country": "RU", "status": 4, "use_photo": false, "photo_type": "driver", "use_calls": false,
"use_calls_office": true, "use_calls_driver": true, "use_flat": false, "use_porch": false,
"use_street": false, "use_comment": false, "use_pre_orders": false, "use_wishes": false,
"use_detail": false, "use_one_address": false, "use_search": false, "lang": "{\\"en\\", \\"ru\\", \\"sr\\"}",
"use_calendars": true, "default_calendar": "gregorian", "use_cars": false, "use_country": false, "use_referral": false,
"is_demo": false, "use_review_block": false, "use_payment_card": false, "use_payment_corp": false,
"use_payment_cash": false, "use_payment_bonus": false, "show_company_balance": false,
"use_referral": true,"use_country": true,"default_calendar": true, "is_demo": false, "use_review_block": true,
"status": 4, "use_calls_driver": true,"autocomplete": 40,"use_payment_personal": true,"is_full_splash": false,
"max_one_address": true, "with_edit_order": true,"geo_url": "https://geo.gootax.pro/v1", "reverse_radius": 0.1}
'''

theme_json = '''
{"splash_bg": "#ced628", "accent_bg": "#ced628",
"accent_text": "#000000", "menu_bg": "#3b3c51", "menu_text": "#ffffff", "menu_stroke": "#ffffff",
"content_bg": "#ced628", "content_text": "#000000", "content_stroke": "#000000", "content_icon_bg": "#3b3c51",
"content_icon_stroke": "#3b3c51", "map_marker_bg": "#3b3b53", "map_marker_bg_stroke": "#3b3b53",
"map_marker_text": "#ced628", "map_car_bg": "#7f81aa", "accent_bg_tariff": "#ced628"}
'''

res = IosResourceHelper(assets_ios=merge(config.BASE_DIR, "/test/ios/assets"),
                        finish_path=merge(config.BASE_DIR, "/resource/master/gootax_app_ios_client_swift23"),
                        path_to_res=merge(config.BASE_DIR, "/test/ios/assets"))

logo_splash = "logo_splash"
menulogo = "menulogo"

params = {
    "need_build_android": False,
    "need_build_ios": True,
    "need_clear": False,
    "create_app": True,
    "version_name": "4",
    "version_code": "1.3",
    "default_bundle": "com.gootax.client",
    "email": "sargeras701@gmail.com"
}

app = app_helper.parse_app_by_json(json.loads(app_json))

builder = LauncherFactory.create_launcher(application=app,
                                          theme=json.loads(theme_json),
                                          params=params,
                                          build_type="ios")
builder.generate()
