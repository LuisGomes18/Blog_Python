from os import getenv, urandom
import requests
from dotenv import load_dotenv
from flask import Flask, abort, render_template, session, redirect, url_for, request
from extras import carregar_configuracoes, gerar_id_post

app = Flask(__name__)
app.secret_key = urandom(16)
confg = carregar_configuracoes()
load_dotenv()
ip_api = getenv('IP_API')


@app.route('/')
def index():
    try:
        response = requests.get(f"http://{ip_api}/api/posts", timeout=5)
        response.raise_for_status()
        posts = response.json()
    except (requests.Timeout, requests.exceptions.RequestException):
        abort(500)

    if 'username' in session:
        username = session.get('username')
        return render_template('index.html', posts=posts, username=username), 200
    else:
        return render_template('index.html', posts=posts), 200


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
            response.raise_for_status()
            session['username'] = username
            return redirect(url_for('index')), 302
        except requests.exceptions.HTTPError:
            return render_template('login.html', error='Credenciais inválidas!'), 401
        except (requests.Timeout, requests.exceptions.RequestException):
            abort(500)

    return render_template('login.html'), 200


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'username' in session:
        return redirect(url_for('index')), 302

    if request.method == 'POST':
        username = request.form['username']
        primeiro_nome = request.form['primeiro_nome']
        ultimo_nome = request.form['ultimo_nome']
        genero = request.form['genero']
        data_nascimento = request.form['data_nascimento']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return render_template('signup.html', error='As senhas não coincidem'), 401

        if not all([username, primeiro_nome, ultimo_nome, genero, data_nascimento, email, password, confirm_password]):
            return render_template('signup.html', error='Credenciais não podem estar em branco!'), 401

        dados = {
            'username': username,
            'primeiro_nome': primeiro_nome,
            'ultimo_nome': ultimo_nome,
            'genero': genero,
            'data_nascimento': data_nascimento,
            'email': email,
            'password': password
        }

        try:
            response = requests.post(f"http://{ip_api}/api/signup", json=dados, timeout=5)
            response.raise_for_status()
            session['username'] = username
            return redirect(url_for('login')), 302
        except requests.exceptions.HTTPError:
            return render_template('signup.html', error='Credenciais inválidas!'), 401
        except (requests.Timeout, requests.exceptions.RequestException):
            abort(500)

    return render_template('signup.html'), 200


@app.route('/criar_post', methods=['GET', 'POST'])
def criar_post():
    if 'username' not in session:
        return redirect(url_for('login')), 302

    id_post = gerar_id_post()
    username = session["username"]

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')

        if not titulo or not descricao:
            return render_template('criar_post.html', error='Informações do post não podem estar em branco!'), 401

        dados = {
            'id': id_post,
            'titulo': titulo, 
            'descricao': descricao,
            'username': username
        }

        try:
            response = requests.post(f"http://{ip_api}/api/criar_post", json=dados, timeout=5)
            response.raise_for_status()
            return redirect(url_for('index')), 302
        except requests.exceptions.HTTPError:
            return render_template('criar_post.html', error='Erro ao criar post!'), 500
        except (requests.Timeout, requests.exceptions.RequestException) as e:
            return render_template('criar_post.html', error=str(e)), 500

    return render_template('criar_post.html', id=id_post), 200


@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
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
