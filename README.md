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

## 🔍 Testar a Comunicação

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

Saída esperada:
```
{"status": "dados inseridos!"}
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

Saída esperada:
```json
{"usuarios": [[1, "Lucas"], [2, "Maria"], [3, "João"]]}
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
* Ambiente:

  * `POSTGRES_USER=user`
  * `POSTGRES_PASSWORD=secret`
  * `POSTGRES_DB=meubanco`

### 3. Cache (Redis)

* Utilizado para simples teste de escrita/leitura.

## Como rodar o projeto

1. No diretório raiz do projeto, execute:

```bash
docker-compose up --build
```

2. Acesse a aplicação:

👉 [http://localhost:5000](http://localhost:5000)

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