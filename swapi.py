import requests
from pathlib import Path


class APIRequester:
    # base_url - базовый адрес API.
    def __init__(self, base_url):
        self.base_url = base_url  # Запоминает базовый адрес внутри объекта.

    def get(self, url):
        try:
            # Отправляем GET-запрос по собранному адресу.
            response = requests.get(
                f'{self.base_url.rstrip("/")}/{url.lstrip("/")}')
            # Проверяем статус ответа. Если ошибка, вызываем исключение.
            response.raise_for_status()
            return response    # Если все хорошо, возвращаем объект ответа.
        except requests.exceptions.RequestException:
            print('Возникла ошибка при выполнении запроса')
            return None  # В случае ошибки возвращаем None.


class SWRequester(APIRequester):  # SWRequester наследуется от APIRequester.
    def __init__(self, base_url='https://swapi.dev/api'):
        # Вызываем двигатель родительского класса, передавая базовый URL.
        super().__init__(base_url)

    # Метод для получения списка доступных категорий.
    def get_sw_categories(self):
        response = self.get('/')  # Вызываем get() из родительского класса.
        if response:
            # Преобразуем ответ от API в словарь Python.
            categories_data = response.json()
            # Возвращаем только названия категорий.
            return categories_data.keys()

    # Метод для получения информации по конкретной категории.
    def get_sw_info(self, sw_type):
        # Составляем путь к нужной категории, например 'people/'.
        # Отправляем запрос через родительский метод get().
        response = self.get(sw_type + '/')
        if response:
            return response.text  # Возвращаем полученный ответ в виде строки.
        return ''  # Если ответа нет, возвращаем пустую строку.


def save_sw_data():
    # Создаем объект класса SWRequester.
    sw_api = SWRequester('https://swapi.dev/api')

    # Создаем директорию 'data', если ее еще нет.
    data_dir = Path('data')
    # exist_ok=True позволяет не выдавать ошибку, если папка уже есть.
    data_dir.mkdir(exist_ok=True)

    # Получаем список всех доступных категорий SWAPI.
    categories = sw_api.get_sw_categories()
    if not categories:
        print('Не удалось получить список категорий.')
        return

    print(f'Найденные категории: {categories}')

    # Для каждой категории выполняем запрос и сохраняем данные.
    for category in categories:
        category_info = sw_api.get_sw_info(category)

        if category_info:
            # Формируем имя файла, например, 'data/people.txt'.
            filename = str(data_dir) + '/' + f'{category}.txt'
            with open(filename, 'w', encoding='utf-8') as f:
                # Записываем полученную информацию в файл.
                f.write(category_info)
            print(f'Данные для категории "{category}" сохранены')
        else:
            print(f'Не удалось получить данные для категории "{category}"')

    print('Все данные SWAPI успешно сохранены!')
