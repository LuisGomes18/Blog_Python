from os import urandom
from random import randint
import time
from datetime import datetime
import mysql.connector
from flask import Flask, jsonify, request, abort
from werkzeug.security import generate_password_hash, check_password_hash
from extras import carregar_configuracoes, conectar_banco_de_dados, gerar_id_conta, gerar_data


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
    status_message = {'message': 'API Rodando normalmente', 'uptime': f'A API está rodando há {uptime_seconds} segundos.'}
    if internal_errors:
        status_message['internal_errors'] = internal_errors
    return jsonify(status_message), 200



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


@app.route('/api/criar_posts', methods=['POST'])
def criar_posts():
    data = request.get_json()

    required_fields = ['titulo', 'descricao', 'username', 'id']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({'message': f'Campos faltando: {", ".join(missing_fields)}'}), 400

    id = data['id']
    titulo = data['titulo']
    descricao = data['descricao']
    username = data['username']
    data_atual = gerar_data()

    try:
        connection = conectar_banco_de_dados()
        cursor = connection.cursor()
        query = "INSERT INTO posts (id, titulo, descricao, data, data_modificacao, modificado, autor_post) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (id, titulo, descricao, data_atual, None, 0, username))
        connection.commit()
        return jsonify({'message': 'Post criado com sucesso'}), 201
    except mysql.connector.Error as err:
        connection.rollback()
        return jsonify({'message': f'Erro com MySQL: {err}'}), 500

    except Exception as e:
        connection.rollback()
        return jsonify({'message': f'Erro ao registrar: {e}'}), 500

    finally:
        cursor.close()
        connection.close()


@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()

    # Verificar se todos os campos necessários estão presentes
    required_fields = ['username', 'primeiro_nome', 'ultimo_nome', 'genero', 'data_nascimento', 'email', 'password']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return jsonify({'message': f'Campos faltando: {", ".join(missing_fields)}'}), 400

    username = data['username']
    primeiro_nome = data['primeiro_nome']
    ultimo_nome = data['ultimo_nome']
    genero = data['genero']
    data_nascimento = data['data_nascimento']
    email = data['email']
    password = data['password']

    # Validar e formatar os dados, se necessário
    if len(password) < 6:
        return jsonify({'message': 'A senha deve ter pelo menos 6 caracteres'}), 400

    hashed_password = generate_password_hash(password)
    user_id = gerar_id_conta()

    try:
        connection = conectar_banco_de_dados()
        cursor = connection.cursor(dictionary=True)
        query = """
            INSERT INTO login (id, username, primeiro_nome, ultimo_nome, genero, data_nascimento, email, password, nivel_acesso)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, username, primeiro_nome, ultimo_nome, genero, data_nascimento, email, hashed_password, 0))
        connection.commit()
        return jsonify({'message': 'Registro bem-sucedido'}), 201

    except mysql.connector.Error as err:
        connection.rollback()
        return jsonify({'message': f'Erro com MySQL: {err}'}), 500

    except Exception as e:
        connection.rollback()
        return jsonify({'message': f'Erro ao registrar: {e}'}), 500

    finally:
        cursor.close()
        connection.close()


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    connection = conectar_banco_de_dados()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM login WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    if user and check_password_hash(user['password'], password):
        return jsonify({'message': 'Login bem-sucedido'}), 200
    else:
        return jsonify({'message': 'Credenciais inválidas'}), 401


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
