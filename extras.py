from yaml import safe_load, YAMLError


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
        with open('config/config.yaml', 'r', encoding='utf-8') as f:

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
