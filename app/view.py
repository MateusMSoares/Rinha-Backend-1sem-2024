from flask import Flask
from controller import realizar_transacao, obter_extrato

app = Flask(__name__)

@app.route('/clientes/<int:id>/transacoes', methods=['POST'])
def transacao(id):
    return realizar_transacao(id)

@app.route('/clientes/<int:id>/extrato', methods=['GET'])
def extrato(id):
    return obter_extrato(id)

if __name__ == '__main__':
    app.run(debug=True)