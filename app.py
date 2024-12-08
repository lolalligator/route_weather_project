from flask import Flask, request, render_template
import weather_api

app = Flask(__name__)


# Тестовая страница для проверки корректности создания flask-приложения
@app.route('/hello_world', methods=["GET"])
def hello_world():
    return 'Hello, World!'

@app.route("/", methods=["GET, POST"])
def check_weather_on_the_route():
    if request.method == "GET":
        return render_template("weather_check.html")
    else:
        start_city = request.form["start_city"]
        end_city = request.form["end_city"]

        start_city_location_key = weather_api.get_location_key_by_city_name(start_city)
        end_city_location_key = weather_api.get_location_key_by_city_name(end_city)

        if not start_city_location_key or not end_city_location_key:
            return "Не смог найти ключ локации для введенных городов. Перепроверьте корректность введенных городов."

        start_city_forecast = weather_api.get_forecast_data_by_location_key(start_city_location_key)



if __name__ == "__main__":
    app.run(debug=True)