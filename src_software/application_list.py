from constants import *
import constants

from classes import APPLICATION
from src_software.download_software import download_from_archive
import json
import os

def get_download_list() -> list:
    # print("GETTING DOWNLOAD LIST")
    download_list = []
    application_list = "application_list.json"

    if not os.path.exists(UTILITY_FOLDER_PATH + application_list):
        download_from_archive(application_list, False)

    with open(UTILITY_FOLDER_PATH + application_list, "r") as json_file:
        json_data = json.load(json_file)


    for item in json_data:
        app = APPLICATION(item["display"], item["name"], item["link"])
        download_list.append(app)

    custom = APPLICATION("Custom Scripts","Custom Scripts","Archive")
    download_list.append(custom)

    constants.APPLICATION_DOWNLOAD_LIST = download_list