from flask import Flask, render_template, jsonify, request
import json
import requests as req

app = Flask(__name__)
song_list = []

@app.route('/')
def home():
    return render_template("home.html", song_list=song_list)

@app.route('/song_search', methods=['POST'])
def song_search():
    if request.method == 'POST':
        song_list = []
        query = request.form.get('query')
        print(query)
        res_length = 20
        url=f"https://www.jiosaavn.com/api.php?p=1&q={ query.replace(' ', '+') }\%20&_format=json&_marker=0&api_version=4&ctx=wap6dot0\%20&n={res_length}&__call=search.getResults"
        data = req.get(url)
        data = json.loads(data.content)
        song_list = processor(data['results'])
        print(song_list)
        return render_template("home.html", song_list=song_list)

def processor(songs_json_list):
    songs_list = []
    for song_json in songs_json_list:
        id = song_json['id']
        url=f"https://www.jiosaavn.com/api.php?__call=song.getDetails&cc=in&_marker=0%3F_marker%3D0&_format=json&pids={id}"
        data = req.get(url)
        data = json.loads(data.content)
        song_url_pl = data[id].get('media_preview_url')
        if song_url_pl:
            song_url = song_url_pl.replace('preview.saavncdn.com', 'aac.saavncdn.com')
            song_url = song_url.replace('_96_p', '_320') 
            songs_list.append(
                {
                # "id": id,
                "name": data[id]['song'],
                "src": song_url,
                "album": data[id]['album'],
                # "album_id": data[id]['albumid'],
                "artist": data[id]['primary_artists'],
                # "duration": data[id]['duration'],
                # "year": data[id]['year'],
                "poster": data[id]['image'].replace('150x150', '500x500'),
                "lyric": " ",
                "sublyric": " "
                # "label": data[id]['label'],
                # "language": data[id]['language']
                }
                )
    return songs_list

if __name__ == '__main__':
    app.run(debug=True)