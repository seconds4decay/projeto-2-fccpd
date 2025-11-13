# Desafio 1 — Containers em Rede

Criar dois containers que se comunicam por uma rede Docker customizada.

---

## Estrutura de Projeto

```
.
├── cliente/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
└── servidor/
    ├── app.py
    ├── requirements.txt
    ├── Dockerfile
```

---

## Criar a Rede Docker

Crie uma rede para permitir a comunicação direta entre os containers:

```bash
docker network create minha_rede
```

---

## Construir as Imagens

### Servidor Flask
Entre na pasta `servidor` e construa a imagem:

```bash
cd servidor
docker build -t flask-server .
cd ..
```

### Cliente Flask
Entre na pasta `cliente` e construa a imagem:

```bash
cd cliente
docker build -t flask-client .
cd ..
```

---

## Criar o Volume para Persistência de Logs

Crie um volume para armazenar os logs do cliente fora do container:

```bash
docker volume create cliente_logs
```

Esse volume será montado em `/app/comunicacao.log` dentro do container cliente.

---

## Rodar os Containers

### Iniciar o Servidor
Rode o container do servidor Flask conectado à rede:

```bash
docker run -d   --name server   --network minha_rede   -p 8080:8080   flask-server
```

### Iniciar o Cliente
Rode o container do cliente Flask conectado à mesma rede, com o volume de logs:

```bash
docker run -d   --name client   --network minha_rede   -p 5000:5000   -v cliente_logs:/app/comunicacao.log   flask-client
```

---

## Testar a Comunicação

Acesse o cliente Flask (porta 5000) para ver o status da última resposta recebida do servidor:

```bash
curl http://localhost:5000
```

Você deve ver algo como:

```json
{"ultima_resposta": "Hello, World!"}
```

---

## Limpeza

```bash
docker rm -f client server
docker network rm minha_rede
docker volume rm cliente_logs
```

---

# Desafio 2 — Volumes e Persistência

Demonstrar persistência de dados usando volumes Docker.

Dois containers são usados:

- db — cria o banco e insere dados.  
- leitor — lê os dados persistidos, mesmo após o container `db` ser removido.

---

## Estrutura do Projeto

```
.
├── db/
│   ├── app.py          # Cria e insere dados no SQLite
│   └── Dockerfile
├── leitor/
│   ├── app.py          # Lê dados do mesmo SQLite
│   └── Dockerfile
└── README.md
```

---

## Passo a passo

### Criar uma rede Docker

```bash
docker network create minha-rede
```

---

### Criar um volume persistente

```bash
docker volume create dados-sqlite
```

---

### Construir as imagens

```bash
docker build -t db-flask ./db
docker build -t leitor-flask ./leitor
```

---

### Rodar o container do banco

```bash
docker run -d   --name db   --network minha-rede   -p 8080:8080   -v dados-sqlite:/data   db-flask
```

---

### Inserir dados no banco

Abra no navegador ou use o `curl`:

```bash
curl http://localhost:8080
```

---

### Remover o container do banco

Agora, para demonstrar a persistência mesmo ápos a remoção do container

```bash
docker stop db
docker rm db
```

O volume `dados-sqlite` ainda contém o banco `meubanco.db`.

---

### Rodar o container leitor

```bash
docker run -d   --name leitor   --network minha-rede   -p 8081:8081   -v dados-sqlite:/data   leitor-flask
```

---

### Ler os dados persistidos

Abra no navegador ou rode:

```bash
curl http://localhost:8081
```

Mesmo após apagar o container do banco, os dados permanecem.

---

### Limpeza

Para remover tudo:

```bash
docker stop leitor
docker rm leitor
docker volume rm dados-sqlite
docker network rm minha-rede
```

---

# Desafio 3 — Docker Compose Orquestrando Serviços

Usar Docker Compose para orquestrar múltiplos serviços dependentes.

## Estrutura do projeto

```
.
├── web/
│   ├── app.py        # Aplicação Flask
│   └── Dockerfile    # Build da aplicação web
├── docker-compose.yml
└── README.md
```

## Serviços

### 1. Web (Flask)

* Conecta ao PostgreSQL e Redis para testar comunicação.
* Variáveis de ambiente:
  * `DATABASE_HOST`: endereço do banco (default: `db`)
  * `REDIS_HOST`: endereço do redis (default: `cache`)
* Exposta na porta 5000.

### 2. Banco de Dados (PostgreSQL)

* Credenciais definidas em `docker-compose.yml`
* Persistência via volume `pgdata`.

### 3. Cache (Redis)

* Utilizado para simples teste de escrita/leitura.

## Como rodar o projeto

1. No diretório raiz do projeto, execute:

```bash
docker-compose up --build
```

2. Acesse a aplicação:

[http://localhost:5000](http://localhost:5000)

## O que a aplicação faz

Ao acessar a rota `/`, a aplicação:

1. Testa conexão com o PostgreSQL e retorna sua versão.
2. Testa conexão com o Redis, grava um valor e lê novamente.

Exemplo de saída:

```
Postgres: PostgreSQL 15.3
Redis: Conexão com Redis OK!
```

## Limpeza

```bash
docker-compose down
docker-compose down -v
```

---

# Desafio 4 — Microsserviços Independentes

## Objetivo
Criar dois microsserviços independentes que se comunicam via HTTP.

---

## Estrutura do Projeto

```
service_a/
├── app.py
└── Dockerfile

service_b/
├── app.py
└── Dockerfile
```

---

## Descrição dos Serviços

### Serviço 1
- Fornece uma lista de usuários em formato JSON.

---

### Serviço B
- Consome os dados do Serviço A por HTTP Request e retorna uma lista de mensagens formatadas.

---

## Execução

### Construir e iniciar os containers
Na raiz dos serviços (`service1/`) e (`service2/`), execute o comando para buildar as imagens:

Para o service 1:
```bash
docker build -t service1 .
```

Para o service 2:
```bash
docker build -t service2 .
```

E depois, para executar os containers no mesmos diretorios:

```bash
docker run -p 5000:5000 --name service1
```

```bash
docker run -p 5001:5001 --name service2
```

Isso irá:
- Construir as imagens de ambos os microsserviços.
- Criar e iniciar os containers `service1` e `service1`.

---

## Como funciona
- Cada microsserviço possui seu Dockerfile e roda de forma independente.
- A comunicação entre eles ocorre via HTTP Request, sem gateway.

---

# Desafio 5 — Microsserviços com API Gateway

## Objetivo
Criar uma arquitetura com API Gateway centralizando o acesso a dois microsserviços.

---

## Estrutura do Projeto

```
gateway/
├── app.py
└── Dockerfile

service_users/
├── app.py
└── Dockerfile

service_orders/
├── app.py
└── Dockerfile
docker-compose.yml
```

---

## Descrição dos Serviços

### Microsserviço 1 — Usuários
- Fornece uma lista de usuários em formato JSON.  

---

### Microsserviço 2 — Pedidos
- Fornece uma lista de pedidos realizados.  

---

### API Gateway
- Centraliza o acesso aos dois microsserviços.  
- Redireciona chamadas:  
  - `/users` → Microsserviço de Usuários  
  - `/orders` → Microsserviço de Pedidos  
- Porta: `8080`

---

## Execução com Docker

### Construir e iniciar os containers
Na raiz do projeto (`desafio5/`), execute:

```bash
docker compose up --build
```

Isso irá:
- Construir as imagens dos três serviços.
- Criar containers independentes.
- Configurar a rede e as variáveis de ambiente automaticamente.

---

### Testar os serviços

#### Listar usuários (via Gateway)
```bash
curl http://localhost:8080/users
```

#### Listar pedidos (via Gateway)
```bash
curl http://localhost:8080/orders
```

Ou acesse pelo navegador:

- [http://localhost:8080/users](http://localhost:8080/users)
- [http://localhost:8080/orders](http://localhost:8080/orders)

---

## Como Funciona
- O API Gateway é o único ponto de entrada (porta 8080).  
- Ele orquestra as chamadas HTTP para cada microsserviço.  
- A comunicação é feita através da rede interna do Docker, usando os nomes dos containers.  

Exemplo de roteamento interno:
```yaml
SERVICE_USERS_URL=http://service_users:5000
SERVICE_ORDERS_URL=http://service_orders:5001
```

---