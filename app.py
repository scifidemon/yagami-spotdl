import os
from flask import Flask, request, redirect, url_for, render_template, send_file, send_from_directory, make_response
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
import shutil

app = Flask(__name__)


def link_verify(url):
    if "open.spotify.com/track" in url:
        return True

@app.route('/', methods=['GET', 'POST'])

def post_link():

    if request.method == 'POST':
        cmd = ''
        TEMP_DIR = "spotdl/"
        shutil.rmtree(TEMP_DIR, ignore_errors=True)
        if not os.path.exists(TEMP_DIR):
            os.makedirs(TEMP_DIR)


        data = dict(request.form)
        print(data)
        url = data['url']
        cmd = f"spotdl --song {url} -f {TEMP_DIR}"
        if cmd:
            os.system(cmd)
            if not os.path.lexists(TEMP_DIR):
                print("Download Failed")
            if os.path.lexists(TEMP_DIR):
                for track in os.listdir(TEMP_DIR):
                    track_loc = TEMP_DIR + track
                response = send_from_directory(TEMP_DIR, track, as_attachment=True)
                response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                response.headers['Pragma'] = 'no-cache'
                response.headers['Expires'] = 0
                return response

        
    if request.method == 'GET':
        return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)