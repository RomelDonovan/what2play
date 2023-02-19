from flask import Flask, render_template
import requests
import json
import random

app = Flask(__name__)

def retrieve_data():
    resp = requests.get("http://api.steampowered.com/ISteamApps/GetAppList/v0002/?format=json")
    data = json.loads(resp.text)
    return data


def parse_data(data):
    info = data['applist']['apps']
    random.shuffle(info)
    games = info[:69]

    game_ids = []
    for id in games:
        game_ids.append(id['appid'])
    return game_ids


@app.route('/')
def index():
    data = retrieve_data()
    appids = parse_data(data)

    game_data = []
    game_names = []
    game_imgs = []
    game_urls = []
    game_details = []

    for id in appids:
        resp = requests.get(f"https://store.steampowered.com/api/appdetails?appids={id}")
        url = f'https://store.steampowered.com/app/{id}'
        data = json.loads(resp.text)
        game_urls.append(url)
        game_data.append(data)

        if data[str(id)]['success'] == False:
            pass

        elif data[str(id)]['data']['type'] == 'game':
            name = data[str(id)]['data']['name']
            img = data[str(id)]['data']['header_image']
            detail = data[str(id)]['data']['short_description']
            game_names = game_names[:29]
            game_details = game_details[:29]
            game_imgs = game_imgs[:29]
            game_details.append(detail)
            game_names.append(name)
            game_imgs.append(img)
        else:
            pass

    return render_template('basic.html', game_info=zip(game_names,game_imgs,game_urls,game_details))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    


if __name__ == '__main__':
    # index()
    app.run(debug=True)