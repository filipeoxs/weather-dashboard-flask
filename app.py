import configparser
import requests
from flask import Flask, render_template,request

app = Flask(__name__)

def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']

def get_weather(cep, API_KEY):
    api_call = f'http://api.openweathermap.org/data/2.5/weather?q={cep}&units=metric&appid={API_KEY}'
    r = requests.get(api_call)
    return r.json()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
   
@app.route('/results', methods=['POST','GET'])
def results():
    city=request.form['city']
    if city !='':
        data = get_weather(city, get_api_key())
        temp = "{0:.1f}".format(data["main"]["temp"])
        min_temp = "{0:.1f}".format(data["main"]["temp_min"])
        max_temp = "{0:.1f}".format(data["main"]["temp_max"])
        humidity = "{0:.0f}".format(data["main"]["humidity"])
        feels_like = "{0:.1f}".format(data["main"]["feels_like"])
        weather_description = dict(data["weather"][0])["description"]
        if request.method == 'POST':
            return render_template('results.html', temp=temp,min_temp = min_temp, max_temp = max_temp,
                                humidity=humidity, feels_like=feels_like, weather_description=weather_description,city=city)
        else:
            return render_template('index.html')
    else:
        return 'There was no city with the name informed registered in our database. Please, try again.'
if __name__ == "__main__":
    app.run(debug=True)
