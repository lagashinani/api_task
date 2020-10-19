import requests
import os
from progress_bar import my_progress_bar

vk_api_url = "http://api.vk.com/method/"
vk_version = "5.124"

class VKApi:
    def __init__(self, token):
        self.vk_token = token


    def get_id(self, user_id):
        """по строке, в которой в каком-то виде screen_name или id возвращает id"""
        if isinstance(user_id, int):
            return user_id

        elif user_id[:2] == "id":
            user_id = user_id[2:]

        try:
            user_id = int(user_id)
        
        except ValueError:
            user_id = self.req_id_by_alias(user_id)

        return user_id


    def req_id_by_alias(self, alias):
            """Возвращает id пользователя по его screen_name, в случае ошибки - None"""
            response = requests.get(vk_api_url + "users.get", 
                params={"user_ids": alias, 
                        "access_token": self.vk_token,
                        "v": vk_version
                        })

            response_parsed = response.json()
            if "error" in response_parsed:
                print(response_parsed)
                return None
            else:
                return int(response_parsed["response"][0]["id"]) 


    def get_photos_links(self, user_id, count=5, album_id="profile"):
        """Возвращает список последние count фотографий из альбома album_id в формате [date, likes, url, size]"""
        user_id = self.get_id(user_id)
        try:
            response = requests.get(vk_api_url + "photos.get", 
                    params={"owner_id": user_id,
                            "album_id": album_id, 
                            "access_token": self.vk_token,
                            "extended": 1,
                            # "photo_sizes": 1,
                            "rev": 1,
                            "count": count,
                            "v": vk_version
                            })
            photos_nfiltered = response.json()["response"]["items"]
        except Exception:
            print(response.content)


        order = "wzyxrqpmos"
        photos_filtered = []
        print("Getting Links")
        for photo in my_progress_bar(photos_nfiltered):
            dt = photo["date"]
            likes = photo["likes"]["count"]
            sizes = min(photo["sizes"], key=lambda x: order.find(x["type"]))
            url = sizes["url"]
            size = sizes["type"]
            photos_filtered.append([dt, likes, url, size])

        return photos_filtered


    @staticmethod
    def save_photos(path, photos):
        """Получает на вход массив images и сохраняет их все в папку"""
        names = set()
        results = []

        print("Downloading Photos")
        for photo in my_progress_bar(photos):
            name = str(photo[1])
            if (photo[1] in names):
                name += "_"
                name += str(photo[0])
            names.add(name)

            VKApi.save_photo(path + "/" + name + '.jpg', photo[2])

            results.append({"file_name": name + ".jpg", "size": photo[3]})

        return results



    @staticmethod
    def save_photo(path_image, url_image):
        os.makedirs(os.path.dirname(path_image), exist_ok=True)
        picture_request = requests.get(url_image)
        with open(path_image, 'wb') as f:
            f.write(picture_request.content)