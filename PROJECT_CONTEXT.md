# Crypto Intelligence Engine

## Objetivo

Criar um sistema avançado de inteligência e análise de mercado de criptomoedas, inicialmente voltado para estudo, pesquisa, backtesting e paper trading.

O sistema deverá coletar dados em tempo real e transformar esses dados em análises probabilísticas sobre pressão compradora, pressão vendedora, momentum, volume, atividade anormal e estrutura de mercado.

O sistema não deve assumir que consegue prever o mercado com certeza.

## Escopo inicial

O sistema deverá ser capaz de:

- monitorar criptomoedas ativas;
- aplicar filtros de preço;
- coletar dados em tempo real;
- analisar trades;
- analisar volume;
- medir buy flow e sell flow;
- detectar volume anormal;
- medir velocidade do preço;
- medir aceleração do preço;
- analisar order book;
- detectar desequilíbrios;
- analisar momentum;
- detectar mudanças de estrutura;
- analisar múltiplos timeframes;
- detectar possíveis movimentos anormais;
- identificar possíveis pumps e dumps;
- criar scores de pressão de mercado;
- gerar análises probabilísticas;
- registrar previsões;
- comparar previsões com resultados reais;
- calcular métricas estatísticas;
- realizar backtesting;
- realizar paper trading;
- futuramente incorporar Machine Learning.

## Filosofia do sistema

O sistema deve responder perguntas como:

- O que está acontecendo agora?
- Quem está exercendo mais pressão: compradores ou vendedores?
- Essa pressão está aumentando ou diminuindo?
- O volume está normal ou anormal?
- O preço está acelerando?
- A estrutura está mudando?
- Os diferentes timeframes concordam?
- O cenário atual é semelhante a situações históricas?
- O que normalmente aconteceu depois em situações semelhantes?

## Componentes principais

### Market Data Engine

Responsável por receber dados em tempo real.

### Trade Flow Engine

Responsável por analisar fluxo de compras e vendas.

### Volume Intelligence Engine

Responsável por detectar mudanças e anomalias de volume.

### Momentum Engine

Responsável por medir direção, velocidade e aceleração.

### Order Book Engine

Responsável por analisar o livro de ordens.

### Market Structure Engine

Responsável por analisar estrutura, rompimentos e mudanças de tendência.

#### Semântica temporal da estrutura de mercado

Os componentes de Market Structure devem operar sobre dados numéricos e estruturais normalizados, permanecendo independentes da Binance ou de qualquer outra fonte específica de dados.

Para pontos de swing:

- `index` representa o candle em que o extremo do swing ocorreu;
- `confirmation_index` representa o primeiro candle em que o swing pode ser considerado conhecido, após a disponibilidade dos candles necessários à sua direita;
- um swing não pode ser utilizado por análises posteriores antes de seu `confirmation_index`;
- a classificação estrutural deve preservar o `confirmation_index` dos swings confirmados;
- detectores de rompimento e outros componentes posteriores devem respeitar essa informação temporal;
- backtests, Prediction Lab e análises históricas devem respeitar essa mesma regra para evitar look-ahead bias.

Para Break of Structure (BOS), um nível estrutural confirmado somente pode ser considerado rompido por candles posteriores ao seu `confirmation_index`.

### Multi-Timeframe Engine

Responsável por comparar diferentes horizontes temporais.

### Anomaly Detection Engine

Responsável por detectar comportamento fora do padrão.

### Market Pressure Engine

Responsável por combinar múltiplas evidências de pressão compradora ou vendedora.

### Intelligence Engine

Responsável por score, confiança, contradições e combinação das análises.

### Prediction Lab

Responsável por registrar previsões e verificar o que realmente aconteceu depois.

### Machine Learning

Será adicionado somente após a coleta de dados suficientes e validação da qualidade dos dados.

## Tecnologias inicialmente previstas

### Backend

- Python
- asyncio
- WebSockets
- httpx
- Pydantic

### Dados

- NumPy
- Pandas
- possivelmente Polars

### Banco de dados

- MongoDB

### API

- FastAPI

### Frontend futuro

- React
- TypeScript
- Vite
- Tailwind CSS

### Machine Learning futuro

- scikit-learn
- XGBoost
- LightGBM
- PyTorch, somente se houver justificativa

### Testes

- pytest
- pytest-asyncio

### Infraestrutura

- Git
- GitHub
- Docker
- Docker Compose

## Estratégia de desenvolvimento

O sistema será construído por fases.

Primeiro:

dados -> processamento -> análise -> registro -> validação

Depois:

Machine Learning -> comparação -> ensemble

A interface gráfica será construída somente depois que o motor principal estiver funcionando.
