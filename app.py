from flask import Flask, render_template
import requests
import json
import random
import time
from config import API_URL, DETAILS_URL, GAME_LIMIT, STEAM_LINK, GAME_REVIEW

app = Flask(__name__)

def retrieve_data():
    try:
        resp = requests.get(API_URL)
        data = json.loads(resp.text)
        return data
    except Exception as e:
        print(f"Unable to retrieve data from API. Exception: {e}")

def get_data(game_data):
    games = []
    game_info = game_data["applist"]["apps"]
    random.shuffle(game_info)

    for data in game_info:
        id = data["appid"]
        resp = requests.get(DETAILS_URL.format(id))
        game_details = json.loads(resp.text)
        steam_url = STEAM_LINK.format(id)
        game = game_details[str(id)]
        

        if game["success"] == False:
            time.sleep(5)
            continue

        elif game["data"]["type"] == "game":
            name = game["data"]["name"]
            img = game["data"]["header_image"]
            detail = game["data"]["short_description"]
            review = get_review(id)
            games.append({"name":name, "img":img, "detail":detail, "url":steam_url, "id":str(id), "review":review})
            if len(games) == GAME_LIMIT:
                
                break
        
    return games

def get_review(appid):
    url= requests.get(GAME_REVIEW.format(appid))
    data = json.loads(url.text)
    pos = data["query_summary"]["total_positive"] 
    total = data["query_summary"]["total_reviews"]

    if not pos or not total:
        return None
        
    rating = round(pos / total * 100)

    if rating >= 1 and rating <= 19:
        stars = 1
    elif rating >= 20 and rating <= 44:
        stars = 2
    elif rating >= 45 and rating <= 64:
        stars = 3
    elif rating >= 65 and rating <= 84:
        stars = 4
    elif rating >= 85 and rating <= 100:
            stars = 5

    return stars

@app.route("/")
def index():
    data = retrieve_data()
    games = get_data(data)
    return render_template("app.html", games=games)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
    


if __name__ == "__main__":
    app.run(debug=True)