-- Cria a tabela de clientes
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    limite INTEGER NOT NULL,
    saldo INTEGER NOT NULL DEFAULT '0'
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
    id_cliente INTEGER NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id),
    realizada_em TIMESTAMP NOT NULL DEFAULT NOW(),
    tipo CHAR NOT NULL,
    valor INTEGER NOT NULL,
    descricao VARCHAR(10) NOT NULL
)