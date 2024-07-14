from os import urandom
from flask import Flask, jsonify
from extras import carregar_configuracoes, conectar_banco_de_dados


app = Flask(__name__)
app.secret_key = urandom(16)
confg = carregar_configuracoes()


@app.route('/api')
def index():
    return jsonify({'message': 'API Rodando normalmente'}), 200

@app.route('/api/posts', methods=['GET'])
def get_posts():
    coneccao = conectar_banco_de_dados()
    cursor = coneccao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    cursor.close()
    coneccao.close()
    return jsonify(posts), 200


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
