from os import getenv
from random import randint
from dotenv import load_dotenv
from yaml import safe_load, YAMLError
import mysql.connector


load_dotenv()
db_host = getenv('DB_HOST')
db_user = getenv('DB_USER')
db_pass = getenv('DB_PASS')
db_name = getenv('DB_NAME')
db_config = {
    'user': db_user,
    'password': db_pass,
    'host': db_host,
    'database': 'BLOG'
}


def carregar_configuracoes():
    """
    Carrega as configurações do arquivo config/config.yaml.

    Retorna as configurações em forma de dicionário.
    Em caso de erro, lança uma exceção.

    :return: Dicionário com as configurações
    :raises YAMLError: Se houver um erro ao ler o arquivo
    :raises FileNotFoundError: Se o arquivo não for encontrado
    :raises Exception: Se houver outro erro
    """

    # Abrimos o arquivo config/config.yaml na modalidade de leitura
    try:
        with open('../config/config.yaml', 'r', encoding='utf-8') as f:

            # Utilizamos a função safe_load para ler o arquivo YAML
            # e converter as configurações em um dicionário.
            # Se houver um erro ao ler o arquivo, lança uma exceção
            # do tipo YAMLError.
            return safe_load(f)

    # Se o arquivo não for encontrado, lança uma exceção do tipo FileNotFoundError.
    except FileNotFoundError:

        # Se houver outro erro, lança uma exceção genérica com uma mensagem
        # de erro detalhada.
        raise Exception(f'Erro ao ler o arquivo config.yml: Arquivo não encontrado')

    # Se houver um erro ao ler o arquivo YAML, lança uma exceção do tipo YAMLError.
    except YAMLError:
        raise YAMLError('Erro ao ler o arquivo config.yml')

    # Se houver outro erro, lança uma exceção genérica com uma mensagem
    # de erro detalhada.
    except Exception as e:
        raise Exception(f'Erro ao ler o arquivo config.yml: {e}')


def conectar_banco_de_dados():
    conececao = mysql.connector.connect(**db_config)
    return conececao


def gerar_id_conta():
    """
    Gera um ID único para uma nova conta.

    Este método abre uma conexão com o banco de dados, cria um cursor e executa
    uma consulta para verificar se o ID gerado já existe. Caso exista, ele gera
    um novo ID até encontrar um ID único.

    :return: Um ID único para uma nova conta
    """

    # Conecta ao banco de dados
    connection = conectar_banco_de_dados()

    # Cria um cursor para executar consultas
    cursor = connection.cursor(dictionary=True)

    # Loop infinito para gerar um ID único
    while True:
        # Gera um novo ID aleatório
        id = randint(1111, 9999)

        # Executa a consulta para verificar se o ID já existe
        query = "SELECT * FROM login WHERE id = %s"
        cursor.execute(query, (id,))

        # Obtém os resultados da consulta
        conta = cursor.fetchone()

        # Verifica se o ID é único
        if not conta:
            # Se for único, sai do loop e retorna o ID
            break

    # Fecha o cursor e a conexão com o banco de dados
    cursor.close()
    connection.close()

    # Retorna o ID único gerado
    return id
