import fileinput
import json
import os

import re
from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/get_check_token", methods=["GET"])
def get_check_token():
    params = request.args
    print(params)
    return json.dumps({
        "code": 0,
        "result": 0
    })


# FIND REGEX
def regex_psfs(key):
    return '^.*\s' + key + '\s=\s\"([^\"]+)\".*$'


# FIND FUNCTIONS
def find_psfs(text, key):
    return re.findall(regex_psfs(key), text, flags=re.MULTILINE)


def regex_obj(key):
    return '^.*\s' + key + '\s*=\s*([^;]+).*$'


def find_obj(text, key):
    return re.findall(regex_obj(key), text, flags=re.MULTILINE)


def replace_distribution_cert(file_path, company_id):
    CODE_SIGN_IDENTITY = "CODE_SIGN_IDENTITY"
    DEVELOPMENT_TEAM = "DEVELOPMENT_TEAM"
    team = "dsadasdasdasdasd"
    distribution_name = f"iPhone Distribution: {team} ({company_id})"

    with fileinput.FileInput("/Users/andrew/PycharmProjects/python-build-script-res/resource/master/Client.xcodeproj/project.pbxproj", inplace=True) as file:
        for line in file:
            group = find_psfs(line, CODE_SIGN_IDENTITY)
            group_corp = find_obj(line, DEVELOPMENT_TEAM)
            if len(group) > 0:
                print(line.replace(group[0], str(distribution_name)), end='')
            elif len(group_corp) > 0:
                print(line.replace(group_corp[0], str(company_id)), end='')
            else:
                print(line, end='')
                continue


if os.path.exists("/Users/andrew/PycharmProjects/python-build-script-res/resource/res/com.gootax.taxi111/com.gootax.taxi111.p12"):
    print("Path exist")