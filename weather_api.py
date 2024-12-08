import requests
import json
from api_key import api_key

response_lang = "ru-ru"


def check_bad_weather(temperature: float, wind_speed: float, precipitation_probability: float) -> bool:
    """
    Проверяет по данным из прогноза погоды (температуре, скорости ветра, вероятности осадков),
    является ли погода плохой. Возвращает True, если погода плохая и False - иначе.

    :param temperature: Температура
    :param wind_speed: Скорость ветра
    :param precipitation_probability: Вероятность осадков
    :return: Ответ на вопрос: является ли погода плохой. (True/False)
    """
    if temperature < 0 or temperature > 35:
        return True
    if wind_speed > 50:
        return True
    if precipitation_probability > 70:
        return True


def get_forecast_data_by_geo_position(latitude: float = 55.791541, longitude: float = 37.748656) -> str:
    """
    Возвращает данные о дневном прогнозе погоды в локации по её геопозиции
    (latitude и longitude) - географическая широта и географическая долгота

    Ответ в формате JSON со следующими значениями:

    - temperature - Средняя дневная температура

    - humidity - Относительная влажность воздуха

    - wind_speed - Средняя дневная скорость воздуха

    - precipitation_probability - Дневная вероятность выпадения осадков

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
        return "{}"
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
        return "{}"
    response_json = response.json()
    temperature_data = response_json["DailyForecasts"]["Day"]["WetBulbTemperature"]["Average"]
    humidity_data = response_json["DailyForecasts"]["Day"]["RelativeHumidity"]["Average"]
    wind_speed_data = response_json["DailyForecasts"]["Day"]["Wind"]["Speed"]
    precipitation_probability = response_json["DailyForecasts"]["Day"]["PrecipitationProbability"]
    result = {
        "temperature": temperature_data["Value"],
        "humidity": humidity_data,
        "wind_speed": wind_speed_data["Value"],
        "precipitation_probability": precipitation_probability,
    }
    json_result = json.dumps(result, indent=4)
    return json_result


if __name__ == "__main__":
    # Тестовые запросы, чтобы проверить работоспособность API

    # Тестовый запрос для места "Екатеринбург"
    forecast_data_json = get_forecast_data_by_geo_position(56.837864, 60.594882)
    print(forecast_data_json)

    # Тестовый запрос для места "Москва, Измайлово Гамма"
    forecast_data_json = get_forecast_data_by_geo_position()
    print(forecast_data_json)