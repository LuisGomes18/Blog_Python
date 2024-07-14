from os import urandom
import time
from flask import Flask, jsonify, request, abort
from extras import carregar_configuracoes, conectar_banco_de_dados


app = Flask(__name__)
app.secret_key = urandom(16)
confg = carregar_configuracoes()
start_time = time.time()

def get_uptime():
    current_time = time.time()
    uptime_seconds = int(current_time - start_time)
    return uptime_seconds

@app.route('/api/status', methods=['GET'])
def index():
    return jsonify({'message': 'API Rodando normalmente'}), 200

@app.route('/api/uptime', methods=['GET'])
def get_uptime_api():
    uptime_seconds = get_uptime()
    return f'A API está rodando há {uptime_seconds} segundos.'

@app.route('/api/posts', methods=['GET'])
def get_posts():
    coneccao = conectar_banco_de_dados()
    cursor = coneccao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    cursor.close()
    coneccao.close()
    return jsonify(posts), 200

@app.route('/api/post', methods=['GET'])
def get_post():
    id = request.args.get('id')
    conexao = conectar_banco_de_dados()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()
    cursor.close()
    conexao.close()
    if post:
        return jsonify(post), 200
    else:
        abort(404)


@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Requisição inválida'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'message': 'Erro interno'}), 500


if __name__ == '__main__':
    debug = confg['informacao_api']['debug']
    host = confg['informacao_api']['host']
    port = confg['informacao_api']['port']
    app.run(debug=debug, host=host, port=port)
