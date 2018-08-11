import json

from std import config
from std.std import merge

country_mask = 'mask'
country_cc = 'cc'
country_name_en = 'name_en'
country_desc_en = 'desc_en'
country_name_ru = 'name_ru'
country_desc_ru = 'desc_ru'


def get_country(code: str) -> dict:
    country_assets = merge(config.ASSETS_PATH, 'phonecodes.json')

    with open(country_assets) as data_file:
        countries = json.load(data_file)
        for country in countries:
            if country['cc'] == code.upper():
                return country



