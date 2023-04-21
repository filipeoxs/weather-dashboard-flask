from flask import Flask, render_template, request
import requests
import json
import configparser


app = Flask(__name__)

class WeatherService:
    """
    Responsável por obter os dados do serviço de clima.
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    API_KEY = config['openweathermap']['api']

    def get_weather(self, city):
        """
        Obtém os dados do clima da cidade especificada.
        """
        url = f"{self.BASE_URL}?q={city}&appid={self.API_KEY}&units=metric"
        response = requests.get(url)
        data = json.loads(response.content)

        return data

class WeatherController:
    """
    Responsável por receber as requisições do usuário e entregar as respostas correspondentes.
    """

    def __init__(self, service):
        self.service = service

    def handle_request(self, request):
        """
        Lida com a requisição do usuário.
        """
        city = request.form.get("city")
        data = self.service.get_weather(city)

        return render_template("index.html", data=data)

weather_service = WeatherService()
weather_controller = WeatherController(weather_service)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        return weather_controller.handle_request(request)

if __name__ == "__main__":
    app.run(debug=True)
