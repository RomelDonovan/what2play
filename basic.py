from flask import Flask, render_template, request
from pip._vendor import requests
import json , random

app = Flask(__name__)

def retrieve_data():
    resp = requests.get("http://api.steampowered.com/ISteamApps/GetAppList/v0002/?format=json")
    data = json.loads(resp.text)
    return data


def parse_data(data):
    info = data['applist']['apps']
    random.shuffle(info)
    games = info[:1]

    game_id = []
    for id in games:
        game_id.append(id['appid'])
        appid = ' '.join(str(appid) for appid in game_id)
        print(appid)
    return appid


def new_request(appid):
    resp = requests.get(f"https://store.steampowered.com/api/appdetails?appids={appid}")
    ndata = json.loads(resp.text)
    # print(ndata)
    return ndata

def new_parse(desc,appid):
    name = desc[str(appid)]['data']['name']
    detail = desc[str(appid)]['data']['short_description']
    img = desc[str(appid)]['data']['header_image']
    return img, name, detail
    print(img)
    print(name)
    print(detail)

@app.route('/')
def index():
    data = retrieve_data()
    appid = parse_data(data)
    desc = new_request(appid)
    game = new_parse(desc, appid)

    return render_template('basic.html', game = game)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    


if __name__ == '__main__':
    app.run(debug=True)