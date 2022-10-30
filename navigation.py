import requests, json
from key import API_SECRET_KEY
from forms import LoginForm, RegisterForm, RouteForm, DeleteForm
from models import db, connect_db, User, Route 

def api_details(start, end):

    data = requests.get(f"http://www.mapquestapi.com/directions/v2/route?key={API_SECRET_KEY}&from={start}&to={end}")
    data_text = data.text
    parsed_json = json.loads(data_text)
    distance = parsed_json['route']['distance']
    distance_rounded = round(distance, 2)


    return distance_rounded


def rate_multipler(distance, travel_type):

    if travel_type == "Business":
        exp = distance * 0.625
    if travel_type == "Medical/Moving":
        exp = distance * 0.22
    if travel_type == "Charitable":
        exp = distance * 0.14

    rounded_exp = round(exp, 2)

    return rounded_exp






