from os import getenv, urandom
import requests
from dotenv import load_dotenv
from flask import Flask, abort, render_template, session, redirect, url_for, request
from extras import carregar_configuracoes

app = Flask(__name__)
app.secret_key = urandom(16)
confg = carregar_configuracoes()
load_dotenv()
ip_api = getenv('IP_API')


@app.route('/')
def index():
    response = requests.get(f"http://{ip_api}/api/posts", timeout=5)
    if response.status_code == 200:
        posts = response.json()
        return render_template('index.html', posts=posts), 200
    else:
        abort(500)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index')), 302

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            return render_template('login.html', error='Credenciais não podem estar em branco!'), 401

        dados = {'username': username, 'password': password}

        try:
            response = requests.post(f"http://{ip_api}/api/login", json=dados, timeout=5)
            if response.status_code == 200:
                session['username'] = username
                return redirect(url_for('index')), 302
            else:
                return render_template('login.html', error='Credenciais inválidas!'), 401

        except requests.Timeout:
            abort(500)
        except requests.exceptions.ConnectionError:
            abort(500)
        except requests.exceptions.RequestException:
            abort(500)

    return render_template('login.html'), 200

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
        return redirect(url_for('login')), 302
    else:
        return redirect(url_for('index')), 302


@app.errorhandler(404)
def not_found(error):
    return render_template('error/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error/500.html'), 500


if __name__ == '__main__':
    debug = confg['informacao_server']['debug']
    host = confg['informacao_server']['host']
    port = confg['informacao_server']['port']
    app.run(debug=debug, host=host, port=port)
