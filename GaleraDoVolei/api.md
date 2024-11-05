# Documentação da API - Quadra de Vôlei

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
