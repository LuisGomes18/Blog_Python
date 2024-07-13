from yaml import safe_load, YAMLError


def carregar_configuracoes():
    try:
        with open('config/config.yaml', 'r', encoding='utf-8') as f:
            return safe_load(f)
    except YAMLError:
        raise YAMLError('Erro ao ler o arquivo config.yml')
    except FileNotFoundError:
        raise FileNotFoundError('Arquivo config.yml não encontrado')
    except Exception as e:
        raise Exception(f'Erro ao ler o arquivo config.yml: {e}')
