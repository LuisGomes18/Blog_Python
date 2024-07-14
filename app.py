from os import getenv, urandom
import requests
from dotenv import load_dotenv
from flask import Flask, abort, render_template
from extras import carregar_configuracoes


app = Flask(__name__)
app.secret_key = urandom(16)
confg = carregar_configuracoes()
load_dotenv()
ip_api = getenv('IP_API')


@app.route('/')
def index():
    response = requests.get(f"http://{ip_api}/api/posts")
    if response.status_code == 200:
        posts = response.json()
        return render_template('index.html', posts=posts), 200
    else:
        abort(500)

@app.route('/login')
def login():
    return render_template('login.html'), 200


if __name__ == '__main__':
    debug = confg['informacao_server']['debug']
    host = confg['informacao_server']['host']
    port = confg['informacao_server']['port']
    app.run(debug=debug, host=host, port=port)
