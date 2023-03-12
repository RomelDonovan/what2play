from flask import Flask, render_template
import requests
import json
import random
from config import API, ID

app = Flask(__name__)

def retrieve_data():
    resp = requests.get(API)
    data = json.loads(resp.text)
    return data


def parse_data(data):
    info = data["applist"]["apps"]
    random.shuffle(info)
    games = info[:49]

    game_ids = []
    for id in games:
        game_ids.append(id["appid"])
    return game_ids

def get_data(appids):
    game_info = []
    
    for id in appids:
        resp = requests.get(f"https://store.steampowered.com/api/appdetails?appids={id}")
        urls = f"https://store.steampowered.com/app/{id}"
        data = json.loads(resp.text)

        if data[str(id)]["success"] == False:
            continue

        elif data[str(id)]["data"]["type"] == "game":
            names = data[str(id)]["data"]["name"]
            imgs = data[str(id)]["data"]["header_image"]
            details = data[str(id)]["data"]["short_description"]
            ids = str(id)

            # names = names[:29]
            # details = details[:29]
            # imgs = imgs[:29]

            game_info.append({"name":names,"img":imgs,"detail":details,"url":urls,"id":ids})

        else:
            pass

    return game_info

def review_rate(appid):
    review_data = []
    rating = []

    for id in appid:
        url= requests.get(f"https://store.steampowered.com/appreviews/{id}?json=1")
        data = json.loads(url.text)
        review_data.append(data)
        pos = data["query_summary"]["total_positive"] 
        neg = data["query_summary"]["total_negative"]
        total = data["query_summary"]["total_reviews"]

        rate = pos == 0 or pos / total * 100

        if rate == True:
            rating.append("Unrated")

        elif rate >= 1 and rate <= 19:
            rating.append("1")

        elif rate >= 20 and rate <= 44:
            rating.append("2")

        elif rate >= 45 and rate <= 64:
            rating.append("3")
        
        elif rate >= 65 and rate <= 84:
            rating.append("4")
        elif rate >= 85 and rate <= 100:
            rating.append("5")

    return rating

@app.route("/")
def index():
    data = retrieve_data()
    appids = parse_data(data)
    get_data(appids)
    review_rate(appids)
    return render_template("app.html", data=zip(get_data(appids),review_rate(appids)))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
    


if __name__ == "__main__":
    app.run(debug=True)