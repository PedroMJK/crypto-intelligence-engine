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

#### Order Book Imbalance

O Order Book Engine deve permitir medir o desequilíbrio entre a quantidade agregada de ordens de compra e venda observadas nos níveis selecionados do livro.

Para o cálculo do imbalance:

- `bids` representam níveis de compra no formato `(price, quantity)`;
- `asks` representam níveis de venda no formato `(price, quantity)`;
- `depth` determina a quantidade máxima de níveis considerados em cada lado;
- quando `depth` for maior que a quantidade disponível de níveis, todos os níveis disponíveis devem ser utilizados;
- a quantidade agregada de bids é a soma das quantidades dos níveis selecionados;
- a quantidade agregada de asks é a soma das quantidades dos níveis selecionados;
- o volume total é `bid_volume + ask_volume`;
- o imbalance deve ser calculado como `(bid_volume - ask_volume) / (bid_volume + ask_volume)`;
- o resultado deve permanecer entre `-1` e `1`;
- imbalance positivo representa maior quantidade agregada no lado dos bids;
- imbalance negativo representa maior quantidade agregada no lado dos asks;
- imbalance igual a zero representa equilíbrio entre os lados;
- `state` deve ser `bid_dominant`, `ask_dominant` ou `balanced`, de acordo com o sinal do imbalance;
- a análise deve utilizar somente os níveis efetivamente observados;
- preços devem ser maiores que zero;
- quantidades não podem ser negativas;
- `depth` deve ser um inteiro maior que zero;
- livros com bids ou asks vazios devem ser rejeitados;
- o volume total deve ser maior que zero;
- as entradas recebidas não devem ser modificadas;
- esta primeira definição não utiliza pesos, distância do preço, order book walls, execução de trades, spoofing ou thresholds arbitrários;
- o imbalance representa a distribuição da liquidez observada no livro e não constitui, isoladamente, uma previsão de movimento futuro do preço.

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

#### Agrupamento de níveis de suporte e resistência

Os níveis estruturais confirmados podem ser agrupados em zonas próximas de suporte ou resistência para representar regiões de preço formadas por múltiplos níveis relacionados.

Para o agrupamento:

- níveis de suporte e resistência devem ser agrupados separadamente e nunca combinados na mesma zona;
- a proximidade entre um novo nível e uma zona deve ser calculada de forma relativa ao preço representativo da zona, evitando uma tolerância absoluta fixa entre ativos com escalas de preço diferentes;
- o limite de proximidade é inclusivo;
- o preço representativo da zona é a média aritmética dos níveis incorporados e deve ser atualizado à medida que novos níveis são adicionados;
- cada novo nível deve ser comparado ao preço representativo atualizado da zona;
- níveis que não encontram uma zona compatível devem ser preservados como zonas individuais;
- a zona deve preservar os índices estruturais dos níveis que contribuíram para sua formação;
- o `confirmation_index` de uma zona representa o momento em que aquela versão da zona passou a ser conhecida;
- o agrupamento deve respeitar a ordem estrutural e temporal dos níveis confirmados;
- nenhuma zona pode incorporar informação que ainda não estivesse disponível naquele momento, preservando causalidade e evitando look-ahead bias em backtests e análises históricas.

#### Detecção de toques em suporte e resistência

Zonas confirmadas de suporte e resistência podem ser monitoradas para identificar contatos posteriores do preço com o preço representativo da zona.

Para a detecção de toques:

- um toque ocorre quando o preço representativo da zona está contido no intervalo negociado pelo candle, isto é, `low <= zone_price <= high`;
- a mesma regra geométrica de contato é utilizada para zonas de suporte e resistência, enquanto o tipo da zona preserva seu significado estrutural;
- candles totalmente acima ou totalmente abaixo do preço representativo da zona não devem ser considerados toques;
- os limites são inclusivos, portanto igualdade com a máxima ou a mínima do candle também representa um toque;
- a busca por toques deve começar somente em `confirmation_index + 1`;
- o candle de confirmação da zona não deve ser contado como um novo toque;
- uma mesma zona pode registrar múltiplos toques posteriores;
- múltiplas zonas podem produzir eventos de toque, e os eventos resultantes devem ser apresentados em ordem cronológica;
- a detecção utiliza o preço representativo já produzido pelo agrupamento e não introduz uma nova tolerância de preço;
- a detecção de toques não calcula força da zona, rompimentos, inversão de papel ou sinais de trading;
- as entradas de zonas, máximas e mínimas não devem ser modificadas;
- a detecção deve preservar causalidade temporal e evitar look-ahead bias.

#### Força de níveis de suporte e resistência

Zonas confirmadas de suporte e resistência podem ter sua força estrutural acompanhada ao longo do tempo a partir das evidências já conhecidas sobre sua formação e seus toques posteriores.

Para o cálculo de força:

- a força inicial de uma zona é determinada por seu `level_count`, representando a quantidade de níveis estruturais que contribuíram para sua formação;
- no momento do `confirmation_index` da zona, `touch_count` deve ser igual a zero e `strength` deve ser igual a `level_count`;
- cada toque posterior confirmado na mesma zona incrementa `touch_count` em uma unidade;
- a força deve ser calculada de forma determinística como `strength = level_count + touch_count`;
- cada novo toque deve produzir um novo estado temporal da força da zona, preservando os estados anteriores;
- os eventos de força devem preservar o tipo, o preço representativo, o `level_count` e o `zone_confirmation_index` da zona correspondente;
- um toque somente pode atualizar a força quando seu índice for posterior ao `confirmation_index` da zona;
- a associação entre um toque e sua zona deve considerar conjuntamente `type`, `price` e `zone_confirmation_index`;
- eventos pertencentes a múltiplas zonas devem ser apresentados em ordem cronológica, preservando eventos distintos que ocorram no mesmo candle;
- a ordem de entrada dos eventos de toque não deve alterar a evolução cronológica da força;
- eventos de toque que não correspondam a uma zona existente devem ser rejeitados em vez de ignorados silenciosamente;
- o cálculo de força não deve modificar as zonas nem os eventos de toque recebidos;
- esta primeira definição de força não utiliza pesos arbitrários, classificações como fraco, médio ou forte, volume, ATR, distância da reação, recência, rompimentos, inversão de papel ou sinais de trading;
- o cálculo deve utilizar somente informações disponíveis em cada momento, preservando causalidade temporal e evitando look-ahead bias em backtests e análises históricas.

#### Rompimento de níveis de suporte e resistência

Zonas confirmadas de suporte e resistência podem ser monitoradas para identificar o primeiro fechamento que rompe seu preço representativo após a confirmação da zona.

Para a detecção de rompimentos:

- uma resistência é considerada rompida quando um candle posterior fecha estritamente acima do preço representativo da zona, isto é, `close > zone_price`;
- um suporte é considerado rompido quando um candle posterior fecha estritamente abaixo do preço representativo da zona, isto é, `close < zone_price`;
- igualdade entre o fechamento e o preço da zona não representa rompimento;
- máximas e mínimas intrabar não são suficientes para confirmar um rompimento nesta definição; a confirmação utiliza o preço de fechamento;
- a busca por rompimentos deve começar somente em `confirmation_index + 1`;
- candles anteriores ou o próprio candle de confirmação da zona não podem produzir um evento de rompimento;
- cada zona deve produzir no máximo um evento, correspondente ao primeiro fechamento que efetivamente rompe seu preço representativo;
- múltiplas zonas podem ser rompidas no mesmo candle, e esses eventos distintos devem ser preservados;
- eventos de diferentes zonas devem ser apresentados em ordem cronológica;
- a detecção de rompimentos é independente da força acumulada da zona;
- o rompimento não deve automaticamente transformar suporte em resistência ou resistência em suporte, pois inversão de papel constitui uma análise distinta;
- a detecção não gera sinais de trading;
- as zonas e os fechamentos recebidos não devem ser modificados;
- o detector deve utilizar somente informações disponíveis após a confirmação de cada zona, preservando causalidade temporal e evitando look-ahead bias.

### Volatility Engine

Responsável por medir a evolução da volatilidade do mercado de forma objetiva e temporal, utilizando métricas numéricas que possam posteriormente alimentar análises de regime, anomalias e inteligência de mercado.

#### Série temporal de Average True Range (ATR)

O componente `AverageTrueRange` deve disponibilizar, além do ATR final, a série de valores ATR confirmados ao longo dos dados recebidos.

Para a série ATR:

- `calculate()` continua retornando somente o ATR final, preservando o contrato existente;
- `calculate_series()` retorna todos os valores ATR válidos a partir do primeiro período completo;
- para `N` candles e período `P`, a série resultante contém `N - P + 1` valores;
- os primeiros `P - 1` candles não produzem valores `None`; a série começa diretamente no primeiro ATR confirmado;
- o primeiro ATR é calculado pela média dos primeiros True Ranges do período;
- os valores posteriores utilizam a suavização de Wilder;
- o True Range considera a máxima, a mínima e o fechamento anterior, preservando gaps entre candles;
- cada valor ATR utiliza somente dados disponíveis até aquele momento, preservando causalidade temporal.

#### Análise de expansão e contração da volatilidade

O componente `VolatilityAnalyzer` compara o ATR atual com uma referência formada pelos valores ATR imediatamente anteriores.

Para a análise:

- o último elemento de `atr_values` representa o ATR atual;
- a referência utiliza somente os `lookback` valores imediatamente anteriores ao ATR atual;
- valores anteriores à janela solicitada não participam do cálculo;
- `reference_atr` é a média aritmética dos ATRs da janela de referência;
- `ratio` é calculado como `current_atr / reference_atr`;
- `change` é calculado como `ratio - 1`;
- `ratio > 1` representa volatilidade `expanding`;
- `ratio < 1` representa volatilidade `contracting`;
- `ratio == 1` representa volatilidade `stable`;
- a análise mede expansão ou contração da volatilidade e não direção do preço;
- volatilidade em expansão não implica movimento de alta, e volatilidade em contração não implica movimento de baixa;
- não são utilizados limites arbitrários para classificar volatilidade como baixa, média ou alta;
- ATR igual a zero é permitido como valor atual;
- ATRs negativos são inválidos;
- a referência deve ser maior que zero para que a razão seja definida;
- a análise exige o ATR atual e pelo menos `lookback` valores anteriores;
- os valores ATR recebidos não devem ser modificados;
- somente informações anteriores ao ATR atual são utilizadas na referência, preservando causalidade temporal e evitando look-ahead bias;
- classificações de regime, thresholds históricos, percentis, sinais de trading e interpretação direcional permanecem responsabilidades de componentes posteriores.

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
