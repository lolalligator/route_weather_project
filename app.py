import requests
import json
from flask import Flask
from api_key import api_key

app = Flask(__name__)

response_lang = "ru-ru"


@app.route('/')
def hello_world():
    return 'Hello, World!'


def test_request(latitude: float = 55.791541, longitude: float = 37.748656) -> str:
    """
    Тестовый запрос для проверки работоспособности API.
    Возвращает данные о дневном прогнозе погоды в локации по её геопозиции
    (latitude и longitude) - географическая широта и географическая долгота

    Ответ в формате JSON со следующими значениями:

    - temperature - Средняя дневная температура

    - humidity - Относительная влажность воздуха

    - wind_speed - Средняя дневная скорость воздуха

    - rain_probability - Дневная вероятность выпадения дождя

    :param latitude: Географическая широта
    :param longitude: Географическая долгота
    :return: Данные о погоде в формате JSON
    """
    # Получение геопозиции
    q = f"{latitude},{longitude}"
    geo_base_url = "http://dataservice.accuweather.com/locations/v1/cities/geoposition/search"
    params = {
        "apikey": api_key,
        "q": q,
        "language": response_lang,
    }
    response = requests.get(geo_base_url, params=params)
    if response.status_code != 200:
        print(f"Ошибка при получении геолокации: {response.text}")
        return
    location_key = response.json()["Key"]

    # Получение прогноза погоды на основе геопозиции
    current_conditions_base_url = f"http://dataservice.accuweather.com/forecasts/v1/daily/1day/{location_key}"
    params = {
        "apikey": api_key,
        "language": response_lang,
    }
    response = requests.get(current_conditions_base_url, params=params)
    if response.status_code != 200:
        print(f"Ошибка при получении геолокации: {response.text}")
        return
    response_json = response.json()
    temperature_data = response_json["DailyForecasts"]["Day"]["WetBulbTemperature"]["Average"]
    humidity_data = response_json["DailyForecasts"]["Day"]["RelativeHumidity"]["Average"]
    wind_speed_data = response_json["DailyForecasts"]["Day"]["Wind"]["Speed"]
    rain_probability_data = response_json["DailyForecasts"]["Day"]["RainProbability"]
    result = {
        "temperature": temperature_data["Value"],
        "humidity": humidity_data,
        "wind_speed": wind_speed_data["Value"],
        "rain_probability": rain_probability_data,
    }
    json_result = json.dumps(result, indent=4)
    return json_result


# Тестовые запросы, чтобы проверить работоспособность API
# Тестовый запрос для места "Москва, Измайлово Гамма"
test_request()

# Тестовый запрос для места "Екатеринбург"
test_request(56.837864, 60.594882)
