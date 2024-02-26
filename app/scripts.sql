-- Cria a tabela de clientes
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    limite INTEGER,
    saldo INTEGER
);

-- Insere os clientes iniciais
INSERT INTO clientes (id, limite, saldo) VALUES 
    (1, 100000, 0),
    (2, 80000, 0),
    (3, 1000000, 0),
    (4, 10000000, 0),
    (5, 500000, 0);

CREATE TABLE transacoes (
    id SERIAL PRIMARY KEY,
    id_cliente INTEGER,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id),
    data_extrato TIMESTAMP,
    tipo CHAR,
    valor INTEGER,
    descricao VARCHAR(10)
)