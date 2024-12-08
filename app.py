import json

from flask import Flask, request, render_template, jsonify, make_response
import weather_api

app = Flask(__name__)


# Тестовая страница для проверки корректности создания flask-приложения
@app.route('/hello_world', methods=["GET"])
def hello_world():
    return 'Hello, World!'


# Основная страница для получения прогноза погоды на маршруте
@app.route("/", methods=["GET", "POST"])
def check_weather_on_the_route():
    # Обработка GET-запроса
    try:
        if request.method == "GET":
            return render_template("weather_check.html")
        # Обработка POST-запроса
        else:
            start_city = request.form["start_city"]
            end_city = request.form["end_city"]

            # Получаем ключи локации для обоих городов
            start_city_location_key = weather_api.get_location_key_by_city_name(start_city)
            end_city_location_key = weather_api.get_location_key_by_city_name(end_city)

            # Обработка ошибки, когда не удалось получить хотя бы один из ключей
            if not start_city_location_key or not end_city_location_key:
                return """Не смог найти ключ локации для введенных городов. 
Перепроверьте корректность введенных городов. Если вы уверены, что ошибки нет, значит ошибка при запросе к API погоды."""

            # Получаем прогноз погоды для обоих городов
            start_city_forecast = weather_api.get_forecast_data_by_location_key(start_city_location_key)
            end_city_forecast = weather_api.get_forecast_data_by_location_key(end_city_location_key)

            # Обработка ошибки, когда не удалось получить хотя бы один из прогнозов погоды
            if not start_city_forecast or not end_city_forecast:
                return "Не смог получить прогноз погоды. Вероятнее всего, не смог получить доступ к API."

            # На основе прогноза погоды строим оценку
            start_city_estimation = weather_api.check_bad_weather(**json.loads(start_city_forecast))
            end_city_estimation = weather_api.check_bad_weather(**json.loads(end_city_forecast))

            # Если хотя бы в одном из городов плохая погода, то оценка будет "Плохая погода"
            estimation = start_city_estimation or end_city_estimation
            if estimation:
                estimation_message = "На маршруте ожидается плохая погода"
            else:
                estimation_message = "На маршруте ожидается хорошая погода"
            return render_template("result.html", start_city_forecast=start_city_forecast,
                                   end_city_forecast=end_city_forecast, estimation_message=estimation_message)
    except Exception as e:
        print(repr(e))
        return make_response(jsonify({'error': 'Ошибка сервера'}), 500)


if __name__ == "__main__":
    app.run(debug=True)
