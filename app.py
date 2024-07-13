from os import urandom
from flask import Flask, render_template
from extras import carregar_configuracoes


app = Flask(__name__)
app.secret_key = urandom(16)
confg = carregar_configuracoes()


@app.route('/')
def index():
    return render_template('index.html'), 200


if __name__ == '__main__':
    debug = confg['informacao_server']['debug']
    host = confg['informacao_server']['host']
    port = confg['informacao_server']['port']
    app.run(debug=debug, host=host, port=port)
