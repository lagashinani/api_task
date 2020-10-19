import requests
import hashlib
from progress_bar import my_progress_bar
import os

# нужно только в первый раз
# сходить по этой ссылке и вставить код из редиректа в переменную code
# если все работает - не трогать
'''
http://www.odnoklassniki.ru/oauth/authorize?client_id=512000665998&response_type=code&redirect_uri=http://localhost/qeqa&scope=VALUABLE_ACCESS;PHOTO_CONTENT
'''
code = ""
od_api_url = "https://api.ok.ru/"


class ODApi:
    redirect = "http://localhost/qeqa"

    def __init__(self, od_cred):
        self.refresh_token = od_cred["refresh_token"]
        ODApi.client_id = od_cred["client_id"]
        ODApi.client_secret = od_cred["client_secret"]
        ODApi.public_key = od_cred["public_key"]

        try:
            self.reauth()
        except Exception:
            self.update_refresh_token()
            self.reauth()


    def update_refresh_token(self):
        response = requests.post(od_api_url + "oauth/token.do", 
            params={"code": code, 
                    "redirect_uri": ODApi.redirect,
                    "grant_type": "authorization_code",
                    "client_id": ODApi.client_id,
                    "client_secret": ODApi.client_secret,
                    "permissions": "VALUABLE_ACCESS"
                    })

        self.refresh_token = response.json()["refresh_token"]

    def reauth(self):
        """Обновление токена с помощью ранее полученного refresh_token, за инфой в apiok.ru"""
        response = requests.post(od_api_url + "oauth/token.do", 
            params={"refresh_token": self.refresh_token, 
                    "grant_type": "refresh_token",
                    "client_id": ODApi.client_id,
                    "client_secret": ODApi.client_secret,
                    "permissions": "VALUABLE_ACCESS"
                    }).json()

        self.new_token = response["access_token"]

    def get_photos_links(self, fid="570768611709", count=5, album_id=None):
        """Возвращает массив [{date, likes, photo_url, size} * count] фотографий пользователя fid"""
        sig = hashlib.md5(("application_key=" + ODApi.public_key + \
                           "count=" + str(count) +\
                           "fid=" + fid +\
                           "fields=photo.*" +\
                           "format=json"+\
                           "method=photos.getPhotos" + \
                           hashlib.md5((self.new_token + ODApi.client_secret).encode()).hexdigest().lower()).encode()).hexdigest().lower()

        response = requests.post(od_api_url + "fb.do", 
                    params={"method": "photos.getPhotos",
                            "fid": fid,
                            "count": count,
                            "fields": "photo.*",
                            "format": "json",
                            "access_token": self.new_token,
                            "application_key": ODApi.public_key,
                            "sig": sig
                            })
        res = []
        for photo in response.json()["photos"]:
            res.append([photo["created_ms"], photo["like_summary"]["count"], 
                        photo["pic_max"], photo["standard_height"]])
        return res


    @staticmethod
    def save_photos(path, photos):
        """Получает на вход массив images и сохраняет их все в папку"""
        names = set()
        results = []

        print("Downloading Photos")
        for photo in my_progress_bar(photos):
            name = str(photo[1])
            if photo[1] in names:
                name += "_"
                name += str(photo[0])
            names.add(name)

            ODApi.save_photo(path + "/" + name + '.jpg', photo[2])

            results.append({"file_name": name + ".jpg", "size": photo[3]})

        return results



    @staticmethod
    def save_photo(path_image, url_image):
        os.makedirs(os.path.dirname(path_image), exist_ok=True)
        picture_request = requests.get(url_image)
        with open(path_image, 'wb') as f:
            f.write(picture_request.content)





if (__name__ == "__main__"):
    odapi = ODApi()
    odapi.reauth()
    ODApi.save_photos("570768611709", odapi.get_photos_links("570768611709", 10))