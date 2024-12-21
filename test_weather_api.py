import weather_api
import json

if __name__ == "__main__":
    # Тестовые запросы, чтобы проверить работоспособность API

    # Тестовый запрос, чтобы получить ключ локации для города "Москва"
    location_key = weather_api.get_location_key_by_city_name("Москва")
    print("Ключ локации для города Москва:", location_key)

    # Тестовый запрос для места "Екатеринбург"
    location_key = weather_api.get_location_key_by_geo_position(56.837864, 60.594882)
    print("Прогноз погоды в Екатеринбурге")
    forecast_data_json = weather_api.get_forecast_data_by_location_key(location_key)
    print(forecast_data_json)

    # Тестовый запрос для места "Москва, Измайлово Гамма"
    location_key = weather_api.get_location_key_by_geo_position(55.791749, 37.748619)
    print("Прогноз погоды в Москве, Измайлово Гамма")
    forecast_data_json = weather_api.get_forecast_data_by_location_key(location_key)
    print(forecast_data_json)

    # Тестовый запрос для места с температурой больше 35 градусов
    # (температура может меняться, на момент написания кода - где-то в Африке больше 35 градусов)
    location_key = weather_api.get_location_key_by_geo_position(10.093611, 27.863056)
    forecast_data_json = weather_api.get_forecast_data_by_location_key(location_key)
    print("Прогноз погоды в Африке")
    print(forecast_data_json)
    dict_data = json.loads(forecast_data_json)
    print("Результат для места с температурой больше 35 градусов:", weather_api.check_bad_weather(**dict_data))

    # Тестовый запрос для места с температурой меньше 0 градусов
    # (температура может меняться, на момент написания кода - в Норильске меньше 0 градусов)
    location_key = weather_api.get_location_key_by_geo_position(69.343985, 88.210393)
    forecast_data_json = weather_api.get_forecast_data_by_location_key(location_key)
    print("Прогноз погоды в Норильске")
    print(forecast_data_json)
    dict_data = json.loads(forecast_data_json)
    print("Результат для места с температурой меньше 0 градусов:", weather_api.check_bad_weather(**dict_data))