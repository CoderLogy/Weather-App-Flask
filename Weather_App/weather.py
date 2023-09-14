import requests
from flask import Flask,render_template,request
from datetime import datetime
import os


"""
    This is a Flask web application that retrieves weather data for a given city using the WeatherAPI
    and displays it on an HTML template.
    :return: The `index` function returns the rendered template "index.html". The `get_weather` function
    returns the rendered template "index.html" with the temperature, description, icon, and location
    variables passed as arguments. The `handle_key_error` function returns the rendered template
"""
app = Flask(__name__)

@app.route("/",methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/weather",methods=['POST'])
def get_weather():
    city = request.form["city"]
    api = os.getenv("API_KEY")
    url = f"https://api.weatherapi.com/v1/current.json?key={api}&q={city}&aqi=yes"
    response = requests.get(url)
    data = response.json()
    current_data = data["current"]
    location_data = data["location"]

    temperature_c = current_data["temp_c"]
    temperature_f = current_data["temp_f"]
    description = current_data["condition"]["text"]
    icon = current_data["condition"]["icon"]
    location = location_data["name"]
    country = location_data["country"]
    aqi = current_data["air_quality"]["gb-defra-index"]

    current_time = datetime.strptime(location_data["localtime"], r"%Y-%m-%d %H:%M")
    formatted_time = current_time.strftime("%H:%M")

    text1 = f"Current Weather of {location}, {country}"
    text2 = f"Temperature: {temperature_c} °C / {temperature_f} °F"
    text3 = f"Description: {description}"
    crtime = f"Current time there: {formatted_time} hours (24-hour format)"
    aqi = f"Aqi: {aqi} ( <7 very dangerous )"
    return render_template("index.html",aqi=aqi,icon=icon,text3=text3,crtime=crtime,text1=text1,text2=text2)

@app.errorhandler(KeyError)
def handle_key_error(error):    
    if str(error) == "'current'":
        error_message = "Enter the right name of city"
    
    else:
        error_message = "Key Error: Other key error occurred."
    
    return render_template("index.html", error_message=error_message), 500
