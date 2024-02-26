import psycopg2
from psycopg2 import sql

class Cliente:
    def __init__(self, id, limite, saldo):
        self.id = id
        self.limite = limite
        self.saldo = saldo

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

class Transacao:
    def __init__(self, valor, tipo, descricao, data):
        self.valor = valor
        self.tipo = tipo
        self.descricao = descricao
        self.data = data

# Conexão com o banco de dados
conn = psycopg2.connect(
    dbname="rinha",
    user="postgres",
    password="root",
    host="localhost"
)

conn.autocommit = True  # Para que as alterações sejam aplicadas automaticamente

def tabelas_existem():
    with conn.cursor() as cur:
        cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'clientes')")
        clientes_existem = cur.fetchone()[0]
        cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'transacoes')")
        transacoes_existem = cur.fetchone()[0]
    return clientes_existem and transacoes_existem

print(f"Tabelas existem:  {tabelas_existem()}")

def criar_tabelas():
    if not tabelas_existem():
        with conn.cursor() as cur:
            cur.execute(open("scripts.sql", "r").read())

# Chamar a função para criar as tabelas ao iniciar a aplicação
criar_tabelas()