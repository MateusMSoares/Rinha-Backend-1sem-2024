from flask import Flask, request, jsonify
from datetime import datetime


app = Flask(__name__)
opcoes_transacao = ['c', 'd']
dataEhora = datetime.now()

clientes = {
    1: {"limite": 100000, "saldo": 0},
    2: {"limite": 80000, "saldo": 0},
    3: {"limite": 1000000, "saldo": 0},
    4: {"limite": 10000000, "saldo": 0},
    5: {"limite": 500000, "saldo": 0}
}

@app.route('/clientes/<int:id>/transacoes', methods=['POST'])
def realizar_transacao(id):
    if id not in clientes:
        return jsonify({"error": "Cliente não encontrado"}), 404
    
    
    data = request.get_json()
    valor = data.get('valor')
    tipo = data.get('tipo')
    descricao = data.get('descricao')

    if tipo not in opcoes_transacao:
        return jsonify({"error": "Opção inválida"}), 400
    
    if 0 < len(descricao) >= 10:
        return jsonify({"error": "Descrição deve ter 10 caracteres"}), 400

    
    if tipo == 'd' and (clientes[id]["saldo"] - valor) < -clientes[id]["limite"]:
        return jsonify({"error": "Saldo insuficiente"}), 422

    if tipo == 'c':
        clientes[id]["saldo"] += valor
    else:
        clientes[id]["saldo"] -= valor

    if "transacoes" not in clientes[id]:
        clientes[id]["transacoes"] = []


    print(clientes)
    transacao = {
    "valor": valor,
    "tipo": tipo,
    "descricao": descricao,
    "realizada_em": dataEhora
    }
    clientes[id]["transacoes"].append(transacao)

    
    return jsonify({"limite": clientes[id]["limite"], "saldo": clientes[id]["saldo"]}), 200


@app.route('/clientes/<int:id>/extrato', methods=['GET'])
def obter_extrato(id):
    if id not in clientes:
         return jsonify({"error": "Cliente não encontrado"}), 404
    
    # Obtém a lista de transações do cliente
    transacoes_cliente = clientes[id].get("transacoes", [])

    # Inverte a lista de transações para ordená-las de forma decrescente
    transacoes_cliente.reverse()

    # Limita a lista às últimas 10 transações, se houver mais do que 10 transações
    ultimas_transacoes = transacoes_cliente[:10]
 
    saldo = {"total": clientes[id]["saldo"], 
             "data_extrato": dataEhora, 
             "limite": clientes[id]["limite"]}

    return jsonify({"saldo": saldo, "ultimas_transacoes": ultimas_transacoes}), 200

if __name__ == '__main__':
    app.run(debug=True)