SHOW DATABASES;

CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha VARCHAR(255)NOT NULL,
    ativo TINYINT(1) NOT NULL DEFAULT 1,
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cliente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) UNIQUE,
    telefone VARCHAR(20),
    email VARCHAR(150),
    endereco VARCHAR(255),
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE carro (
    id INT AUTO_INCREMENT PRIMARY KEY,
    placa VARCHAR(10) NOT NULL UNIQUE,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(100) NOT NULL,
    ano YEAR,
    cor VARCHAR(30),
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE servico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    ativo TINYINT(1) NOT NULL DEFAULT 1
);

CREATE TABLE ordem_servico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    carro_id INT NOT NULL,
    status ENUM('aberta', 'em_andamento', 'concluida', 'cancelada') NOT NULL DEFAULT 'aberta',
    observacoes TEXT,
    valor_total DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_os_cliente FOREIGN KEY (cliente_id) REFERENCES cliente (id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_os_carro   FOREIGN KEY (carro_id) REFERENCES carro (id)   ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE os_servico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ordem_servico_id INT NOT NULL,
    servico_id INT NOT NULL,
    quantidade INT NOT NULL DEFAULT 1,
    preco_unitario DECIMAL(10, 2)  NOT NULL,

    CONSTRAINT fk_osserv_os      FOREIGN KEY (ordem_servico_id) REFERENCES ordem_servico (id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_osserv_servico FOREIGN KEY (servico_id) REFERENCES servico (id) ON UPDATE CASCADE ON DELETE RESTRICT
);

INSERT INTO usuario (nome, email, senha) VALUES ('Administrador', 'admin@oficina.estacio.com', 'admin123');

-- Serviços de exemplo
INSERT INTO servico (nome, descricao, preco) VALUES ('Troca de óleo',       'Troca de óleo do motor + filtro',          80.00), 
('Alinhamento',         'Alinhamento das quatro rodas',             120.00),
('Balanceamento',       'Balanceamento das quatro rodas',            80.00),
('Revisão geral',       'Revisão completa do veículo',              350.00),
('Troca de pastilhas',  'Troca das pastilhas de freio dianteiras',  200.00);
    
SHOW TABLES;

SELECT * FROM usuario;