# Documentação da API - Quadra de Vôlei
#### Dupla:
Aser Junior e Ebert Ian
## Rotas da API

---

### **Mostrar uma lista de jogadores**
Retorna a lista de jogadores cadastrados, com possibilidade de filtrar, ordenar e buscar por diferentes parâmetros.

#### Rota: `/jogadores`
#### Método: `GET`

**Query Params**:
- `sexo` (opcional): Filtra jogadores por sexo (`M`, `F`, `O`).
- `faixa_idade` (opcional): Filtra jogadores por faixa de idade (ex: `15-18`, `19-25`).
- `categoria` (opcional): Filtra jogadores por categoria (ex: `iniciante`, `avançado`).
- `q` (opcional): Busca por nome ou parte do nome do jogador.
- `sort` (opcional): Ordenação dos resultados (`nome`, `idade`, `categoria`, etc). Prefixar com `-` para ordem decrescente (ex: `-idade`).
- `page` (opcional): Número da página para paginação (padrão: 1).
- `limit` (opcional): Número máximo de resultados por página (padrão: 10).

**Exemplo de Requisição**:
```http
GET /jogadores?sexo=M&faixa_idade=19-25&sort=nome&page=2&limit=5
```
Resposta
```
{
  "total": 50,
  "page": 2,
  "limit": 5,
  "jogadores": [
    {
      "id": 1,
      "nome": "João Silva",
      "sexo": "M",
      "idade": 23,
      "faixa_idade": "19-25",
      "categoria": "avançado"
    },
    {
      "id": 2,
      "nome": "Carlos Souza",
      "sexo": "M",
      "idade": 24,
      "faixa_idade": "19-25",
      "categoria": "iniciante"
    }
  ]
}
```

### **Criar um novo jogador**
Cria um novo jogador na base de dados.

#### Rota: `/jogadores`
#### Método: `POST`

**Body Params (JSON)**:
```
{
  "nome": "Carlos Souza",
  "sexo": "M",
  "idade": 24,
  "faixa_idade": "19-25",
  "categoria": "iniciante"
}
```
Resposta
```
{
  "id": 3,
  "mensagem": "Jogador criado com sucesso."
}
```

### **Mostrar uma lista de partidas**
Retorna uma lista de partidas disponíveis, com possibilidade de filtragem por tipo, categoria, situação e outros parâmetros.

#### Rota: `/partidas`
#### Método: `GET`

**Query Params**:
- `tipo` (opcional): Tipo da partida (`mista`, `especifica`).
- `categoria` (opcional): Categoria da partida (ex: `iniciante`, `avançado`).
- `situacao` (opcional): Situação da partida (ex: `nova`, `em_adesao`, `realizada`).
- `local` (opcional): Filtra por local da partida (ex: `Quadra 01`).
- `data_inicio` (opcional): Filtra partidas a partir de uma data específica (ex: `data_inicio=2024-11-01`).
- `q` (opcional): Busca por nome ou descrição da partida.
- `sort` (opcional): Ordenação dos resultados (ex: `data`).
- `page` (opcional): Número da página para paginação (padrão: 1).
- `limit` (opcional): Número máximo de resultados por página (padrão: 10).

**Exemplo de Requisição**:
```http
GET /partidas?tipo=mista&categoria=avançado&situacao=nova&sort=data&page=1&limit=5
```

Resposta
```
{
  "total": 15,
  "page": 1,
  "limit": 5,
  "partidas": [
    {
      "id": 101,
      "tipo": "mista",
      "categoria": "avançado",
      "local": "Quadra 1",
      "data": "2024-11-05T14:00:00",
      "situacao": "nova"
    },
    {
      "id": 102,
      "tipo": "mista",
      "categoria": "iniciante",
      "local": "Quadra 2",
      "data": "2024-11-06T09:00:00",
      "situacao": "em_adesao"
    }
  ]
}
```

### **Criar uma nova partida**
Cria uma nova partida na base de dados.

#### Rota: `/partidas/{id}/adesao`
#### Método: `POST`

**Url params**:
- `{id}` (obrigatório): O ID da partida à qual o jogador deseja aderir.

**Body Params (JSON)**:
```
{
  "jogador_id": 1
}
```

Resposta
```
{
  "mensagem": "Pedido de adesão enviado. Aguardando aprovação."
}
```

### **Listar adesões pendentes**
Retorna a lista de jogadores que solicitaram adesão a uma partida específica.

#### Rota: `/partidas/{id}/adesao`
#### Método: `GET`

**Url params**:
- `{id}` (obrigatório): O ID da partida.

Resposta
```
{
  "jogadores": [
    {
      "jogador_id": 1,
      "nome": "João Silva",
      "status": "pendente"
    },
    {
      "jogador_id": 2,
      "nome": "Carlos Souza",
      "status": "pendente"
    }
  ]
}
```

### **Aprovar ou rejeitar adesão**
Aprova ou rejeita um pedido de adesão para um jogador em uma partida.

#### Rota: `/partidas/{id}/adesao/{jogador_id}`
#### Método: `PUT`

**Url params**:
- `{id}` (obrigatório): O ID da partida.
- `{jogador_id}` (obrigatório): O ID do jogador a ser aprovado ou rejeitado.


**Body Params (JSON)**:
```
{
  "status": "aceito"  // ou "rejeitado"
}
```

Resposta
```
{
  "mensagem": "Status do pedido de adesão atualizado."
}
```

### **Operações Autenticadas**
Algumas rotas da API exigem autenticação para garantir a segurança. Isso inclui:

- Criação de Jogadores `(POST /jogadores)`
- Criação de Partidas  `(POST /partidas)`
- Solicitação de Adesão `(POST /partidas/{id}/adesao)`
- Aprovação/Rejeição de Adesões `(PUT /partidas/{id}/adesao/{jogador_id})`

**Cabeçalho de Autenticação**:
```
Authorization: Bearer_token
```

### **Respostas de Erro**
A API pode retornar os seguintes códigos de status HTTP para indicar erros:

- 400 Bad Request: Parâmetros inválidos ou dados faltantes.
- 401 Unauthorized: Falta de autenticação ou token inválido
- 404 Not Found: Recurso não encontrado
- 500 Internal Server Error: Erro no servidor.
