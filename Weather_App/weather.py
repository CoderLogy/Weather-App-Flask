import requests
from flask import Flask,render_template,request
import os

app = Flask(__name__)

@app.route("/",methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/weather",methods=['POST'])
def get_weather():
    city = request.form["city"]
    api = os.getenv("API_KEY")
    url = f"https://api.weatherapi.com/v1/current.json?key={api}&q={city}"
    response = requests.get(url)
    data = response.json()
    temperature = data["current"]["temp_c"]
    description = data["current"]["condition"]["text"]
    icon = data["current"]["condition"]["icon"]
    location = data["location"]["name"]
    return render_template("index.html",temperature=temperature,description=description,icon = icon,location = location)

@app.errorhandler(KeyError)
def handle_key_error(error):    
    if str(error) == "'current'":
        error_message = "Enter the right name of city"
    
    else:
        error_message = "Key Error: Other key error occurred."
    
    return render_template("index.html", error_message=error_message), 500
