import requests
import json
import time
import sys

from vk import VKApi
from ya import YAApi
from gd import GDApi
from od import ODApi

vk_token = ""
ya_token = ""

od_cred = {"client_id": "",
           "client_secret": "", 
           "public_key": "",
           "refresh_token": ""}



def choose_net_and_download():
    while True:
        soc_net = input("Download from vk or [od] noklassniki: ")
        album = None
        if soc_net == "vk":
            soc_api = VKApi(vk_token)
            album = input("Choose album (default profile): ")
            if album == "":
                album = "profile"
            break
        elif soc_net == "od":
            soc_api = ODApi(od_cred)
            break
        elif soc_net == "e":
            return None
        else:
            print("Wrong choice. Use vk or od or e for exit")
            continue

    user = input("Enter user id: ")
    count = int(input("Enter photo count: "))

    print("Downloading {} photos from {} of user {}".format(count, soc_net, user))

    photos_links = soc_api.get_photos_links(user, count=count, album_id=album)

    saved = soc_api.save_photos(user + "_downloaded", photos_links)

    return [user + "_downloaded", photos_links]

def choose_drive_and_upload(path_name, saved):
    while True:
        drive = input("Upload drive [gd] or [ya]: ")
        if drive == "ya":
            drive = YAApi(ya_token)
            break
        elif drive == "gd":
            drive = GDApi()
            break
        elif drive == "e":
            return None
        else:
            print("Wrong choice. Use ya or gd or e for exit")
            continue
    
    uploaded = drive.upload(path_name, saved)

    return uploaded


saved = choose_net_and_download()
uploaded = choose_drive_and_upload(*saved)


with open("saved_photos.json", "w+") as out:
    json.dump(uploaded, out)
