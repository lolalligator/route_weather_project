import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
from weather_api import get_location_key_by_city_name, get_several_days_forecast_by_location_key

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Прогноз погоды на маршруте", style={"textAlign": "center"}),

    html.Div([
        html.Label("Введите маршрут (разделяйте города запятыми):"),
        dcc.Input(
            id="route-input",
            type="text",
            placeholder="например: Москва, Санкт-Петербург, Казань",
            style={"width": "60%"}
        ),
        html.Br(),
        html.Label("Выбери продолжительность прогноза:"),
        dcc.Dropdown(
            id="forecast-duration",
            options=[
                {"label": "1 день", "value": 1},
                {"label": "2 дня", "value": 2},
                {"label": "3 дня", "value": 3},
                {"label": "4 дня", "value": 4},
                {"label": "5 дней", "value": 5},
            ],
            value=3,
            style={"width": "30%"}
        ),
        html.Br(),
        html.Label("Выберите параметры прогноза погоды, которые нужно отобразить:"),
        dcc.Checklist(
            id="weather-parameters",
            options=[
                {"label": "Температура (°C)", "value": "temperature"},
                {"label": "Влажность (%)", "value": "humidity"},
                {"label": "Скорость ветра (км/ч)", "value": "wind_speed"},
                {"label": "Вероятность осадков (%)", "value": "precipitation_probability"},
            ],
            value=["temperature", "humidity", "wind_speed", "precipitation_probability"],
            inline=True
        ),
        html.Br(),
        html.Button("Получить прогноз!", id="submit-button", n_clicks=0),
    ], style={"marginBottom": "20px"}),

    html.Div(id="error-message", style={"color": "red", "textAlign": "center"}),

    dcc.Graph(id="route-map"),
    html.Div(id="forecast-graphs-container")
])


@app.callback(
    [
        Output("route-map", "figure"),
        Output("forecast-graphs-container", "children"),
        Output("error-message", "children"),
    ],
    [
        Input("submit-button", "n_clicks")
    ],
    [
        State("route-input", "value"),
        State("forecast-duration", "value"),
        State("weather-parameters", "value"),
    ]
)
def update_forecast(n_clicks, route_input, forecast_duration, selected_parameters):
    if n_clicks == 0 or not route_input:
        return {}, {}, "Введите маршрут для отображения графиков прогноза погоды."

    cities = [city.strip() for city in route_input.split(",")]
    if not cities:
        return {}, {}, "Пожалуйста, введите хотя бы один город."

    all_weather_data = []
    map_points = []

    parameter_display_names = {
        "temperature": "Температура (°C)",
        "humidity": "Влажность (%)",
        "wind_speed": "Скорость ветра (км/ч)",
        "precipitation_probability": "Вероятность осадков (%)",
    }

    size_arg_priority = ["humidity", "wind_speed", "precipitation_probability"]
    size_arg = None
    for arg in size_arg_priority:
        if arg in selected_parameters:
            size_arg = parameter_display_names[arg]
            break

    route_coords = []
    for city in cities:
        result_location_key = get_location_key_by_city_name(city, return_geo=True)
        if not result_location_key:
            return {}, {}, f"Не смог получить ключ локации для города {city}."
        location_key, geo_data = result_location_key
        if not location_key:
            return {}, {}, f"Не смог получить ключ локации для города {city}."

        weather_data = get_several_days_forecast_by_location_key(location_key, days=forecast_duration)
        if not weather_data:
            return {}, {}, f"Не смог получить данные о погоде для города {city}."

        all_weather_data.append((city, weather_data, geo_data))
        route_coords.append((geo_data["latitude"], geo_data["longitude"]))
        map_points.append({
            "Город": city,
            "lat": geo_data["latitude"],
            "lon": geo_data["longitude"],
            "Температура (°C)": round(weather_data[0]["temperature"], 2),
            "Влажность (%)": round(weather_data[0]["humidity"], 2),
            "Скорость ветра (км/ч)": round(weather_data[0]["wind_speed"], 2),
            "Вероятность осадков (%)": round(weather_data[0]["precipitation_probability"], 2),
        })

    map_figure = px.scatter_mapbox(
        map_points,
        lat="lat",
        lon="lon",
        hover_name="Город",
        hover_data={parameter_display_names[param]: True for param in selected_parameters},
        color="Температура (°C)",
        size=size_arg,
        size_max=20,
        zoom=4,
        title="Маршрутная карта с данными о погоде (наведись на город, чтобы увидеть прогноз)",
    )

    # Добавляем линию маршрута на карту
    route_line = {
        "type": "scattermapbox",
        "lat": [coord[0] for coord in route_coords],
        "lon": [coord[1] for coord in route_coords],
        "mode": "lines",
        "line": {"width": 3, "color": "blue"},
        "name": "Route",
    }
    map_figure.add_trace(route_line)

    map_figure.update_layout(mapbox_style="open-street-map",
                             showlegend=False)

    # Строим графики с параметрами погоды
    forecast_graphs = []
    for param in selected_parameters:
        forecast_data = []
        for city, weather_data, _ in all_weather_data:
            for day, daily_forecast in enumerate(weather_data, start=1):
                forecast_data.append({
                    "Город": city,
                    "День": f"День {day}",
                    "Значение": daily_forecast[param],
                })

        forecast_graph = px.line(
            forecast_data,
            x="День",
            y="Значение",
            color="Город",
            labels={"Значение": parameter_display_names[param]},
            title=f"Параметр прогноза погоды: {parameter_display_names[param]}",
            markers=True,
        )

        forecast_graphs.append(dcc.Graph(figure=forecast_graph))

    return map_figure, forecast_graphs, ""


if __name__ == "__main__":
    app.run_server(debug=True)
