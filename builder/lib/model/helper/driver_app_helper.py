# Author Andrew Chupin
# Coding in UTF-8

# Generate JSON app by request
from backend.model.entity.driver_app import DriverApplication
from std.std import validate_field


def generate_app_json(form) -> dict:
    return {
        "app_name": form["app_name"],
        "bundle": form["bundle"],
        "tenant_name": form["tenant_name"],
        "host": form["host"],
        "new_host": form["new_host"],
        "chat_host": form["chat_host"],
        "geocode_host": form["geocode_host"],
        "push_key": form["push_key"],
        "google_map_key": form["google_map_key"],
        "app_type": int(form["app_type"]),
        "version_app": int(form["version_app"])
    }


def parse_app_by_json(parsed_json: dict) -> DriverApplication:
    app_name = validate_field(parsed_json['app_name'])
    tenant_name = validate_field(parsed_json['tenant_name'])
    bundle = validate_field(parsed_json['bundle'])
    host = validate_field(parsed_json['host'])
    new_host = validate_field(parsed_json['new_host'])
    chat_host = validate_field(parsed_json['chat_host'])
    geocode_host = validate_field(parsed_json['geocode_host'])
    push_key = validate_field(parsed_json['push_key'])
    google_map_key = validate_field(parsed_json['google_map_key'])
    app_type = validate_field(parsed_json['app_type'])
    version_app = validate_field(parsed_json['version_app'])

    return DriverApplication(app_name=app_name, tenant_name=tenant_name, bundle=bundle,
                             host=host, new_host=new_host, chat_host=chat_host, geocode_host=geocode_host,
                             push_key=push_key, google_map_key=google_map_key, app_type=app_type,
                             version_app=version_app)
