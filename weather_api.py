import requests
import json
from api_key import api_key
from typing import Optional

response_lang = "ru-ru"


def get_location_key_by_geo_position(latitude: float, longitude: float) -> Optional[str]:
    """
    Получает ключ гео-позиции с сайта AccuWeather по географической широте и географической долготе

    Возвращает полученный ключ гео-позиции в формате строки
    :param latitude: Географическая широта
    :param longitude: Географическая долгота
    :return: Ключ гео-позиции с сайта AccuWeather
    """
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
    return location_key


def get_location_key_by_city_name(city_name: str) -> Optional[str]:
    """
    Получает ключ гео-позиции с сайта AccuWeather по названию города

    Возвращает полученный ключ гео-позиции в формате строки
    :param city_name: Название города
    :return: Ключ гео-позиции с сайта AccuWeather
    """
    cities_base_url = "http://dataservice.accuweather.com/locations/v1/cities/search"
    params = {
        "apikey": api_key,
        "q": city_name,
        "language": response_lang,
    }
    response = requests.get(cities_base_url, params=params)
    if response.status_code != 200:
        print(f"Ошибка при получении геолокации: {response.text}")
        return
    location_key = response.json()["Key"]
    return location_key


def get_forecast_data_by_location_key(location_key: str) -> Optional[str]:
    """Возвращает данные о дневном прогнозе погоды в локации по её ключу локации
    с сайта AccuWeather

    Ответ в формате JSON со следующими значениями:

    - temperature - Средняя дневная температура

    - humidity - Относительная влажность воздуха

    - wind_speed - Средняя дневная скорость воздуха

    - precipitation_probability - Дневная вероятность выпадения осадков

    :param location_key: Ключ локации с сайта AccuWeather
    :return: Данные о погоде в формате JSON
    """
    forecast_base_url = f"http://dataservice.accuweather.com/forecasts/v1/daily/1day/{location_key}"
    params = {
        "apikey": api_key,
        "language": response_lang,
    }
    response = requests.get(forecast_base_url, params=params)
    if response.status_code != 200:
        print(f"Ошибка при получении прогноза погоды: {response.text}")
        return
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


def check_bad_weather(temperature: float, humidity: float, wind_speed: float, precipitation_probability: float) -> bool:
    """
    Проверяет по данным из прогноза погоды (температуре, влажности, скорости ветра, вероятности осадков),
    является ли погода плохой. Возвращает True, если погода плохая и False - иначе.

    :param temperature: Температура
    :param humidity: Влажность
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
    if humidity < 30 or humidity > 80:
        return True
    return False


if __name__ == "__main__":
    # Тестовые запросы, чтобы проверить работоспособность API

    # Тестовый запрос для места "Екатеринбург"
    location_key = get_location_key_by_geo_position(56.837864, 60.594882)
    forecast_data_json = get_forecast_data_by_location_key(location_key)
    print(forecast_data_json)

    # Тестовый запрос для места "Москва, Измайлово Гамма"
    location_key = get_location_key_by_geo_position(55.791749, 37.748619)
    forecast_data_json = get_forecast_data_by_location_key(location_key)
    print(forecast_data_json)

    # Тестовый запрос для места с температурой больше 35 градусов
    # (температура может меняться, на момент написания кода - в Ботсване больше 35 градусов)
    location_key = get_location_key_by_geo_position(-24.658372, 25.912146)
    forecast_data_json = get_forecast_data_by_location_key(location_key)
    print(forecast_data_json)
    dict_data = json.loads(forecast_data_json)
    print("Результат для места с температурой больше 35 градусов:", check_bad_weather(**dict_data))

    # Тестовый запрос для места с температурой меньше 0 градусов
    # (температура может меняться, на момент написания кода - в Норильске меньше 0 градусов)
    location_key = get_location_key_by_geo_position(69.343985, 88.210393)
    print(forecast_data_json)
    dict_data = json.loads(forecast_data_json)
    print("Результат для места с температурой больше 35 градусов:", check_bad_weather(**dict_data))
