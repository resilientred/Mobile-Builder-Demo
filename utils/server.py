import flask
import logging
from flask import Flask
from flask import json
import re
import fileinput


app = Flask(__name__)


@app.route("/get_rules", methods=['GET'])
def get_home():
    return json.dumps([{"title": "Hello",
                        "description": "description",
                        "rating": 12,
                        "complexity": 11,
                        "size": 13,
                        "image": "image",
                        }])


def regex_language():
    return '^.*\sarr\.append\(([^;]+)\)$'


def find_language(text):
    return re.findall(regex_language(), text, flags=re.MULTILINE)


# PUT FUNCTIONS
def find_language_line(key) -> str:
    language_block = ""
    with fileinput.FileInput("/Users/santa/Desktop/Code/iOS/Constants.swift", inplace=True) as file:
        for line in file:
            if f"country.{key}" in str(line):
                matches = find_language(line)
                if len(matches) > 0:
                    language_block = matches[0]
            print(line, end='')
    return language_block


# FIND REGEX
def regex_return():
    return '^.*\sreturn\s{1}([^;]+)$'


def find_return(text):
    return re.findall(regex_return(), text, flags=re.MULTILINE)


def put_return(new):
    with fileinput.FileInput("/Users/santa/Desktop/Code/iOS/Config.swift", inplace=True) as file:
        for line in file:
            group = find_return(line)
            if len(group) > 0:
                print(line.replace(group[0], str(new).lower()), end='\n')
            else:
                print(line, end='')


def configure_language(config):
    lang_block = find_language_line("kz")
    if len(lang_block) > 0:
        put_return(lang_block)
