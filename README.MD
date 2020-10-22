# BackUp Helper
## Photo Backup project for backup from VK/Odnoklassniki to GoogleDrive/YandexDisk

Файл для запуска: reserve_copy.py

Для начала работы требуется получить и внести следующие токены/данные:
1) Для работы с GoogleDrive: credentials.json  -- файл, получаемый при регистрации приложения для доступа к [api](https://developers.google.com/drive/api/v3/about-auth) GoogleDrive. Должен располагаться в корневой директории.
2) Для работы с YandexDisk: требуется токен, который нужно получить с полигона и положить соответственно в переменную ya_token reserve_copy.py.
3) Для работы с Odnoklassniki: требуется зарегистрировать приложение с правами VALUABLE_ACCESS;PHOTO_CONTENT и внести полученные данные в структуру od_cred reserve_copy.py.
4) Для работы с VK: требуется токен, положить в vk_token reserve_copy.py.
