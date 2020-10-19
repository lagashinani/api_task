import requests
from progress_bar import my_progress_bar


vk_api_url = "https://cloud-api.yandex.net/v1/disk/resources"


class YAApi:
    def __init__(self, token):
        self.ya_token = token


    def save_to_yandex(self, path, photos):
        """Загружает файлы из photos на яндекс диск
            photos -  [date, likes, url, size]"""
        # создаем папку
        response = requests.put(vk_api_url, 
                headers={"Authorization": "OAuth " + self.ya_token,
                         "Content-Type": "application/json"},
                params={"path": path})

        names = set()
        results = []
        print("Uploading to YA drive")
        for photo in my_progress_bar(photos):
            name = str(photo[1])
            if photo[1] in names:
                name += "_"
                name += str(photo[0])

            names.add(name)

            response = requests.post(vk_api_url + "/upload", 
                headers={"Authorization": "OAuth " + self.ya_token,
                         "Content-Type": "application/json"},
                params={"path": path + "/" + name + ".jpg", 
                        "url": photo[2]})

            results.append({"file_name": name + ".jpg", "size": photo[3]})

        return results


    def upload(self, path, photos):
        return self.save_to_yandex(path, photos)