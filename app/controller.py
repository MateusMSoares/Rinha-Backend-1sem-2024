from flask import request, jsonify
from model import conn
from datetime import datetime


opcoes_transacao = ['c', 'd']

def realizar_transacao(id):
    with conn.cursor() as cur:
        # Obter cliente do banco de dados
        cur.execute("SELECT id, limite, saldo FROM clientes WHERE id = %s", (id,))
        cliente = cur.fetchone()
        if not cliente:
            return jsonify({"error": "Cliente não encontrado"}), 404
        
        data = request.get_json()
        valor = data.get('valor')
        tipo = data.get('tipo')
        descricao = data.get('descricao')

        if tipo not in opcoes_transacao:
            return jsonify({"error": "Opção inválida"}), 400
        
        if len(descricao) > 10:
            return jsonify({"error": "Descrição deve ter 10 caracteres"}), 400

        cliente_id, cliente_limite, cliente_saldo = cliente  # Desempacotando os valores

        if tipo == 'd' and (cliente_saldo - valor) < -cliente_limite or tipo == "c" and (cliente_saldo - valor) < -cliente_limite:
            return jsonify({"error": "Saldo insuficiente"}), 422
        

        # Atualizar saldo do cliente no banco de dados
        novo_saldo = cliente_saldo - valor
        cur.execute("UPDATE clientes SET saldo = %s WHERE id = %s", (novo_saldo, id))

        # Inserir transação no banco de dados
        cur.execute("INSERT INTO transacoes (id_cliente, data_extrato, tipo, valor, descricao) VALUES (%s, NOW(), %s, %s, %s)", (id, tipo, valor, descricao))

        return jsonify({"limite": cliente_limite, "saldo": novo_saldo}), 200

def obter_extrato(id):
    with conn.cursor() as cur:
        # Obter cliente do banco de dados
        cur.execute("SELECT id, limite, saldo FROM clientes WHERE id = %s", (id,))
        cliente = cur.fetchone()
        if not cliente:
            return jsonify({"error": "Cliente não encontrado"}), 404
        
        cliente_id, cliente_limite, cliente_saldo = cliente 

        # Obter últimas transações do cliente do banco de dados
        cur.execute("SELECT data_extrato, tipo, valor, descricao FROM transacoes WHERE id_cliente = %s ORDER BY data_extrato DESC LIMIT 10", (id,))
        transacoes_cliente = cur.fetchall()

        saldo = {"total": cliente_saldo, 
                 "data_extrato": datetime.now(),
                 "limite": cliente_limite}

        return jsonify({"saldo": saldo, "ultimas_transacoes": transacoes_cliente}), 200
