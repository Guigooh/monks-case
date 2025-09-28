# 📊 Monks Dashboard

Projeto desenvolvido para visualização de métricas a partir de arquivos CSV, com login seguro e controle de acesso por perfil de usuário (admin e user).

---

## 🚀 Tecnologias utilizadas

- **Backend:** FastAPI  
- **Frontend:** HTML, CSS, Bootstrap, JavaScript  
- **Autenticação:** JWT (JSON Web Token)  
- **Banco de Dados:** Arquivos CSV (`users.csv` e `metrics.csv`)  
- **Linguagem:** Python 3.9+  

---

## 📂 Estrutura de Pastas

```bash
monks-case/
├── backend/
│   ├── main.py          # API FastAPI
│   └── data/
│       ├── users.csv    # Usuários cadastrados
│       └── metrics.csv  # Métricas carregadas no dashboard
├── frontend/
│   ├── index.html       # Tela de login
│   └── dashboard.html   # Tela do dashboard
└── README.md
```

---

## ⚙️ Como rodar o projeto

1. **Clonar o repositório**
   ```bash
   git clone https://github.com/seu-repo/monks-case.git
   cd monks-case/backend
   ```

2. **Criar ambiente virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate    # Windows
   ```

3. **Instalar dependências**
   ```bash
   pip install fastapi uvicorn[standard] python-jose pandas
   ```

4. **Executar o servidor**
   ```bash
   uvicorn main:app --reload
   ```

👉 O servidor rodará em: [http://localhost:8000](http://localhost:8000)  
👉 Frontend disponível em: [http://localhost:8000/index.html](http://localhost:8000/index.html)

---

## 🔑 Autenticação

O login é feito com base no arquivo `users.csv`, que deve conter colunas de `username` (ou `email`), `password` e `role`.

**Exemplo de `users.csv`:**

```csv
username,password,role
useradmn,123,admin
user10,123,user
```

- **Usuários `admin`** → visualizam todas as colunas.  
- **Usuários `user`** → não visualizam a coluna `cost_micros`.  

---

## 📊 Métricas (`metrics.csv`)

O arquivo `metrics.csv` é usado como fonte de dados. Ele deve conter uma coluna de data (`date`, `dia` ou `ds`) para que os filtros funcionem.

**Exemplo de `metrics.csv`:**

```csv
date,impressions,clicks,cost_micros
2025-01-01,1200,300,4500000
2025-01-02,1800,500,6000000
2025-01-03,2000,600,7000000
```

---

## 🖥️ Frontend

### 🔐 Login (`index.html`)
- Usuário insere usuário/email e senha.  
- Após autenticação bem-sucedida:
  - É gerado um token JWT.  
  - O token é armazenado no `localStorage`.  
  - Usuário é redirecionado para o `dashboard.html`.  

### 📈 Dashboard (`dashboard.html`)
- Exibe métricas paginadas (25 registros por página).  
- Mostra:
  - Total de registros  
  - Página atual  
  - Registros por página  
- Possui filtros por data (inicial e final).  
- Possui paginação (botões **Anterior / Próxima**).  
- Usuário pode sair clicando em **Sair**, o que remove o token e retorna à tela de login.  

---

## 📑 Endpoints da API

### `POST /api/login`
**Entrada:**
```json
{ "email": "user@monks.com", "password": "123" }
```
**Saída:**
```json
{ "access_token": "...", "token_type": "bearer" }
```

### `GET /api/me`
Retorna informações do usuário logado (`email`, `role`).

### `GET /api/columns`
Retorna colunas do CSV (dependendo do perfil do usuário).

### `GET /api/data`
Retorna dados filtrados e paginados.

**Parâmetros:**  
- `start_date` → filtro por data inicial  
- `end_date` → filtro por data final  
- `order_by` → coluna para ordenar  
- `order_dir` → `asc` (padrão) ou `desc`  
- `page` → número da página  
- `page_size` → quantidade de registros por página  

---

## 🔧 Variáveis de ambiente

- `SECRET_KEY`: chave secreta usada para assinar tokens JWT.  
  Se não definida, será usado o valor padrão `"CHANGE_THIS_SECRET_TO_A_STRONG_KEY"`.  

**Exemplo:**

```bash
export SECRET_KEY="minha_chave_super_secreta"
```

---

## ✅ Melhorias Futuras

- Permitir upload dinâmico de arquivos CSV.  
- Adicionar gráficos visuais (ex: Chart.js) no dashboard.  
- Criar exportação de relatórios em Excel/PDF.  
- Adicionar CRUD de usuários via API.  

---
