from builder.lib.model.entity.theme import Theme
from std.std import validate_field, hashing

VALIDATE_FIELDS = ['splash_bg', 'accent_bg', 'accent_text', 'menu_bg', 'menu_text', 'menu_stroke', 'content_bg',
                   'content_text', 'content_stroke', 'content_icon_bg', 'content_icon_stroke', 'map_marker_bg',
                   'map_marker_bg_stroke', 'map_marker_text', 'map_car_bg', 'accent_bg_tariff']


def parse_theme(json_theme: dict) -> Theme:
    validate_field(json_theme)

    splash_bg = validate_field(json_theme['splash_bg'])
    accent_bg = validate_field(json_theme['accent_bg'])
    accent_text = validate_field(json_theme['accent_text'])
    menu_bg = validate_field(json_theme['menu_bg'])
    menu_text = validate_field(json_theme['menu_text'])
    menu_stroke = validate_field(json_theme['menu_stroke'])
    content_bg = validate_field(json_theme['content_bg'])
    content_text = validate_field(json_theme['content_text'])
    content_stroke = validate_field(json_theme['content_stroke'])
    content_icon_bg = validate_field(json_theme['content_icon_bg'])
    content_icon_stroke = validate_field(json_theme['content_icon_stroke'])
    map_marker_bg = validate_field(json_theme['map_marker_bg'])
    map_marker_bg_stroke = validate_field(json_theme['map_marker_bg_stroke'])
    map_marker_text = validate_field(json_theme['map_marker_text'])
    map_car_bg = validate_field(json_theme['map_car_bg'])
    accent_bg_tariff = validate_field(json_theme['accent_bg_tariff'])

    # in last rabbit, when all field validated need calculate hash | SORT -> STR -> HASH
    theme_hash = get_theme_hash(json_theme)

    return Theme(splash_bg=splash_bg, accent_bg=accent_bg, accent_text=accent_text, menu_bg=menu_bg,
                 menu_text=menu_text, menu_stroke=menu_stroke, content_bg=content_bg, content_text=content_text,
                 content_stroke=content_stroke, content_icon_bg=content_icon_bg,
                 content_icon_stroke=content_icon_stroke, map_marker_bg=map_marker_bg,
                 map_marker_bg_stroke=map_marker_bg_stroke, map_marker_text=map_marker_text, map_car_bg=map_car_bg,
                 accent_bg_tariff=accent_bg_tariff, hash=theme_hash)


# Dict must be without fields [id, hash]
def get_theme_hash(form: dict) -> str:
    colors_str = ""
    for filed in VALIDATE_FIELDS:
        colors_str += form[filed]
    return hashing(colors_str)
