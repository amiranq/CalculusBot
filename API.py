import uuid
import requests
import json
import warnings
import time

warnings.filterwarnings("ignore")

client_id = "c1310d16-f951-491e-a69f-5b41574665a4"
secret = "99ac4c3a-6ad7-417d-bbe2-a71ddd52def9"
auth = "YzEzMTBkMTYtZjk1MS00OTFlLWE2OWYtNWI0MTU3NDY2NWE0Ojk5YWM0YzNhLTZhZDctNDE3ZC1iYmUyLWE3MWRkZDUyZGVmOQ=="

giga_token = "eyJjdHkiOiJqd3QiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiUlNBLU9BRVAtMjU2In0.aSTGVfyHpezhU2WlfpAGbqPsjfT6r8O6oENBC9y78aYh9bSj0swGYANDZfe1V5bh90-ui578WEdWL_X4NgUgkPQWvYBlo50Q3tXO96vsRnDZ3vRZ7ZUe7rZq07VXMngWQVYqYz5QjLyMZqAn_WFw1CgK_YF7VXXTxvN14LonVcPd5E6DCqAQOe2K53PI9eBqHMXonNLx06DF-dhi-ykVT58SGLXdZjDNDN9dZYLmWBSfozx9kv7n9DRFQxbT5ymbXEEq_O5O2C9x1YGJmS5p5JiEzS-wv8ENDf5Mb3FOWebDc7HFrtT3ptyOce0uRvC2DZ5vx4rY7VDmYgPDiskAag.7UtbQrxrUsoW7oycwr0Prg.MSEnnEeeYynXC-vNQjA1PXBXNNIt8RvcbcpTlNMYRbPTwSGoiriLA9At-zPNR4f_tysuXaCTay-uOqzr7THRQ7NCpH1eBhuEWDIvCNNlj9iQ7aCsvVOx8TfVysrS6OxKmA3-OqfnqLdksDVzWhOkPZIPdn3BOdRPm6y5ZNBwSOM3pzy9cojqXU5jZLLeojpq9F31MY_Rx_wa_SYLp0_1cHiKRPglDhG7DjeeWmFWYd3ERFPkz_pmUADu7tT8t9RTLRKTCBeejhSrMdwVEk4gmF4k1S2IFjlXLCJIYjvO8V7vv1hMTP9MMbfV6D2A_2rRxnacD0OJHG1mY0cNfHhHRSQtEJTNanOkBNIMmBB7kdveYBK1IQaP-j_VDAIFAekhkX6YY_RWb96SEd47OtdCiP0hF-qUfHQW2WcRDwXIEZY_eizwVMMgzD4Ou_g6JocKZz5syo7uGInbZeCsmuOP-9YY02kY9oTqZJT_RwPHQj0EAmJEHI7kiDDH7QGdmbDGgeCcbHif0kPjJxPn-VemMs524p-odPAFty6s7xkKi6QZjOtAFH88aCCVkn5EVKlhnfGUK2sJlKUra64w8UpVUD1-XQcPTWoe7u-I03dMq1do8E_GFDR9lKiZq1lJIHUFYswCz_L0wqoSLT-5MrnhgDQxP4oLsBN25pzIP4nIkMB3V_BI8_-6BuuG9DrIU4shiHi_wefgyS1pEn_O_UKYja0CODQ-gzP67xNyJ6eyoxw.MLyK-VSYsILfSOaaglui8Ro_PGqGJ6QI-tDxqiFcFmI"


def get_token(auth_token, scope='GIGACHAT_API_PERS'):
    """
      Выполняет POST-запрос к эндпоинту, который выдает токен.

      Параметры:
      - auth_token (str): токен авторизации, необходимый для запроса.
      - область (str): область действия запроса API. По умолчанию — «GIGACHAT_API_PERS».

      Возвращает:
      - ответ API, где токен и срок его "годности".
      """
    # Создадим идентификатор UUID (36 знаков)
    rq_uid = str(uuid.uuid4())

    # API URL
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    # Заголовки
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': rq_uid,
        'Authorization': f'Basic {auth_token}'
    }

    # Тело запроса
    payload = {
        'scope': scope
    }

    try:
        # Делаем POST запрос с отключенной SSL верификацией
        # (можно скачать сертификаты Минцифры, тогда отключать проверку не надо)
        response = requests.post(url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        print(f"Ошибка: {str(e)}")
        return "Промыслов прилёг отдохнуть и тебе советует"


def post_image(path, giga_token):
    try:
        url = "https://gigachat.devices.sberbank.ru/api/v1/files"

        payload = {'purpose': 'general'}
        files = [
            ('file', ('response.jpeg', open(f'{path}', 'rb'), 'image/jpeg'))
        ]
        headers = {
            'Authorization': f'Bearer {giga_token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=False)

        # print(response.text)
        print(response.text)
        return response.json()["id"]
    except Exception as e:
        print("Все поломалось:", str(e))
        return "Промыслов прилёг отдохнуть и тебе советует"


def get_chat_completion(auth_token, attachment=None, text=""):
    """
    Отправляет POST-запрос к API чата для получения ответа от модели GigaChat.

    Параметры:
    - auth_token (str): Токен для авторизации в API.
    - attachment (str): ID фотографии
    - text (str): Запрос от пользователя

    Возвращает:
    - str: Ответ от API в виде текстовой строки.
    """
    # URL API, к которому мы обращаемся
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    if attachment:
        payload = json.dumps({
            "model": "GigaChat-Pro",  # Используемая модель
            "messages": [
                {
                    "role": "user",  # Роль отправителя (пользователь)
                    "content": f"Какие темы, определения и теоремы нужно знать, чтобы решить данный пример(решать его не нужно): {text}",  # Содержание сообщения
                    "attachments": [
                        f"{attachment}"
                    ]
                }
            ],
            "temperature": 1,  # Температура генерации
            "top_p": 0.1,  # Параметр top_p для контроля разнообразия ответов
            "n": 1,  # Количество возвращаемых ответов
            "stream": False,  # Потоковая ли передача ответов
            "max_tokens": 512,  # Максимальное количество токенов в ответе
            "repetition_penalty": 1,  # Штраф за повторения
            "update_interval": 0  # Интервал обновления (для потоковой передачи)
        })
    else:
        payload = json.dumps({
            "model": "GigaChat",  # Используемая модель
            "messages": [
                {
                    "role": "user",  # Роль отправителя (пользователь)
                    "content": f"Какие темы, определения и теоремы нужно знать, чтобы решить данный пример(решать его не нужно): {text}",
                }
            ],
            "temperature": 1,  # Температура генерации
            "top_p": 0.1,  # Параметр top_p для контроля разнообразия ответов
            "n": 1,  # Количество возвращаемых ответов
            "stream": False,  # Потоковая ли передача ответов
            "max_tokens": 1024,  # Максимальное количество токенов в ответе
            "repetition_penalty": 1,  # Штраф за повторения
            "update_interval": 0  # Интервал обновления (для потоковой передачи)
        })

    # Заголовки запроса
    headers = {
        'Content-Type': 'application/json',  # Тип содержимого - JSON
        'Accept': 'application/json',  # Принимаем ответ в формате JSON
        'Authorization': f'Bearer {auth_token}'  # Токен авторизации
    }

    # Выполнение POST-запроса и возвращение ответа
    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        # Обработка исключения в случае ошибки запроса
        print(f"Произошла ошибка: {str(e)}")
        return "Промыслов прилёг отдохнуть и тебе советует"


def get_answer(path="", text=""):
    try:
        giga_token = get_token(auth_token=auth).json()["access_token"]
        if path != "":
            attach_id = post_image(path, giga_token)
            response = get_chat_completion(giga_token, attach_id, text=text)
        else:
            response = get_chat_completion(giga_token, text=text)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print("Все поломалось:", str(e))
        return "Промыслов прилёг отдохнуть и тебе советует"
