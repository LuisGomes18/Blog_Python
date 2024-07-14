from os import urandom
import time
from datetime import datetime
from flask import Flask, jsonify, request, abort
from extras import carregar_configuracoes, conectar_banco_de_dados


app = Flask(__name__)
app.secret_key = urandom(16)
config = carregar_configuracoes()
start_time = time.time()
internal_errors = []

def get_uptime():
    current_time = time.time()
    uptime_seconds = int(current_time - start_time)
    return uptime_seconds


@app.route('/api/status', methods=['GET'])
def index():
    uptime_seconds = get_uptime()
    status_message = {'message': 'API Rodando normalmente', 'uptime_seconds': uptime_seconds}
    if internal_errors:
        status_message['internal_errors'] = internal_errors
    return jsonify(status_message), 200

@app.route('/api/uptime', methods=['GET'])
def get_uptime_api():
    uptime_seconds = get_uptime()
    return f'A API está rodando há {uptime_seconds} segundos.'

@app.route('/api/posts', methods=['GET'])
def get_posts():
    connection = conectar_banco_de_dados()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(posts), 200

@app.route('/api/post', methods=['GET'])
def get_post():
    id = request.args.get('id')
    connection = conectar_banco_de_dados()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()
    cursor.close()
    connection.close()
    if post:
        return jsonify(post), 200
    else:
        abort(404)


@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Requisição inválida'}), 404

@app.errorhandler(Exception)
def handle_exception(error):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_message = f'Erro em {now}: {str(error)}'
    internal_errors.append(error_message)
    return jsonify({'message': 'Erro interno'}), 500


if __name__ == '__main__':
    debug = config['informacao_api']['debug']
    host = config['informacao_api']['host']
    port = config['informacao_api']['port']
    app.run(debug=debug, host=host, port=port)
