# Crypto Intelligence Engine

## Objetivo

Criar um sistema avançado de inteligência e análise de mercado de criptomoedas, inicialmente voltado para estudo, pesquisa, backtesting e paper trading.

O sistema deverá coletar dados em tempo real e transformar esses dados em análises probabilísticas sobre pressão compradora, pressão vendedora, momentum, volume, atividade anormal e estrutura de mercado.

O sistema não deve assumir que consegue prever o mercado com certeza.

## Escopo inicial

O sistema deverá ser capaz de:

* monitorar criptomoedas ativas;
* aplicar filtros de preço;
* coletar dados em tempo real;
* analisar trades;
* analisar volume;
* medir buy flow e sell flow;
* detectar volume anormal;
* medir velocidade do preço;
* medir aceleração do preço;
* analisar order book;
* detectar desequilíbrios;
* analisar momentum;
* detectar mudanças de estrutura;
* analisar múltiplos timeframes;
* detectar possíveis movimentos anormais;
* identificar possíveis pumps e dumps;
* criar scores de pressão de mercado;
* gerar análises probabilísticas;
* registrar previsões;
* comparar previsões com resultados reais;
* calcular métricas estatísticas;
* realizar backtesting;
* realizar paper trading;
* futuramente incorporar Machine Learning.

## Filosofia do sistema

O sistema deve responder perguntas como:

* O que está acontecendo agora?
* Quem está exercendo mais pressão: compradores ou vendedores?
* Essa pressão está aumentando ou diminuindo?
* O volume está normal ou anormal?
* O preço está acelerando?
* A estrutura está mudando?
* Os diferentes timeframes concordam?
* O cenário atual é semelhante a situações históricas?
* O que normalmente aconteceu depois em situações semelhantes?

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

* `bids` representam níveis de compra no formato `(price, quantity)`;
* `asks` representam níveis de venda no formato `(price, quantity)`;
* `depth` determina a quantidade máxima de níveis considerados em cada lado;
* quando `depth` for maior que a quantidade disponível de níveis, todos os níveis disponíveis devem ser utilizados;
* a quantidade agregada de bids é a soma das quantidades dos níveis selecionados;
* a quantidade agregada de asks é a soma das quantidades dos níveis selecionados;
* o volume total é `bid_volume + ask_volume`;
* o imbalance deve ser calculado como `(bid_volume - ask_volume) / (bid_volume + ask_volume)`;
* o resultado deve permanecer entre `-1` e `1`;
* imbalance positivo representa maior quantidade agregada no lado dos bids;
* imbalance negativo representa maior quantidade agregada no lado dos asks;
* imbalance igual a zero representa equilíbrio entre os lados;
* `state` deve ser `bid_dominant`, `ask_dominant` ou `balanced`, de acordo com o sinal do imbalance;
* a análise deve utilizar somente os níveis efetivamente observados;
* preços devem ser maiores que zero;
* quantidades não podem ser negativas;
* `depth` deve ser um inteiro maior que zero;
* livros com bids ou asks vazios devem ser rejeitados;
* o volume total deve ser maior que zero;
* as entradas recebidas não devem ser modificadas;
* esta primeira definição não utiliza pesos, distância do preço, order book walls, execução de trades, spoofing ou thresholds arbitrários;
* o imbalance representa a distribuição da liquidez observada no livro e não constitui, isoladamente, uma previsão de movimento futuro do preço.

### Market Structure Engine

Responsável por analisar estrutura, rompimentos e mudanças de tendência.

#### Semântica temporal da estrutura de mercado

Os componentes de Market Structure devem operar sobre dados numéricos e estruturais normalizados, permanecendo independentes da Binance ou de qualquer outra fonte específica de dados.

Para pontos de swing:

* `index` representa o candle em que o extremo do swing ocorreu;
* `confirmation_index` representa o primeiro candle em que o swing pode ser considerado conhecido, após a disponibilidade dos candles necessários à sua direita;
* um swing não pode ser utilizado por análises posteriores antes de seu `confirmation_index`;
* a classificação estrutural deve preservar o `confirmation_index` dos swings confirmados;
* detectores de rompimento e outros componentes posteriores devem respeitar essa informação temporal;
* backtests, Prediction Lab e análises históricas devem respeitar essa mesma regra para evitar look-ahead bias.

Para Break of Structure (BOS), um nível estrutural confirmado somente pode ser considerado rompido por candles posteriores ao seu `confirmation_index`.

#### Agrupamento de níveis de suporte e resistência

Os níveis estruturais confirmados podem ser agrupados em zonas próximas de suporte ou resistência para representar regiões de preço formadas por múltiplos níveis relacionados.

Para o agrupamento:

* níveis de suporte e resistência devem ser agrupados separadamente e nunca combinados na mesma zona;
* a proximidade entre um novo nível e uma zona deve ser calculada de forma relativa ao preço representativo da zona, evitando uma tolerância absoluta fixa entre ativos com escalas de preço diferentes;
* o limite de proximidade é inclusivo;
* o preço representativo da zona é a média aritmética dos níveis incorporados e deve ser atualizado à medida que novos níveis são adicionados;
* cada novo nível deve ser comparado ao preço representativo atualizado da zona;
* níveis que não encontram uma zona compatível devem ser preservados como zonas individuais;
* a zona deve preservar os índices estruturais dos níveis que contribuíram para sua formação;
* o `confirmation_index` de uma zona representa o momento em que aquela versão da zona passou a ser conhecida;
* o agrupamento deve respeitar a ordem estrutural e temporal dos níveis confirmados;
* nenhuma zona pode incorporar informação que ainda não estivesse disponível naquele momento, preservando causalidade e evitando look-ahead bias em backtests e análises históricas.

#### Detecção de toques em suporte e resistência

Zonas confirmadas de suporte e resistência podem ser monitoradas para identificar contatos posteriores do preço com o preço representativo da zona.

Para a detecção de toques:

* um toque ocorre quando o preço representativo da zona está contido no intervalo negociado pelo candle, isto é, `low <= zone_price <= high`;
* a mesma regra geométrica de contato é utilizada para zonas de suporte e resistência, enquanto o tipo da zona preserva seu significado estrutural;
* candles totalmente acima ou totalmente abaixo do preço representativo da zona não devem ser considerados toques;
* os limites são inclusivos, portanto igualdade com a máxima ou a mínima do candle também representa um toque;
* a busca por toques deve começar somente em `confirmation_index + 1`;
* o candle de confirmação da zona não deve ser contado como um novo toque;
* uma mesma zona pode registrar múltiplos toques posteriores;
* múltiplas zonas podem produzir eventos de toque, e os eventos resultantes devem ser apresentados em ordem cronológica;
* a detecção utiliza o preço representativo já produzido pelo agrupamento e não introduz uma nova tolerância de preço;
* a detecção de toques não calcula força da zona, rompimentos, inversão de papel ou sinais de trading;
* as entradas de zonas, máximas e mínimas não devem ser modificadas;
* a detecção deve preservar causalidade temporal e evitar look-ahead bias.

#### Força de níveis de suporte e resistência

Zonas confirmadas de suporte e resistência podem ter sua força estrutural acompanhada ao longo do tempo a partir das evidências já conhecidas sobre sua formação e seus toques posteriores.

Para o cálculo de força:

* a força inicial de uma zona é determinada por seu `level_count`, representando a quantidade de níveis estruturais que contribuíram para sua formação;
* no momento do `confirmation_index` da zona, `touch_count` deve ser igual a zero e `strength` deve ser igual a `level_count`;
* cada toque posterior confirmado na mesma zona incrementa `touch_count` em uma unidade;
* a força deve ser calculada de forma determinística como `strength = level_count + touch_count`;
* cada novo toque deve produzir um novo estado temporal da força da zona, preservando os estados anteriores;
* os eventos de força devem preservar o tipo, o preço representativo, o `level_count` e o `zone_confirmation_index` da zona correspondente;
* um toque somente pode atualizar a força quando seu índice for posterior ao `confirmation_index` da zona;
* a associação entre um toque e sua zona deve considerar conjuntamente `type`, `price` e `zone_confirmation_index`;
* eventos pertencentes a múltiplas zonas devem ser apresentados em ordem cronológica, preservando eventos distintos que ocorram no mesmo candle;
* a ordem de entrada dos eventos de toque não deve alterar a evolução cronológica da força;
* eventos de toque que não correspondam a uma zona existente devem ser rejeitados em vez de ignorados silenciosamente;
* o cálculo de força não deve modificar as zonas nem os eventos de toque recebidos;
* esta primeira definição de força não utiliza pesos arbitrários, classificações como fraco, médio ou forte, volume, ATR, distância da reação, recência, rompimentos, inversão de papel ou sinais de trading;
* o cálculo deve utilizar somente informações disponíveis em cada momento, preservando causalidade temporal e evitando look-ahead bias em backtests e análises históricas.

#### Rompimento de níveis de suporte e resistência

Zonas confirmadas de suporte e resistência podem ser monitoradas para identificar o primeiro fechamento que rompe seu preço representativo após a confirmação da zona.

Para a detecção de rompimentos:

* uma resistência é considerada rompida quando um candle posterior fecha estritamente acima do preço representativo da zona, isto é, `close > zone_price`;
* um suporte é considerado rompido quando um candle posterior fecha estritamente abaixo do preço representativo da zona, isto é, `close < zone_price`;
* igualdade entre o fechamento e o preço da zona não representa rompimento;
* máximas e mínimas intrabar não são suficientes para confirmar um rompimento nesta definição; a confirmação utiliza o preço de fechamento;
* a busca por rompimentos deve começar somente em `confirmation_index + 1`;
* candles anteriores ou o próprio candle de confirmação da zona não podem produzir um evento de rompimento;
* cada zona deve produzir no máximo um evento, correspondente ao primeiro fechamento que efetivamente rompe seu preço representativo;
* múltiplas zonas podem ser rompidas no mesmo candle, e esses eventos distintos devem ser preservados;
* eventos de diferentes zonas devem ser apresentados em ordem cronológica;
* a detecção de rompimentos é independente da força acumulada da zona;
* o rompimento não deve automaticamente transformar suporte em resistência ou resistência em suporte, pois inversão de papel constitui uma análise distinta;
* a detecção não gera sinais de trading;
* as zonas e os fechamentos recebidos não devem ser modificados;
* o detector deve utilizar somente informações disponíveis após a confirmação de cada zona, preservando causalidade temporal e evitando look-ahead bias.

### Volatility Engine

Responsável por medir a evolução da volatilidade do mercado de forma objetiva e temporal, utilizando métricas numéricas que possam posteriormente alimentar análises de regime, anomalias e inteligência de mercado.

#### Série temporal de Average True Range (ATR)

O componente `AverageTrueRange` deve disponibilizar, além do ATR final, a série de valores ATR confirmados ao longo dos dados recebidos.

Para a série ATR:

* `calculate()` continua retornando somente o ATR final, preservando o contrato existente;
* `calculate_series()` retorna todos os valores ATR válidos a partir do primeiro período completo;
* para `N` candles e período `P`, a série resultante contém `N - P + 1` valores;
* os primeiros `P - 1` candles não produzem valores `None`; a série começa diretamente no primeiro ATR confirmado;
* o primeiro ATR é calculado pela média dos primeiros True Ranges do período;
* os valores posteriores utilizam a suavização de Wilder;
* o True Range considera a máxima, a mínima e o fechamento anterior, preservando gaps entre candles;
* cada valor ATR utiliza somente dados disponíveis até aquele momento, preservando causalidade temporal.

#### Análise de expansão e contração da volatilidade

O componente `VolatilityAnalyzer` compara o ATR atual com uma referência formada pelos valores ATR imediatamente anteriores.

Para a análise:

* o último elemento de `atr_values` representa o ATR atual;
* a referência utiliza somente os `lookback` valores imediatamente anteriores ao ATR atual;
* valores anteriores à janela solicitada não participam do cálculo;
* `reference_atr` é a média aritmética dos ATRs da janela de referência;
* `ratio` é calculado como `current_atr / reference_atr`;
* `change` é calculado como `ratio - 1`;
* `ratio > 1` representa volatilidade `expanding`;
* `ratio < 1` representa volatilidade `contracting`;
* `ratio == 1` representa volatilidade `stable`;
* a análise mede expansão ou contração da volatilidade e não direção do preço;
* volatilidade em expansão não implica movimento de alta, e volatilidade em contração não implica movimento de baixa;
* não são utilizados limites arbitrários para classificar volatilidade como baixa, média ou alta;
* ATR igual a zero é permitido como valor atual;
* ATRs negativos são inválidos;
* a referência deve ser maior que zero para que a razão seja definida;
* a análise exige o ATR atual e pelo menos `lookback` valores anteriores;
* os valores ATR recebidos não devem ser modificados;
* somente informações anteriores ao ATR atual são utilizadas na referência, preservando causalidade temporal e evitando look-ahead bias;
* classificações de regime, thresholds históricos, percentis, sinais de trading e interpretação direcional permanecem responsabilidades de componentes posteriores.

### Multi-Timeframe Engine

Responsável por comparar estados de mercado confirmados em diferentes horizontes temporais, preservando a evolução temporal de cada timeframe sem transformar essa primeira camada em uma interpretação direcional de trading.

Para a análise multi-timeframe:

* cada estado deve identificar seu `timeframe`, seu `state` e seu `confirmation_timestamp`;
* `confirmation_timestamp` representa o momento em que aquele estado passou a estar confirmado e disponível para análises posteriores;
* `reference_timestamp` representa o momento de referência da análise atual;
* estados com `confirmation_timestamp` posterior ao `reference_timestamp` devem ser ignorados, pois ainda não estavam disponíveis naquele momento;
* para cada timeframe, somente o estado mais recentemente confirmado até o `reference_timestamp` deve ser preservado;
* estados anteriores do mesmo timeframe devem ser substituídos pelo estado mais recente confirmado;
* timeframes distintos devem permanecer independentes, mesmo quando apresentarem estados diferentes ou contraditórios;
* a ordem de entrada dos estados não deve alterar o resultado final;
* os estados resultantes devem ser apresentados em ordem temporal crescente de timeframe;
* timeframes como `1m`, `5m`, `15m`, `30m`, `1h`, `4h` e `1d` devem ser ordenados pela duração representada, e não alfabeticamente;
* timeframes reconhecidos devem ser convertidos para uma unidade temporal comum para determinar sua ordem;
* timeframes não reconhecidos pela semântica temporal inicial devem ser preservados e apresentados após os timeframes reconhecidos, em vez de causar falha durante a ordenação;
* a análise deve preservar os registros recebidos e não modificar os objetos de entrada;
* estados confirmados exatamente no `reference_timestamp` são considerados disponíveis e podem participar da análise;
* estados futuros em relação ao `reference_timestamp` não devem influenciar o resultado;
* a análise deve utilizar somente informações disponíveis até o `reference_timestamp`, preservando causalidade temporal e evitando look-ahead bias;
* esta primeira camada não determina concordância, conflito, força de confluência, score, probabilidade ou direção futura do preço;
* a interpretação de concordância ou divergência entre timeframes permanece responsabilidade de componentes posteriores do sistema.

### Market Regime Engine

Responsável por representar o contexto atual do mercado a partir da combinação de tendência estrutural e estado de volatilidade, mantendo essas dimensões separadas e sem transformar o contexto em um sinal de trading.

Para a primeira definição de Market Regime:

* `trend` deve representar o estado produzido pela análise de estrutura de mercado;
* os estados de tendência aceitos são `bullish`, `bearish` e `indeterminate`;
* `volatility` deve representar o estado produzido pela análise de volatilidade;
* os estados de volatilidade aceitos são `expanding`, `stable` e `contracting`;
* o resultado deve preservar as duas dimensões separadamente, utilizando as chaves `trend` e `volatility`;
* a combinação entre tendência e volatilidade não deve criar classificações compostas arbitrárias;
* `PressureScore` não faz parte da primeira definição do Market Regime e deve permanecer uma análise independente;
* a análise multi-timeframe não deve ser reduzida a um único estado de regime nesta primeira camada;
* estados de tendência devem ser validados contra o conjunto de estados estruturais suportados;
* estados de volatilidade devem ser validados contra o conjunto de estados de volatilidade suportados;
* valores de tendência e volatilidade devem ser strings não vazias;
* entradas com tipos inválidos devem ser rejeitadas;
* entradas inválidas não devem ser silenciosamente convertidas ou normalizadas;
* a análise não deve modificar os valores recebidos;
* o Market Regime deve descrever o contexto observado e não deve gerar, isoladamente, sinais de compra ou venda;
* o Market Regime não deve produzir probabilidades, previsões de movimento futuro ou decisões de trading;
* a interpretação conjunta de pressão, múltiplos timeframes, confluências, contradições, confiança e probabilidade permanece responsabilidade de componentes posteriores do sistema.

### Anomaly Detection Engine

Responsável por medir estatisticamente o quanto um valor atual se desvia de seu comportamento histórico, fornecendo evidências quantitativas de comportamento fora do padrão sem transformar essa primeira camada em classificação arbitrária, previsão ou sinal de trading.

Para a primeira definição de Anomaly Detection:

* `historical_values` representa a janela histórica utilizada como referência estatística;
* `current_value` representa o valor atual que será comparado com essa referência;
* o valor atual não deve participar do cálculo de sua própria referência histórica;
* `mean` deve representar a média aritmética dos valores históricos;
* `standard_deviation` deve utilizar o desvio-padrão populacional da janela histórica;
* a variância deve ser calculada dividindo a soma dos desvios quadráticos pela quantidade total de valores históricos;
* `deviation` deve ser calculado como `current_value - mean`;
* `z_score` deve ser calculado como `deviation / standard_deviation`;
* Z-score positivo representa um valor atual acima da média histórica;
* Z-score negativo representa um valor atual abaixo da média histórica;
* Z-score igual a zero representa um valor atual igual à média histórica;
* esta primeira camada não deve utilizar thresholds arbitrários para decidir automaticamente se um valor constitui uma anomalia;
* valores como `2`, `-2`, `3` ou `-3` não devem ser tratados isoladamente como limites universais de anomalia;
* a interpretação posterior da magnitude do Z-score deve permanecer separada do cálculo estatístico;
* valores históricos positivos, negativos e iguais a zero são permitidos;
* `current_value` também pode ser positivo, negativo ou igual a zero;
* `historical_values` deve ser uma lista não vazia;
* todos os valores históricos devem ser numéricos;
* `current_value` deve ser numérico;
* booleanos não devem ser aceitos como valores numéricos válidos;
* históricos com desvio-padrão igual a zero devem ser rejeitados, pois o Z-score não pode ser calculado nessa condição;
* os valores históricos recebidos não devem ser modificados;
* a análise deve ser determinística para as mesmas entradas;
* `VolumeAnomaly` permanece um componente independente responsável pela razão entre volume atual e volume de referência;
* o `AnomalyDetector` não substitui métricas específicas de domínio, como volume anomaly, volatilidade, order book imbalance ou estrutura de mercado;
* o componente deve fornecer contexto estatístico que possa posteriormente alimentar mecanismos de inteligência, calibração, análise histórica e backtesting;
* o cálculo deve utilizar somente valores históricos disponíveis antes do valor atual, preservando causalidade temporal e evitando look-ahead bias;
* o componente não deve gerar sinais de compra ou venda;
* o componente não deve produzir probabilidades de movimento futuro;
* o componente não deve decidir direção futura do preço;
* classificação de anomalias, calibração de thresholds, combinação com outras evidências, confiança e interpretação preditiva permanecem responsabilidades de componentes posteriores do sistema.

### Market Pressure Engine

Responsável por combinar múltiplas evidências de pressão compradora ou vendedora.

### Intelligence Engine

Responsável por transformar evidências produzidas pelas camadas analíticas em scores normalizados, medir concordâncias e contradições e posteriormente combinar essas evidências sem transformar scores intermediários em probabilidades ou previsões não validadas.

Os primeiros scores do Intelligence Engine devem preservar a separação entre diferentes domínios de evidência:

* `TechnicalScore` representa evidências direcionais derivadas de indicadores técnicos;
* `FlowScore` representa evidências relacionadas ao fluxo comprador e vendedor observado;
* `MomentumScore` representa evidências relacionadas à direção, velocidade e aceleração do movimento do preço;
* `VolumeScore` representa evidências relacionadas à intensidade e anormalidade da atividade de volume, sem assumir automaticamente direção do preço;
* `StructureScore` representa evidências produzidas pela estrutura de mercado, rompimentos e contexto estrutural;
* métricas correlacionadas ou matematicamente derivadas umas das outras não devem ser tratadas automaticamente como evidências independentes;
* volatilidade, regime de mercado, análise multi-timeframe e contexto de anomalias não devem ser convertidos artificialmente em evidências direcionais quando sua semântica original não determina direção;
* combinação entre scores, confiança, contradições e interpretação conjunta permanecem responsabilidades das camadas posteriores do Intelligence Engine;
* pesos e thresholds não devem ser introduzidos arbitrariamente e deverão ser calibrados e validados posteriormente quando houver evidência histórica suficiente;
* todos os componentes devem preservar causalidade temporal e evitar look-ahead bias.

#### Technical Score

O componente `TechnicalScore` é responsável por agregar evidências técnicas direcionais que já tenham sido previamente transformadas para uma escala normalizada comum.

Para a primeira definição de Technical Score:

* `signals` deve ser uma lista não vazia de evidências técnicas normalizadas;
* cada sinal deve ser numérico e permanecer no intervalo inclusivo entre `-1.0` e `1.0`;
* valores negativos representam evidência técnica com inclinação bearish;
* valores positivos representam evidência técnica com inclinação bullish;
* zero representa evidência técnica neutra;
* os extremos `-1.0` e `1.0` são valores válidos;
* booleanos não devem ser aceitos como valores numéricos válidos;
* entradas não numéricas devem ser rejeitadas;
* sinais fora do intervalo permitido devem ser rejeitados;
* uma única evidência válida pode produzir um Technical Score;
* o score deve ser calculado pela média aritmética das evidências disponíveis;
* todas as evidências possuem o mesmo peso nesta primeira definição;
* pesos arbitrários não devem ser introduzidos;
* evidências ausentes não devem ser inventadas ou substituídas por valores artificiais;
* uma lista vazia não possui evidência suficiente para produzir um score e deve ser rejeitada;
* os sinais recebidos não devem ser modificados;
* o cálculo deve ser determinístico para as mesmas entradas;
* o resultado permanece no intervalo entre `-1.0` e `1.0`;
* o valor resultante representa evidência técnica agregada e não uma probabilidade de movimento futuro;
* por exemplo, um Technical Score igual a `0.6` não significa 60% de probabilidade de alta;
* o componente não deve calcular diretamente SMA, EMA, RSI, MACD ou outros indicadores;
* indicadores técnicos permanecem componentes independentes;
* a transformação de valores brutos de indicadores em sinais normalizados deve permanecer separada do agregador e poderá ser calibrada posteriormente;
* ATR e outras medidas de volatilidade não devem ser convertidos automaticamente em sinais bullish ou bearish, pois magnitude de volatilidade não determina direção;
* evidências de estrutura de mercado devem permanecer separadas para evitar sobreposição com o futuro `StructureScore`;
* evidências de fluxo, momentum e volume devem permanecer separadas para evitar dupla contagem entre os diferentes scores;
* o Technical Score não deve gerar sinais de compra ou venda;
* o Technical Score não deve produzir confiança;
* o Technical Score não deve produzir probabilidades;
* o Technical Score não deve realizar previsão do preço;
* calibração, pesos aprendidos, thresholds, confiança, contradições e combinação com outros scores permanecem responsabilidades de etapas posteriores do sistema.

#### Flow Score

O componente `FlowScore` é responsável por agregar evidências direcionais relacionadas ao fluxo de mercado que já tenham sido previamente transformadas para uma escala normalizada comum.

Para a primeira definição de Flow Score:

* `signals` deve ser uma lista não vazia de evidências de fluxo normalizadas;
* cada sinal deve ser numérico e permanecer no intervalo inclusivo entre `-1.0` e `1.0`;
* valores negativos representam evidência de fluxo com inclinação vendedora;
* valores positivos representam evidência de fluxo com inclinação compradora;
* zero representa evidência de fluxo neutra ou equilibrada;
* os extremos `-1.0` e `1.0` são valores válidos;
* booleanos não devem ser aceitos como valores numéricos válidos;
* entradas não numéricas devem ser rejeitadas;
* sinais fora do intervalo permitido devem ser rejeitados;
* uma única evidência válida pode produzir um Flow Score;
* o score deve ser calculado pela média aritmética das evidências disponíveis;
* todas as evidências possuem o mesmo peso nesta primeira definição;
* pesos arbitrários não devem ser introduzidos;
* evidências ausentes não devem ser inventadas ou substituídas por valores artificiais;
* uma lista vazia não possui evidência suficiente para produzir um score e deve ser rejeitada;
* os sinais recebidos não devem ser modificados;
* o cálculo deve ser determinístico para as mesmas entradas;
* o resultado permanece no intervalo entre `-1.0` e `1.0`;
* o valor resultante representa evidência agregada de fluxo e não uma probabilidade de movimento futuro;
* por exemplo, um Flow Score igual a `0.6` não significa 60% de probabilidade de alta;
* o componente não deve calcular diretamente Buy Volume, Sell Volume, Buy/Sell Ratio, Volume Delta ou Order Book Imbalance;
* métricas de fluxo permanecem componentes independentes;
* a transformação de métricas brutas de fluxo em sinais normalizados deve permanecer separada do agregador e poderá ser calibrada posteriormente;
* Buy/Sell Ratio e Volume Delta derivam dos mesmos volumes de compra e venda e não devem ser tratados automaticamente como evidências independentes, evitando dupla contagem da mesma informação;
* Order Book Imbalance representa o desequilíbrio observado entre liquidez bid e ask e não deve ser interpretado isoladamente como previsão do movimento futuro do preço;
* evidências técnicas, de momentum, volume e estrutura devem permanecer separadas para evitar sobreposição entre os diferentes scores;
* o Flow Score não deve gerar sinais de compra ou venda;
* o Flow Score não deve produzir confiança;
* o Flow Score não deve produzir probabilidades;
* o Flow Score não deve realizar previsão do preço;
* calibração, pesos aprendidos, thresholds, confiança, contradições e combinação com outros scores permanecem responsabilidades de etapas posteriores do sistema.

#### Momentum Score

O componente `MomentumScore` é responsável por agregar evidências direcionais relacionadas ao momentum do preço que já tenham sido previamente transformadas para uma escala normalizada comum.

Para a primeira definição de Momentum Score:

* `signals` deve ser uma lista não vazia de evidências de momentum normalizadas;
* cada sinal deve ser numérico e permanecer no intervalo inclusivo entre `-1.0` e `1.0`;
* valores negativos representam evidência de momentum com inclinação bearish;
* valores positivos representam evidência de momentum com inclinação bullish;
* zero representa evidência de momentum neutra;
* os extremos `-1.0` e `1.0` são valores válidos;
* booleanos não devem ser aceitos como valores numéricos válidos;
* entradas não numéricas devem ser rejeitadas;
* sinais fora do intervalo permitido devem ser rejeitados;
* uma única evidência válida pode produzir um Momentum Score;
* o score deve ser calculado pela média aritmética das evidências disponíveis;
* todas as evidências possuem o mesmo peso nesta primeira definição;
* pesos arbitrários não devem ser introduzidos;
* evidências ausentes não devem ser inventadas ou substituídas por valores artificiais;
* uma lista vazia não possui evidência suficiente para produzir um score e deve ser rejeitada;
* os sinais recebidos não devem ser modificados;
* o cálculo deve ser determinístico para as mesmas entradas;
* o resultado permanece no intervalo entre `-1.0` e `1.0`;
* o valor resultante representa evidência agregada de momentum e não uma probabilidade de movimento futuro;
* por exemplo, um Momentum Score igual a `0.6` não significa 60% de probabilidade de alta;
* o componente não deve calcular diretamente Price Velocity ou Price Acceleration;
* métricas de momentum permanecem componentes independentes;
* a transformação de valores brutos de velocity e acceleration em sinais normalizados deve permanecer separada do agregador e poderá ser calibrada posteriormente;
* Price Acceleration deriva da mudança de Price Velocity ao longo do tempo e sua relação deve ser considerada ao construir evidências para evitar dupla contagem inadequada;
* velocity positiva com acceleration negativa pode representar movimento ainda positivo, porém desacelerando, e não deve ser automaticamente interpretada como erro ou contradição;
* evidências técnicas, de fluxo, volume e estrutura devem permanecer separadas para evitar sobreposição entre os diferentes scores;
* o Momentum Score não deve gerar sinais de compra ou venda;
* o Momentum Score não deve produzir confiança;
* o Momentum Score não deve produzir probabilidades;
* o Momentum Score não deve realizar previsão do preço;
* calibração, pesos aprendidos, thresholds, confiança, contradições e combinação com outros scores permanecem responsabilidades de etapas posteriores do sistema.

#### Volume Score

O componente `VolumeScore` é responsável por agregar evidências relacionadas à intensidade de volume que já tenham sido previamente transformadas para uma escala normalizada comum.

Diferentemente de Technical Score, Flow Score e Momentum Score, o Volume Score não representa direção bullish ou bearish. Volume representa principalmente intensidade e participação de mercado, portanto sua escala normalizada permanece entre `0.0` e `1.0`.

Para a primeira definição de Volume Score:

* `signals` deve ser uma lista não vazia de evidências de volume normalizadas;
* cada sinal deve ser numérico e permanecer no intervalo inclusivo entre `0.0` e `1.0`;
* `0.0` representa a menor intensidade dentro da escala normalizada;
* `1.0` representa a maior intensidade dentro da escala normalizada;
* valores intermediários representam níveis intermediários de intensidade;
* booleanos não devem ser aceitos como valores numéricos válidos;
* entradas não numéricas devem ser rejeitadas;
* sinais fora do intervalo permitido devem ser rejeitados;
* uma única evidência válida pode produzir um Volume Score;
* o score deve ser calculado pela média aritmética das evidências disponíveis;
* todas as evidências possuem o mesmo peso nesta primeira definição;
* pesos arbitrários não devem ser introduzidos;
* evidências ausentes não devem ser inventadas ou substituídas por valores artificiais;
* uma lista vazia não possui evidência suficiente para produzir um score e deve ser rejeitada;
* os sinais recebidos não devem ser modificados;
* o cálculo deve ser determinístico para as mesmas entradas;
* o resultado permanece no intervalo entre `0.0` e `1.0`;
* o Volume Score não possui sinal direcional;
* um Volume Score alto não significa evidência bullish;
* um Volume Score baixo não significa evidência bearish;
* por exemplo, um Volume Score igual a `0.9` não significa 90% de probabilidade de alta, queda ou qualquer outro movimento futuro;
* o componente não deve calcular diretamente Volume Anomaly ou z-score;
* métricas brutas de volume e detecção de anomalias permanecem componentes independentes;
* a transformação de Volume Anomaly, z-score ou outras métricas de volume em sinais normalizados entre `0.0` e `1.0` deve permanecer separada do agregador e poderá ser calibrada posteriormente;
* `VolumeAnomaly` e um `AnomalyDetector` aplicado aos mesmos dados de volume não devem ser automaticamente tratados como evidências independentes, pois podem representar diferentes transformações do mesmo fenômeno subjacente;
* direção de preço ou pressão compradora/vendedora não deve ser inferida exclusivamente a partir da intensidade de volume;
* evidências técnicas, de fluxo, momentum e estrutura devem permanecer separadas para evitar sobreposição entre os diferentes scores;
* o Volume Score não deve gerar sinais de compra ou venda;
* o Volume Score não deve produzir confiança;
* o Volume Score não deve produzir probabilidades;
* o Volume Score não deve realizar previsão do preço;
* calibração, normalização de métricas brutas, pesos aprendidos, thresholds, confiança, contradições e combinação com outros scores permanecem responsabilidades de etapas posteriores do sistema.

#### Structure Score

O componente `StructureScore` é responsável por agregar evidências direcionais relacionadas à estrutura de mercado que já tenham sido previamente transformadas para uma escala normalizada comum e preparadas para evitar dupla contagem de informações estruturalmente relacionadas.

Para a primeira definição de Structure Score:

* `signals` deve ser uma lista não vazia de evidências estruturais normalizadas;
* cada sinal deve ser numérico e permanecer no intervalo inclusivo entre `-1.0` e `1.0`;
* valores negativos representam evidência estrutural com inclinação bearish;
* valores positivos representam evidência estrutural com inclinação bullish;
* zero representa evidência estrutural neutra ou balanceada;
* os extremos `-1.0` e `1.0` são valores válidos;
* booleanos não devem ser aceitos como valores numéricos válidos;
* entradas não numéricas devem ser rejeitadas;
* sinais fora do intervalo permitido devem ser rejeitados;
* uma única evidência válida pode produzir um Structure Score;
* o score deve ser calculado pela média aritmética das evidências disponíveis;
* todas as evidências possuem o mesmo peso nesta primeira definição;
* pesos arbitrários não devem ser introduzidos;
* evidências ausentes não devem ser inventadas ou substituídas por valores artificiais;
* uma lista vazia não possui evidência suficiente para produzir um score e deve ser rejeitada;
* os sinais recebidos não devem ser modificados;
* o cálculo deve ser determinístico para as mesmas entradas;
* o resultado permanece no intervalo entre `-1.0` e `1.0`;
* o valor resultante representa evidência estrutural agregada e não uma probabilidade de movimento futuro;
* por exemplo, um Structure Score igual a `0.7` não significa 70% de probabilidade de alta;
* o componente não deve classificar diretamente pontos estruturais como HH, HL, LH ou LL;
* o componente não deve detectar diretamente tendência estrutural;
* o componente não deve detectar diretamente Break of Structure;
* o componente não deve detectar diretamente mudanças de estrutura;
* Structural Point Classification, Structural Trend, Break of Structure e Structure Change permanecem componentes independentes de análise;
* HH, HL, LH e LL alimentam a interpretação da tendência estrutural e não devem ser automaticamente tratados como evidências independentes adicionais quando a mesma informação já estiver representada por uma evidência derivada;
* Break of Structure e Structure Change também podem representar informações relacionadas, pois Structure Change utiliza contexto estrutural e eventos de break;
* evidências estruturais relacionadas devem ser preparadas e deduplicadas antes de serem fornecidas ao agregador;
* a existência de múltiplas representações derivadas do mesmo evento estrutural não deve aumentar artificialmente a força do Structure Score;
* a transformação dos resultados estruturais brutos em sinais normalizados deve permanecer separada do agregador e poderá ser calibrada posteriormente;
* evidências técnicas, de fluxo, momentum e volume devem permanecer separadas das evidências estruturais;
* o Structure Score não deve gerar sinais de compra ou venda;
* o Structure Score não deve produzir confiança;
* o Structure Score não deve produzir probabilidades;
* o Structure Score não deve realizar previsão do preço;
* calibração, normalização, deduplicação, pesos aprendidos, thresholds, confiança, contradições e combinação com outros scores permanecem responsabilidades de etapas posteriores do sistema.

#### Confidence Engine

O componente `ConfidenceEngine` é responsável por agregar medidas de força de evidência que já tenham sido previamente transformadas para uma escala normalizada comum.

Nesta primeira definição, confidence representa a força agregada das evidências fornecidas ao componente. Confidence não representa direção, concordância entre sinais, ausência de contradição ou probabilidade calibrada de um movimento futuro.

Para a primeira definição do Confidence Engine:

* `signals` deve ser uma lista não vazia de medidas de força de evidência previamente normalizadas;
* cada sinal deve ser numérico e permanecer no intervalo inclusivo entre `0.0` e `1.0`;
* `0.0` representa a extremidade inferior da escala normalizada de força de evidência;
* `1.0` representa a extremidade superior da escala normalizada de força de evidência;
* os extremos `0.0` e `1.0` são valores válidos;
* booleanos não devem ser aceitos como valores numéricos válidos;
* entradas não numéricas devem ser rejeitadas;
* sinais fora do intervalo permitido devem ser rejeitados;
* uma única evidência válida pode produzir confidence;
* confidence deve ser calculada pela média aritmética das evidências disponíveis;
* todas as evidências possuem o mesmo peso nesta primeira definição;
* pesos arbitrários não devem ser introduzidos;
* evidências ausentes não devem ser inventadas ou substituídas por valores artificiais;
* uma lista vazia não possui evidência suficiente para produzir confidence e deve ser rejeitada;
* os sinais recebidos não devem ser modificados;
* o cálculo deve ser determinístico para as mesmas entradas;
* o resultado permanece no intervalo entre `0.0` e `1.0`;
* o valor resultante representa força agregada das evidências normalizadas fornecidas ao componente;
* por exemplo, confidence igual a `0.8` não significa 80% de probabilidade de alta, queda ou acerto;
* confidence não representa direção bullish ou bearish;
* confidence não representa concordância entre evidências direcionais;
* confidence não representa ausência de contradição;
* evidências fortes podem existir simultaneamente em direções opostas;
* contradição entre evidências permanece responsabilidade do `ContradictionEngine`;
* scores direcionais não devem ser convertidos automaticamente para confidence por meio de valor absoluto dentro do `ConfidenceEngine`;
* a transformação de resultados brutos ou scores direcionais em medidas normalizadas de força deve permanecer separada do agregador;
* evidências correlacionadas não devem ser automaticamente tratadas como fontes independentes adicionais de confiança;
* a existência de múltiplas representações derivadas da mesma informação não deve aumentar artificialmente confidence;
* Volume Score permanece uma medida de intensidade e não deve ser interpretado automaticamente como confidence;
* Technical Score, Flow Score, Momentum Score e Structure Score permanecem medidas direcionais independentes do Confidence Engine;
* o Confidence Engine não deve gerar direção de mercado;
* o Confidence Engine não deve gerar sinais de compra ou venda;
* o Confidence Engine não deve produzir probabilidades;
* o Confidence Engine não deve realizar previsão do preço;
* calibração estatística, transformação de scores em medidas de força, deduplicação de evidências, pesos aprendidos e probabilidades permanecem responsabilidades de etapas posteriores do sistema.

A separação conceitual adotada pelo sistema é:

* direção representa qual lado as evidências direcionais favorecem;
* confidence representa força agregada das evidências normalizadas fornecidas;
* contradiction representa o grau de conflito entre evidências direcionais e permanece uma dimensão separada;
* probability exige calibração estatística contra resultados observados e não deve ser inferida diretamente de confidence.

#### Contradiction Engine

O componente `ContradictionEngine` é responsável por medir a intensidade da oposição entre evidências direcionais que já tenham sido previamente normalizadas para uma escala comum.

Nesta primeira definição, contradiction representa a força agregada do conflito entre evidências bullish e bearish. Contradiction não representa direção, confidence, probabilidade ou previsão de movimento futuro.

Para a primeira definição do Contradiction Engine:

* `signals` deve ser uma lista não vazia de evidências direcionais previamente normalizadas;
* cada sinal deve ser numérico e permanecer no intervalo inclusivo entre `-1.0` e `1.0`;
* valores positivos representam evidência direcional bullish;
* valores negativos representam evidência direcional bearish;
* zero representa evidência direcional neutra;
* os extremos `-1.0` e `1.0` são valores válidos;
* booleanos não devem ser aceitos como valores numéricos válidos;
* entradas não numéricas devem ser rejeitadas;
* sinais fora do intervalo permitido devem ser rejeitados;
* uma única evidência válida pode ser analisada e produz contradiction igual a zero, pois não existe uma evidência oposta concorrente;
* uma lista vazia não possui evidência suficiente para análise e deve ser rejeitada;
* os sinais recebidos não devem ser modificados;
* o cálculo deve ser determinístico para as mesmas entradas;
* a força bullish deve ser calculada pela soma das magnitudes positivas dividida pelo número total de sinais fornecidos;
* a força bearish deve ser calculada pela soma das magnitudes negativas absolutas dividida pelo número total de sinais fornecidos;
* contradiction deve ser calculada como duas vezes o menor valor entre a força bullish e a força bearish;
* o resultado permanece no intervalo entre `0.0` e `1.0`;
* `0.0` representa ausência de oposição direcional entre evidências;
* `1.0` representa oposição máxima possível entre evidências de magnitude máxima nesta definição;
* evidências alinhadas exclusivamente na mesma direção produzem contradiction igual a zero;
* evidências exclusivamente neutras produzem contradiction igual a zero;
* a presença de evidência direcional juntamente com evidência neutra não cria contradição por si só;
* oposição entre evidências fracas deve produzir contradiction menor do que oposição equivalente entre evidências fortes;
* sinais neutros reduzem a densidade agregada de evidência conflitante porque permanecem no denominador do cálculo;
* por exemplo, `[1.0, -1.0]` produz contradiction igual a `1.0`;
* por exemplo, `[0.1, -0.1]` produz contradiction igual a `0.1`;
* por exemplo, `[1.0, -1.0, 0.0, 0.0]` produz contradiction igual a `0.5`;
* por exemplo, `[0.9, 0.0]` produz contradiction igual a `0.0`;
* contradiction não deve ser inferida apenas pela existência de sinais com sinais matemáticos diferentes;
* magnitude das evidências deve participar da intensidade da contradição;
* o componente não deve introduzir thresholds arbitrários para decidir quando existe contradição;
* evidências correlacionadas ou derivadas da mesma informação não devem ser automaticamente tratadas como fontes independentes de conflito;
* evidências direcionais devem ser normalizadas, preparadas e deduplicadas antes de serem fornecidas ao componente;
* Technical Score, Flow Score, Momentum Score e Structure Score permanecem componentes direcionais separados;
* Volume Score permanece uma medida de intensidade e não deve ser utilizado automaticamente como evidência direcional pelo Contradiction Engine;
* Confidence Engine permanece responsável pela agregação de medidas normalizadas de força de evidência;
* contradiction e confidence são dimensões diferentes e podem apresentar valores elevados simultaneamente;
* o Contradiction Engine não deve decidir qual direção do mercado é favorecida;
* o Contradiction Engine não deve gerar sinais de compra ou venda;
* o Contradiction Engine não deve produzir confidence;
* o Contradiction Engine não deve produzir probabilidades;
* o Contradiction Engine não deve realizar previsão do preço;
* calibração estatística, pesos aprendidos, transformação de métricas brutas, probabilidades e interpretação preditiva permanecem responsabilidades de etapas posteriores do sistema.

A separação conceitual adotada pelo sistema permanece:

* direção representa qual lado as evidências direcionais favorecem;
* confidence representa força agregada das evidências normalizadas fornecidas;
* contradiction representa a intensidade da oposição entre evidências direcionais;
* probability exige calibração estatística contra resultados observados e não deve ser inferida diretamente de contradiction ou confidence.

#### Ensemble Engine

O componente `EnsembleEngine` é responsável por consolidar os scores produzidos pela camada de Intelligence Engine sem eliminar a separação semântica entre direção, intensidade, confidence e contradiction.

Nesta primeira definição, o Ensemble Engine não produz probabilidade, previsão de preço ou sinal operacional. Seu objetivo é fornecer uma representação consolidada e estruturada dos resultados já calculados pelos componentes especializados.

Para a primeira definição do Ensemble Engine:

* `technical_score`, `flow_score`, `momentum_score` e `structure_score` representam evidências direcionais previamente normalizadas;
* cada score direcional deve ser numérico, finito e permanecer no intervalo inclusivo entre `-1.0` e `1.0`;
* valores direcionais positivos representam evidência bullish;
* valores direcionais negativos representam evidência bearish;
* zero representa neutralidade direcional;
* `volume_score`, `confidence` e `contradiction` representam dimensões não direcionais separadas;
* cada score não direcional deve ser numérico, finito e permanecer no intervalo inclusivo entre `0.0` e `1.0`;
* booleanos não devem ser aceitos como valores numéricos válidos;
* valores não numéricos devem ser rejeitados;
* `NaN`, infinito positivo e infinito negativo devem ser rejeitados;
* valores fora dos intervalos definidos devem ser rejeitados;
* `direction_score` deve ser calculado pela média aritmética simples de `technical_score`, `flow_score`, `momentum_score` e `structure_score`;
* nenhum peso arbitrário deve ser aplicado aos scores direcionais nesta primeira definição;
* `volume_score` não deve alterar `direction_score`;
* `confidence` não deve alterar `direction_score`;
* `contradiction` não deve alterar `direction_score`;
* `volume_score`, `confidence` e `contradiction` devem ser preservados separadamente no resultado consolidado;
* scores direcionais equilibrados podem produzir `direction_score` igual a zero mesmo quando existe forte oposição entre as evidências;
* neutralidade direcional e contradição são conceitos distintos;
* `direction_score` igual a zero não implica automaticamente ausência de contradição;
* `direction_score` deve permanecer no intervalo entre `-1.0` e `1.0`;
* o resultado deve ser representado por `EnsembleResult`;
* `EnsembleResult` deve preservar `direction_score`, `volume_score`, `confidence` e `contradiction`;
* `EnsembleResult` deve ser imutável após sua criação;
* o cálculo deve ser determinístico para as mesmas entradas;
* o Ensemble Engine deve receber scores já calculados e normalizados, sem conhecer os detalhes internos dos indicadores ou analisadores que os produziram;
* o Ensemble Engine não deve recalcular RSI, MACD, médias móveis, fluxo, momentum, estrutura de mercado, volume ou qualquer outra métrica de nível inferior;
* o Ensemble Engine não deve transformar automaticamente volume em direção;
* o Ensemble Engine não deve transformar confidence em direção;
* o Ensemble Engine não deve utilizar contradiction como penalidade automática sobre direção;
* fórmulas como `direction × confidence`, `direction × volume` ou `direction × (1 - contradiction)` não devem ser introduzidas sem validação empírica;
* o Ensemble Engine não deve gerar sinais automáticos de compra ou venda;
* o Ensemble Engine não deve executar operações;
* o Ensemble Engine não deve interpretar seus resultados como probabilidades;
* o Ensemble Engine não deve prometer capacidade preditiva;
* pesos aprendidos, calibração estatística, probabilidades e interpretação preditiva permanecem responsabilidades de etapas posteriores do sistema.

A saída consolidada preserva quatro dimensões distintas:

* `direction_score` representa a direção agregada das evidências direcionais;
* `volume_score` representa intensidade ou participação de volume;
* `confidence` representa força agregada das evidências normalizadas fornecidas ao Confidence Engine;
* `contradiction` representa intensidade da oposição entre evidências direcionais.

A arquitetura mantém a seguinte separação:

* direção não é probabilidade;
* volume não é direção;
* confidence não é probabilidade;
* contradiction não é ausência de confidence;
* Ensemble não é previsão;
* probabilidade exige calibração estatística contra resultados observados em etapas posteriores.

### Prediction Lab

Responsável por registrar análises e previsões e verificar o que realmente aconteceu depois, preservando a separação entre estado observado, hipótese preditiva e resultado futuro.

#### Analysis Record

O componente `AnalysisRecord` representa um snapshot imutável das informações disponíveis no instante de referência de uma análise.

O registro preserva:

* `symbol`;
* `reference_timestamp`;
* `reference_price`;
* `technical_score`;
* `flow_score`;
* `momentum_score`;
* `structure_score`;
* `direction_score`;
* `volume_score`;
* `confidence`;
* `contradiction`.

Para o registro:

* `reference_timestamp` representa o instante máximo até o qual as informações utilizadas pela análise estavam disponíveis;
* `reference_price` representa o preço de referência da observação e deve ser positivo e finito;
* scores direcionais permanecem no intervalo `[-1.0, +1.0]`;
* `volume_score`, `confidence` e `contradiction` permanecem no intervalo `[0.0, 1.0]`;
* valores não numéricos, booleanos, `NaN` e infinitos são rejeitados quando aplicável;
* o registro é imutável após sua criação.

O `AnalysisRecord` não calcula scores e não transforma scores em previsões ou probabilidades. Ele preserva os valores produzidos anteriormente pelos componentes responsáveis por esses cálculos.

A separação conceitual inicial do Prediction Lab permanece:

`Analysis → Prediction → Outcome`

Analysis representa somente informações disponíveis no instante de referência. Prediction deverá representar uma hipótese registrada a partir dessas informações. Outcome deverá representar o que foi observado posteriormente.

Resultados futuros não podem ser utilizados na construção retroativa de uma análise. Informações estruturais ou multi-timeframe somente podem participar de uma análise quando já estiverem confirmadas e disponíveis até seu `reference_timestamp`.

Probabilidade não deve ser inferida diretamente de `direction_score`, `confidence`, `volume_score` ou `contradiction`. A transformação de evidências em probabilidades exigirá validação e calibração estatística contra resultados observados.

#### Analysis Registry

O componente `AnalysisRegistry` é responsável por registrar objetos `AnalysisRecord` durante a execução do Prediction Lab.

O registro segue as seguintes regras:

* somente instâncias de `AnalysisRecord` podem ser registradas;
* registros são preservados na ordem em que foram inseridos;
* o registry não reorganiza análises automaticamente por `reference_timestamp`;
* a coleção exposta aos consumidores é imutável por meio de uma `tuple`;
* registros com os mesmos valores são permitidos enquanto não existir uma regra formal de identidade;
* o registry não cria nem modifica `AnalysisRecord`;
* nenhuma regra de UUID, deduplicação ou identidade persistente é assumida nesta etapa.

O `AnalysisRegistry` é atualmente uma implementação em memória. Ele estabelece o comportamento de registro sem acoplar o Prediction Lab a MongoDB ou outra tecnologia de persistência.

Persistência durável, consultas especializadas e regras de identidade deverão ser introduzidas somente quando seus contratos forem definidos explicitamente.

#### Prediction Record

O componente `PredictionRecord` representa uma hipótese direcional imutável registrada no instante da previsão.

O registro preserva:

* `symbol`;
* `prediction_timestamp`;
* `reference_price`;
* `direction_score`.

Para o registro:

* `prediction_timestamp` representa o instante em que a hipótese foi registrada;
* `reference_price` representa o preço de referência no instante da previsão e deve ser positivo e finito;
* `direction_score` preserva a hipótese direcional contínua no intervalo `[-1.0, +1.0]`;
* valores não numéricos, booleanos, `NaN` e infinitos são rejeitados quando aplicável;
* o registro é imutável após sua criação.

O `direction_score` registrado não representa probabilidade, confiança, retorno esperado ou recomendação de trading. Nenhuma transformação automática para `BUY`, `SELL`, `LONG`, `SHORT`, bullish, bearish ou neutral é realizada nesta etapa.

O Prediction Lab não introduz thresholds direcionais arbitrários. A relação entre scores registrados e resultados futuros deverá ser avaliada empiricamente a partir dos outcomes observados.

O `PredictionRecord` também não contém outcomes futuros nem horizontes de avaliação. Uma mesma hipótese registrada em `t0` poderá posteriormente ser confrontada com resultados observados em diferentes horizontes temporais sem utilizar informação futura na construção da previsão.

#### Prediction Registry

O componente `PredictionRegistry` é responsável por registrar objetos `PredictionRecord` durante a execução do Prediction Lab.

O registro segue as seguintes regras:

* somente instâncias de `PredictionRecord` podem ser registradas;
* registros são preservados na ordem em que foram inseridos;
* o registry não reorganiza previsões automaticamente por `prediction_timestamp`;
* a coleção exposta aos consumidores é imutável por meio de uma `tuple`;
* registros com os mesmos valores são permitidos enquanto não existir uma regra formal de identidade;
* o registry não cria nem modifica `PredictionRecord`;
* nenhuma regra de UUID, deduplicação ou identidade persistente é assumida nesta etapa.

O `PredictionRegistry` é atualmente uma implementação em memória. Ele estabelece o comportamento de registro sem acoplar o Prediction Lab a MongoDB ou outra tecnologia de persistência.

O registry não calcula scores, probabilidades, outcomes ou sinais de trading. Sua responsabilidade é exclusivamente preservar as hipóteses já representadas por `PredictionRecord`.

#### Feature Snapshot

O componente `FeatureSnapshot` representa um snapshot imutável das features conhecidas em um instante específico do Prediction Lab.

O snapshot preserva:

* `symbol`;
* `feature_timestamp`;
* `features`.

O campo `features` representa um mapping entre nomes de features e valores numéricos escalares. O contrato não fixa antecipadamente um conjunto fechado de indicadores, permitindo que novas features sejam incorporadas sem alterar a estrutura fundamental do snapshot.

Para o snapshot:

* `feature_timestamp` representa o instante em que as features estavam disponíveis;
* pelo menos uma feature deve estar presente;
* nomes de features devem ser strings não vazias;
* valores de features devem ser numéricos e finitos;
* valores negativos, zero e positivos são permitidos porque cada feature preserva sua própria escala e semântica;
* booleanos, `NaN` e infinitos são rejeitados;
* o mapping de features é defensivamente copiado e exposto de forma imutável;
* alterações posteriores no mapping original não modificam o snapshot.

O `FeatureSnapshot` não impõe genericamente intervalos como `[0, 1]`, `[-1, 1]` ou `[0, 100]`, pois diferentes features possuem escalas distintas.

Somente informações disponíveis até `feature_timestamp` podem compor o snapshot. Outcomes futuros, preços futuros, retornos futuros ou qualquer informação derivada deles não pertencem às features, preservando a regra de zero look-ahead.

Estruturas complexas produzidas pelos motores de análise não são armazenadas diretamente neste primeiro contrato. Quando necessário, propriedades escalares semanticamente definidas poderão ser extraídas dessas estruturas e registradas como features.

#### Feature Registry

O componente `FeatureRegistry` mantém em memória os snapshots de features registrados pelo Prediction Lab.

O registry:

* aceita somente instâncias de `FeatureSnapshot`;
* preserva a ordem de registro dos snapshots;
* não reordena snapshots por `feature_timestamp`;
* expõe os snapshots registrados como uma `tuple`;
* permite o registro repetido do mesmo snapshot;
* não cria identidade, UUID ou chave artificial;
* não realiza deduplicação;
* não implementa filtros ou mecanismos de busca;
* não realiza persistência em banco de dados.

A responsabilidade do `FeatureRegistry` é somente preservar, em memória e na ordem de inserção, os snapshots de features capturados pelo Prediction Lab.

A imutabilidade de cada `FeatureSnapshot` continua sendo responsabilidade do próprio snapshot, enquanto o registry protege sua coleção interna ao não expor a lista mutável utilizada para armazenamento.

#### Prediction Outcome

O componente `PredictionOutcome` representa o resultado observado de uma previsão após um horizonte futuro definido.

O outcome preserva:

* `symbol`;
* `prediction_timestamp`;
* `reference_price`;
* `horizon_minutes`;
* `evaluation_timestamp`;
* `evaluation_price`.

O campo `future_return` é derivado diretamente dos preços:

`future_return = evaluation_price / reference_price - 1`

O retorno futuro não é recebido como entrada independente, evitando estados inconsistentes entre preços observados e retorno registrado.

Para o outcome:

* `symbol` identifica o ativo avaliado;
* `prediction_timestamp` representa o instante original da previsão;
* `reference_price` representa o preço conhecido no instante da previsão;
* `horizon_minutes` representa o horizonte futuro avaliado;
* `evaluation_timestamp` representa o instante da observação futura;
* `evaluation_price` representa o preço observado nessa avaliação;
* `future_return` preserva o retorno contínuo observado entre o preço de referência e o preço de avaliação.

O `evaluation_timestamp` não pode ocorrer antes de:

`prediction_timestamp + horizon_minutes * 60_000`

A avaliação pode ocorrer exatamente no horizonte ou depois dele. O contrato não exige uma observação disponível exatamente no milissegundo-alvo, evitando acoplamento prematuro à resolução ou à fonte dos dados de mercado.

O `PredictionOutcome` registra o que aconteceu no mercado e não classifica a previsão como correta ou incorreta. Ele não define thresholds, categorias direcionais, probabilidades, lucro/prejuízo, taxas, alavancagem ou sinais de trading.

A comparação entre `direction_score` e `future_return` pertence à futura etapa de cálculo de métricas.

#### Outcome Evaluator

O componente `OutcomeEvaluator` cria um `PredictionOutcome` a partir de um `PredictionRecord` e de uma observação futura.

O evaluator reutiliza diretamente da previsão:

* `symbol`;
* `prediction_timestamp`;
* `reference_price`.

A avaliação fornece:

* `horizon_minutes`;
* `evaluation_timestamp`;
* `evaluation_price`.

O `OutcomeEvaluator` aceita somente instâncias de `PredictionRecord` e delega ao `PredictionOutcome` as validações relacionadas ao horizonte, timestamps e preços.

O evaluator não consulta diretamente fontes de mercado e não calcula métricas de acerto. Sua responsabilidade é transformar uma previsão existente e uma observação futura em um outcome validado.

Para o horizonte de 1 minuto, essa estrutura permite avaliar uma previsão somente quando a observação ocorre em `t0 + 1 minuto` ou depois desse limite.

O mesmo contrato foi validado explicitamente para os horizontes de 5, 15 e 30 minutos.

Para 5 minutos:

* uma avaliação anterior a `t0 + 300_000 ms` é rejeitada;
* uma avaliação exatamente em `t0 + 300_000 ms` é aceita;
* uma avaliação posterior ao limite também é aceita.

Para 15 minutos:

* uma avaliação anterior a `t0 + 900_000 ms` é rejeitada;
* uma avaliação exatamente em `t0 + 900_000 ms` é aceita;
* uma avaliação posterior ao limite também é aceita.

Para 30 minutos:

* uma avaliação anterior a `t0 + 1_800_000 ms` é rejeitada;
* uma avaliação exatamente em `t0 + 1_800_000 ms` é aceita;
* uma avaliação posterior ao limite também é aceita;
* `future_return` continua sendo derivado dos preços de referência e avaliação.

As validações dos horizontes de 5, 15 e 30 minutos não exigem alterações adicionais no código de produção, confirmando que `PredictionOutcome` e `OutcomeEvaluator` permanecem independentes de um horizonte específico.

Com isso, o mesmo contrato de outcome está explicitamente validado para todos os horizontes atualmente definidos pelo Prediction Lab: 1, 5, 15 e 30 minutos.

#### Prediction Metrics

O componente `PredictionMetrics` representa um registro imutável das métricas calculadas para uma previsão avaliada em um horizonte específico.

O registro preserva:

* `symbol`;
* `prediction_timestamp`;
* `horizon_minutes`;
* `direction_score`;
* `future_return`;
* `directional_alignment`;
* `absolute_return`.

O `direction_score` continua representando somente a orientação direcional contínua registrada pela previsão, dentro do intervalo `[-1, +1]`.

O `future_return` preserva o retorno futuro observado pelo `PredictionOutcome` e não é convertido em categoria, probabilidade ou resultado de trading.

O `absolute_return` representa somente a magnitude absoluta do movimento observado:

`absolute_return = abs(future_return)`

O `directional_alignment` representa o alinhamento contínuo entre a orientação registrada pela previsão e o retorno futuro observado:

`directional_alignment = direction_score * future_return`

Valores positivos de `directional_alignment` indicam que `direction_score` e `future_return` possuem orientação compatível, enquanto valores negativos indicam orientação oposta. Valor zero pode resultar de uma previsão sem orientação direcional ou de retorno futuro igual a zero.

`directional_alignment` não representa accuracy, probabilidade, lucro, recomendação de trading ou classificação de uma previsão como correta ou incorreta.

O `PredictionMetrics` valida e preserva as métricas calculadas, mas não é responsável por derivá-las.

#### Metrics Calculator

O componente `MetricsCalculator` calcula `PredictionMetrics` a partir de um `PredictionRecord` e de um `PredictionOutcome` correspondente.

Antes do cálculo, prediction e outcome devem representar a mesma observação lógica. Para isso, devem possuir os mesmos:

* `symbol`;
* `prediction_timestamp`;
* `reference_price`.

Após essa validação, o calculator preserva o `direction_score` da previsão e o `future_return` do outcome e deriva:

* `absolute_return` como o valor absoluto de `future_return`;
* `directional_alignment` como o produto entre `direction_score` e `future_return`.

O cálculo permanece contínuo e não introduz thresholds direcionais arbitrários.

Nesta etapa, o Prediction Lab não transforma `direction_score` em probabilidade e não calcula `accuracy`, precision, recall, F1 score, P&L, ROI ou sinais `BUY`/`SELL`.

Métricas classificatórias e métricas de backtesting permanecem separadas até que seus contratos e critérios sejam definidos explicitamente nas fases apropriadas.

#### Statistical Report

O componente `StatisticalReport` representa um resumo estatístico imutável de múltiplos registros `PredictionMetrics` pertencentes ao mesmo horizonte temporal.

O relatório preserva:

* `horizon_minutes`;
* `sample_count`;
* `mean_direction_score`;
* `mean_future_return`;
* `mean_absolute_return`;
* `mean_directional_alignment`.

Cada média representa a agregação direta da métrica correspondente nas observações individuais.

O `mean_absolute_return` é calculado a partir da média dos valores `absolute_return` individuais e não como o valor absoluto de `mean_future_return`.

Da mesma forma, `mean_directional_alignment` é calculado a partir da média dos valores `directional_alignment` individuais e não como o produto entre `mean_direction_score` e `mean_future_return`.

O relatório permanece descritivo e não transforma essas estatísticas em probabilidade, accuracy, win rate, classificação de acerto ou erro, resultado financeiro ou recomendação de trading.

#### Statistical Report Generator

O componente `StatisticalReportGenerator` agrega uma coleção não vazia de registros `PredictionMetrics` e produz um `StatisticalReport`.

Todos os registros fornecidos devem pertencer ao mesmo `horizon_minutes`.

Horizontes diferentes não são combinados automaticamente em uma única população estatística. Dessa forma, resultados de 1, 5, 15 e 30 minutos permanecem separados e podem ser analisados independentemente.

Para uma coleção com `N` observações, o generator calcula:

`mean_direction_score = Σ direction_score / N`

`mean_future_return = Σ future_return / N`

`mean_absolute_return = Σ absolute_return / N`

`mean_directional_alignment = Σ directional_alignment / N`

O generator não cria thresholds direcionais, não classifica previsões como corretas ou incorretas e não calcula métricas de backtesting.

Com isso, o fluxo estatístico do Prediction Lab passa a ser:

`PredictionRecord -> PredictionOutcome -> PredictionMetrics -> StatisticalReportGenerator -> StatisticalReport`

Métricas classificatórias como accuracy, precision, recall e confusion matrix permanecem responsabilidade da fase de Backtesting.

### Backtesting

Responsável por avaliar historicamente o comportamento do sistema a partir de observações registradas, preservando a separação temporal entre informações disponíveis no momento da previsão e resultados observados posteriormente.

#### Backtest Sample

O componente `BacktestSample` representa uma observação histórica imutável utilizada pelo Backtesting.

Cada amostra associa:

* um `FeatureSnapshot`, contendo as features disponíveis no momento de referência;
* um `PredictionRecord`, contendo a hipótese direcional registrada naquele mesmo momento;
* um `PredictionOutcome`, contendo o resultado de mercado observado posteriormente para um horizonte específico.

Para que os componentes representem a mesma observação histórica:

* `FeatureSnapshot.symbol`, `PredictionRecord.symbol` e `PredictionOutcome.symbol` devem corresponder;
* `FeatureSnapshot.feature_timestamp` deve corresponder a `PredictionRecord.prediction_timestamp`;
* `PredictionRecord.prediction_timestamp` deve corresponder a `PredictionOutcome.prediction_timestamp`;
* `PredictionRecord.reference_price` deve corresponder a `PredictionOutcome.reference_price`.

O `PredictionOutcome` permanece separado das features e representa informação futura utilizada somente para avaliação histórica.

O `BacktestSample` não calcula métricas, não classifica previsões como corretas ou incorretas, não gera sinais de trading e não executa simulações.

#### Backtest Dataset

O componente `BacktestDataset` representa uma coleção histórica imutável e não vazia de registros `BacktestSample`.

O dataset:

* aceita somente coleções `list` ou `tuple`;
* aceita somente instâncias de `BacktestSample`;
* converte defensivamente a coleção recebida para uma `tuple`;
* preserva a ordem das amostras recebidas;
* preserva amostras repetidas;
* pode conter múltiplos símbolos;
* pode conter múltiplos horizontes de avaliação.

Nesta camada, o dataset não reordena observações por timestamp, não remove duplicatas, não agrupa símbolos ou horizontes e não executa lógica de simulação.

A presença de um outcome futuro dentro de uma amostra não o torna informação disponível para a geração das features ou da previsão. A separação entre dados disponíveis em `t0` e resultados conhecidos posteriormente deve ser preservada pelos componentes de Backtesting.

Controles adicionais de execução temporal e prevenção explícita de look-ahead bias permanecem responsabilidade das etapas posteriores da fase de Backtesting.

#### Backtest Simulator

O componente `BacktestSimulator` executa a avaliação histórica das previsões registradas em um `BacktestDataset`.

Para cada `BacktestSample`, o simulator utiliza o `PredictionRecord` e o `PredictionOutcome` correspondentes e delega o cálculo ao `MetricsCalculator`.

O resultado de `run()` é uma `tuple` de registros `PredictionMetrics`, preservando a ordem das amostras recebidas pelo dataset.

O simulator:

* aceita somente uma instância de `BacktestDataset`;
* avalia todas as amostras presentes no dataset;
* preserva a ordem das amostras;
* suporta múltiplos símbolos;
* suporta múltiplos horizontes de avaliação;
* preserva amostras repetidas como avaliações correspondentes;
* não modifica o dataset recebido;
* reutiliza o `MetricsCalculator` como fonte única das fórmulas de avaliação.

O `FeatureSnapshot` permanece preservado como contexto histórico da amostra, mas não é utilizado pelo simulator para recalcular a previsão. O `PredictionRecord` representa a hipótese que já havia sido registrada no momento de referência.

O `BacktestSimulator` não gera previsões, não recalcula features, não cria sinais `BUY` ou `SELL`, não simula capital, posições, taxas, leverage, P&L ou ROI e não calcula accuracy, precision, recall ou confusion matrix.

O fluxo inicial de Backtesting passa a ser:

`BacktestDataset -> BacktestSimulator -> MetricsCalculator -> PredictionMetrics`

A prevenção explícita de look-ahead bias durante a execução histórica permanece responsabilidade da próxima etapa da fase de Backtesting.

#### Look-Ahead Guard

O componente `LookAheadGuard` estabelece uma fronteira explícita de causalidade temporal para a execução histórica do Backtesting.

Antes de uma amostra ser avaliada pelo `MetricsCalculator`, o `BacktestSimulator` executa `LookAheadGuard.validate()` sobre o `BacktestSample`.

O Guard valida que:

* o objeto recebido é uma instância de `BacktestSample`;
* `FeatureSnapshot.feature_timestamp` corresponde a `PredictionRecord.prediction_timestamp`;
* `PredictionOutcome.evaluation_timestamp` não ocorre antes de `PredictionRecord.prediction_timestamp + horizon_minutes`.

O fluxo de avaliação passa a ser:

`BacktestDataset -> BacktestSimulator -> LookAheadGuard -> MetricsCalculator -> PredictionMetrics`

A validação ocorre antes do cálculo das métricas de cada amostra.

O `LookAheadGuard` não modifica features, predictions ou outcomes, não calcula métricas e não gera previsões ou sinais de trading.

A proteção fornecida nesta camada é temporal. O Guard não tenta inferir semanticamente se o valor de uma feature foi calculado utilizando informação futura. A causalidade da geração das features continua dependendo da pipeline responsável por construí-las, que deve utilizar somente informações disponíveis e confirmadas até `feature_timestamp`.

A presença de `PredictionOutcome` no `BacktestSample` existe exclusivamente para avaliação histórica e não torna o outcome disponível para a geração do `FeatureSnapshot` ou do `PredictionRecord`.

#### Accuracy Calculator

O componente `AccuracyCalculator` calcula a acurácia direcional histórica a partir de uma coleção de `PredictionMetrics`.

A classificação utiliza exclusivamente o sinal de `directional_alignment`, sem introduzir thresholds arbitrários de magnitude:

* `directional_alignment > 0` representa uma observação direcional alinhada;
* `directional_alignment < 0` representa uma observação direcional oposta;
* `directional_alignment == 0` representa uma observação neutra e não entra no denominador da acurácia.

A métrica é calculada como:

`accuracy = aligned / (aligned + opposed)`

O resultado pertence ao intervalo `[0, 1]`.

Observações com `direction_score == 0` ou `future_return == 0` produzem `directional_alignment == 0` e são excluídas do cálculo da acurácia.

O componente aceita coleções `list` ou `tuple` de `PredictionMetrics`, pode avaliar múltiplos símbolos e horizontes na coleção recebida e não realiza agrupamento ou filtragem automática.

Uma coleção vazia é inválida. Quando a coleção contém apenas observações neutras, a acurácia é considerada indefinida pelo contrato atual e o componente gera `ValueError`.

O `AccuracyCalculator` não recalcula `directional_alignment`, não introduz classificação de trading e não interpreta `direction_score`, `confidence` ou qualquer outra métrica como probabilidade.

#### Directional Classification

A camada de Backtesting possui uma classificação direcional compartilhada para métricas classificatórias históricas.

`DirectionalClassifier` recebe uma coleção de `PredictionMetrics` e produz um `DirectionalClassification` imutável contendo:

* `true_positive`;
* `false_positive`;
* `true_negative`;
* `false_negative`.

A classificação utiliza o sinal matemático de `direction_score` e `future_return`:

* `direction_score > 0` e `future_return > 0` -> true positive;
* `direction_score > 0` e `future_return < 0` -> false positive;
* `direction_score < 0` e `future_return < 0` -> true negative;
* `direction_score < 0` e `future_return > 0` -> false negative.

Observações com `direction_score == 0` ou `future_return == 0` são consideradas neutras e não entram nas quatro contagens.

Nenhum threshold de magnitude é aplicado. Valores positivos ou negativos diferentes de zero mantêm sua direção independentemente da magnitude.

O termo positive representa exclusivamente uma direção positiva na avaliação histórica. Ele não representa probabilidade, recomendação de compra ou sinal de trading.

O `DirectionalClassifier` aceita coleções `list` ou `tuple` de `PredictionMetrics`, preserva os objetos recebidos sem mutação e pode classificar múltiplos símbolos e horizontes sem agrupamento automático.

O `DirectionalClassification` apenas representa as contagens classificatórias e não calcula métricas derivadas. Uma classificação contendo zero em todas as quatro contagens é válida quando nenhuma observação da coleção é direcionalmente classificável.

Essa classificação é a base compartilhada para precision e para as futuras métricas de recall e confusion matrix, evitando definições independentes de TP, FP, TN e FN.

#### Precision Calculator

O componente `PrecisionCalculator` calcula a precisão das previsões direcionais positivas utilizando a classificação produzida pelo `DirectionalClassifier`.

A métrica é definida como:

`precision = true_positive / (true_positive + false_positive)`

True negatives, false negatives e observações neutras não participam do cálculo da precision.

O `PrecisionCalculator` delega a classificação ao `DirectionalClassifier` e não redefine as regras de TP, FP, TN ou FN.

Quando `true_positive + false_positive == 0`, não existem previsões positivas avaliáveis. Nesse caso, precision é considerada indefinida pelo contrato atual e o componente gera `ValueError`.

O resultado pertence ao intervalo `[0, 1]`.

O cálculo não introduz thresholds arbitrários, não interpreta `direction_score` como probabilidade e não produz sinais ou recomendações de trading.

#### Recall Calculator

O componente `RecallCalculator` calcula o recall das previsões direcionais positivas utilizando a classificação produzida pelo `DirectionalClassifier`.

A métrica é definida como:

`recall = true_positive / (true_positive + false_negative)`

False positives, true negatives e observações neutras não participam do cálculo do recall.

O `RecallCalculator` delega a classificação ao `DirectionalClassifier` e não redefine as regras de TP, FP, TN ou FN. Dessa forma, precision, recall e as futuras métricas baseadas em classificação compartilham exatamente o mesmo contrato classificatório.

Quando `true_positive + false_negative == 0`, não existem observações positivas classificáveis. Nesse caso, recall é considerado indefinido pelo contrato atual e o componente gera `ValueError`.

O resultado pertence ao intervalo `[0, 1]`.

O cálculo não introduz thresholds arbitrários, não interpreta `direction_score` como probabilidade e não produz sinais ou recomendações de trading.

#### Confusion Matrix Calculator

O componente `ConfusionMatrixCalculator` expõe a matriz de confusão da avaliação direcional histórica utilizando diretamente a classificação produzida pelo `DirectionalClassifier`.

O resultado é um `DirectionalClassification` imutável contendo:

* `true_positive`;
* `false_positive`;
* `true_negative`;
* `false_negative`.

O `ConfusionMatrixCalculator` delega integralmente a classificação ao `DirectionalClassifier` e retorna a própria instância de `DirectionalClassification` produzida por ele. O componente não redefine nem duplica as regras de TP, FP, TN ou FN.

A matriz utiliza o contrato classificatório compartilhado:

* `direction_score > 0` e `future_return > 0` -> true positive;
* `direction_score > 0` e `future_return < 0` -> false positive;
* `direction_score < 0` e `future_return < 0` -> true negative;
* `direction_score < 0` e `future_return > 0` -> false negative.

Observações com `direction_score == 0` ou `future_return == 0` permanecem neutras e não entram nas quatro contagens.

Uma coleção contendo somente observações neutras é válida e produz uma classificação com TP, FP, TN e FN iguais a zero. Diferentemente de precision e recall, a matriz de confusão não possui uma divisão que se torne indefinida nesse cenário.

Nenhum threshold de magnitude é aplicado. O componente aceita múltiplos símbolos e horizontes sem agrupamento automático e não introduz normalização, probabilidades, sinais ou recomendações de trading.

`PrecisionCalculator`, `RecallCalculator` e `ConfusionMatrixCalculator` compartilham o mesmo `DirectionalClassifier`, mantendo uma única definição de classificação direcional em toda a camada de Backtesting.

#### Model Comparison

A comparação de modelos do Backtesting é representada pelos componentes `ModelEvaluation` e `ModelComparator`.

`ModelEvaluation` é uma estrutura imutável que representa a avaliação histórica de um modelo identificado por nome. Ela contém:

* `model_name`;
* `sample_count`;
* `accuracy`;
* `precision`;
* `recall`;
* `confusion_matrix`.

`accuracy`, `precision` e `recall` pertencem ao intervalo `[0, 1]` quando definidas. Cada uma também pode ser `None` quando seu denominador matemático não existe para a amostra avaliada. `None` representa uma métrica indefinida e não equivale a `0.0`.

A `confusion_matrix` utiliza o `DirectionalClassification` compartilhado, preservando as contagens de true positive, false positive, true negative e false negative.

O `ModelComparator.evaluate()` avalia um conjunto de `PredictionMetrics` identificado por `model_name`. O componente reutiliza `AccuracyCalculator`, `PrecisionCalculator`, `RecallCalculator` e `ConfusionMatrixCalculator` em vez de duplicar suas fórmulas ou regras classificatórias.

A disponibilidade das métricas é determinada a partir da classificação direcional:

* accuracy é indefinida quando não existem observações direcionais classificadas;
* precision é indefinida quando não existem predicted positives;
* recall é indefinida quando não existem actual positives.

O `ModelComparator.compare()` recebe múltiplos modelos e retorna uma tupla imutável de `ModelEvaluation`, preservando a ordem fornecida pelo chamador.

Nesta fase, `model` representa uma estratégia ou versão identificável que produziu um conjunto de métricas históricas. O Backtesting não exige que esse modelo seja um modelo de Machine Learning.

A comparação é descritiva. O componente não ordena modelos por desempenho, não seleciona vencedor e não cria score composto, pesos arbitrários ou ranking automático.

A comparação também não introduz probabilidades, sinais de BUY/SELL, recomendações de trading, treinamento de modelos, hiperparâmetros ou seleção automática de modelos. Essas responsabilidades permanecem separadas da camada de Backtesting.

#### Feature Pipeline

- `FeaturePipeline` transforms `AnalysisRecord` instances into immutable `FeatureSnapshot` instances for Machine Learning.
- The pipeline preserves the analysis symbol and uses `reference_timestamp` as the feature timestamp.
- The initial feature set contains `technical_score`, `flow_score`, `momentum_score`, `structure_score`, `direction_score`, `volume_score`, `confidence`, and `contradiction`.
- `reference_price` is not included in the initial feature set.
- `build()` transforms one `AnalysisRecord`.
- `build_many()` transforms a non-empty list or tuple of `AnalysisRecord` instances and returns an ordered tuple of snapshots.
- Batch transformation preserves input order and does not sort, deduplicate, group, or otherwise reorganize observations.
- The pipeline does not create labels or targets, prepare training datasets, split datasets, train models, calculate probabilities, or access future outcomes.
- Feature generation remains tied to information available at the analysis reference time to preserve temporal causality and prevent leakage.
- Existing score semantics remain unchanged: directional scores are not probabilities, while confidence, contradiction, and volume retain their established meanings.

#### ML Dataset

- `MLSample` represents one immutable supervised-learning observation composed of a `FeatureSnapshot`, `horizon_minutes`, a continuous `target`, and `target_timestamp`.
- The initial target is the historical `PredictionOutcome.future_return`; it remains continuous and is not converted into UP/DOWN classes, binary labels, thresholds, or probabilities.
- `target_timestamp` represents the actual time at which the supervised target became observable and must be an integer timestamp at or after the nominal horizon end defined by `feature_timestamp + horizon_minutes`.
- Future outcome information is used only as the supervised target and its observation timestamp and is never added to the input feature mapping.
- `MLDatasetPreparer.prepare_sample()` pairs a `FeatureSnapshot` with a `PredictionOutcome` only when their symbols match and the feature timestamp matches the prediction timestamp.
- The sample horizon is preserved from the corresponding `PredictionOutcome`.
- `PredictionOutcome.evaluation_timestamp` is preserved as `MLSample.target_timestamp`, so downstream temporal validation uses the actual outcome observation time rather than reconstructing it only from the nominal horizon.
- `MLDataset` stores a non-empty immutable tuple of `MLSample` instances.
- Datasets may contain multiple symbols, multiple horizons, repeated observations, and preserve the caller-provided order.
- Dataset preparation does not sort, deduplicate, group, shuffle, normalize, scale, split, train models, create probabilities, or generate trading signals.
- `MLDatasetPreparer.prepare_dataset()` transforms a non-empty list or tuple of `(FeatureSnapshot, PredictionOutcome)` pairs into an `MLDataset` while reusing the single-sample compatibility validation.
- Train/validation/test separation remains a distinct responsibility of the next Machine Learning task.

### Machine Learning

#### Temporal Dataset Split

The machine learning dataset can be split into training, validation, and test partitions using `TemporalDatasetSplitter`.

The split is chronological and preserves the original sample order. The splitter does not shuffle, sort, deduplicate, or group samples automatically.

Split ratios are explicitly provided by the caller and must:

- be numeric, finite, and greater than zero;
- sum to `1.0`;
- produce non-empty training, validation, and test partitions.

The dataset must already be in chronological order by `FeatureSnapshot.feature_timestamp`. Equal feature timestamps are allowed within the same partition, supporting simultaneous samples such as different symbols or horizons, but the same feature timestamp cannot cross a train/validation or validation/test boundary.

`DatasetSplit` represents the immutable split result with three `MLDataset` partitions:

- `train`
- `validation`
- `test`

The splitter enforces both feature-time chronology and target-time availability across partition boundaries. Future outcomes remain supervised-learning targets and are never input features.

For target-time leakage protection:

- every training target must be observed strictly before the first validation feature timestamp;
- every validation target must be observed strictly before the first test feature timestamp;
- equality with the next partition's first feature timestamp is rejected;
- the latest `target_timestamp` across the entire preceding partition is used for validation rather than assuming that the last feature sample also has the latest target;
- overlapping target windows are rejected instead of being silently purged, reordered, or moved between partitions.

This protection uses the actual `MLSample.target_timestamp` propagated from `PredictionOutcome.evaluation_timestamp`, rather than inferring target availability only from the nominal prediction horizon.

The splitter does not introduce an automatic purge or configurable embargo interval. Instead, it rejects a requested split whenever the observed target timestamps would cross or touch the next partition's feature-time boundary.

No scaling, model training, probability calibration, trading threshold, BUY/SELL decision, or execution behavior is introduced by this component.

Será adicionado somente após a coleta de dados suficientes e validação da qualidade dos dados.

### Mean Return Baseline

The initial machine learning baseline is a regression baseline that predicts the mean training target independently for each `horizon_minutes`.

The baseline:

- fits only on `MLDataset` training samples;
- learns one mean `future_return` per observed horizon;
- keeps horizons independent instead of mixing their targets;
- rejects prediction before fitting;
- rejects horizons that were not observed during training;
- does not create directional classes, probabilities, thresholds, or trading signals.

Baseline evaluation is performed without refitting on validation or test data. `MeanReturnBaselineEvaluator` groups evaluation samples by `horizon_minutes`, uses the mean learned from the training dataset, and calculates regression metrics independently for each horizon.

The initial regression metrics are:

- MAE — Mean Absolute Error;
- MSE — Mean Squared Error;
- RMSE — Root Mean Squared Error.

`RegressionMetricsCalculator` is independent from the baseline so the same metric definitions can be reused by future machine learning models.

The baseline establishes a simple reference for determining whether later models provide predictive value beyond the historical mean training return for each horizon.

### Random Forest Regressor

The first trained machine learning model is a Random Forest regression model implemented with `scikit-learn`.

The model preserves the continuous regression target:

- input `X` comes exclusively from `FeatureSnapshot.features`;
- target `y` remains the continuous `future_return`;
- no UP/DOWN classes, probability estimates, thresholds, BUY/SELL signals, or trading actions are introduced.

`RandomForestReturnRegressor` trains one independent `RandomForestRegressor` per `horizon_minutes`. Horizons are therefore kept explicit instead of silently mixing targets from different prediction windows into the same model.

The feature schema is learned from the training dataset by feature name. Feature names are stored in deterministic sorted order so mapping insertion order does not affect the model input. All training samples must expose the same feature schema, and prediction snapshots must match the schema used during training.

The following metadata is intentionally excluded from the model feature vector:

- `symbol`;
- `feature_timestamp`;
- `target`;
- `target_timestamp`;
- `horizon_minutes`.

`horizon_minutes` selects the independently trained model and is not treated as an input feature.

The model validates its exposed `n_estimators` and `random_state` configuration and rejects prediction before fitting or prediction for horizons that were not observed during training.

`RandomForestReturnRegressorEvaluator` evaluates an already fitted model without retraining it. Validation and test samples are passed through the model using each sample's own feature snapshot and horizon.

Evaluation remains independent per horizon and reuses the shared regression metrics:

- MAE;
- MSE;
- RMSE.

This preserves the train/validation/test boundary and allows Random Forest performance to be compared with the Mean Return Baseline using the same continuous target and metric definitions.

The implementation uses `scikit-learn==1.9.1`.

### Traditional Rules Comparison

Traditional Intelligence Engine output and ML regression output are compared directionally per prediction horizon against the same observed future return.

The comparison preserves the original continuous values:
- `direction_score` for the traditional Intelligence Engine;
- `predicted_return` for the ML model;
- `future_return` as the observed outcome.

The traditional `direction_score` and ML `predicted_return` are not compared numerically because they have different semantics and units. Directional evaluation uses only their signs, without introducing arbitrary thresholds.

A positive value represents positive direction, a negative value represents negative direction, and an exact zero prediction is treated as neutral rather than silently classified as negative. Observed returns equal to zero are excluded from directional evaluation because they provide no positive or negative observed direction.

Directional accuracy is evaluated independently per horizon. Neutral predictions are tracked separately from evaluated directional predictions so accuracy is not interpreted without its prediction coverage.

The comparison layer is evaluation-only. It does not retrain models, create trading signals, select a winner automatically, or introduce capital, positions, fees, leverage, P&L, or strategy simulation.

### Return Ensemble

The initial ML ensemble combines compatible return regressors that predict the same continuous quantity: `future_return`.

The ensemble currently combines the trained Random Forest, XGBoost, and LightGBM return regressors through an unweighted arithmetic mean of their `predicted_return` values:

`ensemble_return = sum(model_predictions) / number_of_models`

The ensemble accepts two or more compatible regressors and does not assign arbitrary model weights. Each model receives the same `FeatureSnapshot` and prediction horizon, and each model is invoked exactly once per ensemble prediction.

The ensemble does not train or refit its component models. All regressors must be trained before they are provided to the ensemble, preserving the existing temporal training and evaluation boundaries.

Individual model predictions must remain finite numeric return values. Positive, negative, and exact-zero ensemble returns are preserved without being converted into classifications or probabilities.

The ensemble does not combine `direction_score` from the traditional Intelligence Engine with ML return predictions because those values have different semantics and scales. It also does not directly average calibrated directional probabilities with predicted returns.

The resulting `ensemble_return` remains a continuous predicted future return, not a probability, trading signal, position recommendation, or expected P&L.

Integration tests verify compatibility with the real Random Forest, XGBoost, and LightGBM regressors, including preservation of their horizon-specific prediction contracts.

## Phase 10 — Paper Trading

### Position Simulator

The paper trading layer introduces simulated position state without executing real exchange orders or interacting with live trading APIs.

`PositionSide` defines the supported simulated position directions:

- `LONG`
- `SHORT`

`SimulatedPosition` is an immutable domain object that preserves the initial state of a simulated position:

- `symbol`
- `side`
- `quantity`
- `entry_price`
- `entry_timestamp`

Symbols must be non-empty strings. Quantity and entry price must be finite positive numeric values, and the entry timestamp must be a non-negative integer.

`PositionSimulator` owns the current simulated position state. A newly created simulator starts without an open position:

- `current_position` is `None`
- `has_open_position` is `False`

The initial simulator deliberately does not register entries or exits. Those behaviors are implemented separately by the subsequent Paper Trading roadmap tasks.

The position model also does not yet contain exit price, exit timestamp, fees, slippage, leverage, realized P&L, or performance metrics. These concerns remain outside the initial position simulator scope.

The paper trading layer is simulation-only. `LONG` and `SHORT` represent simulated position directions and do not constitute trading recommendations or trigger real exchange execution.

### Simulated Entries

`PositionSimulator` can register a simulated entry when no position is currently open.

A simulated entry receives:

- `symbol`
- `side`
- `quantity`
- `entry_price`
- `entry_timestamp`

The simulator delegates domain validation to `SimulatedPosition` rather than duplicating position validation rules.

After a valid entry is registered:

- a new immutable `SimulatedPosition` is created
- `current_position` references that position
- `has_open_position` becomes `True`
- the created position is returned to the caller

A simulator supports only one open position at a time. Attempting to register another entry while a position is already open raises an error and preserves the existing position without modification.

If position validation fails, the invalid position is not registered and the simulator remains without an open position.

Entry registration remains simulation-only. It does not execute exchange orders, communicate with Binance, calculate fees or slippage, close positions, calculate P&L, or persist the position to a database.

## Tecnologias inicialmente previstas

### Backend

* Python
* asyncio
* WebSockets
* httpx
* Pydantic

### Dados

* NumPy
* Pandas
* possivelmente Polars

### Banco de dados

* MongoDB

### API

* FastAPI

### Frontend futuro

* React
* TypeScript
* Vite
* Tailwind CSS

### Machine Learning futuro

* scikit-learn
* XGBoost
* LightGBM
* PyTorch, somente se houver justificativa

### Testes

* pytest
* pytest-asyncio

### Infraestrutura

* Git
* GitHub
* Docker
* Docker Compose

## Estratégia de desenvolvimento

O sistema será construído por fases.

Primeiro:

dados -> processamento -> análise -> registro -> validação

Depois:

Machine Learning -> comparação -> ensemble

A interface gráfica será construída somente depois que o motor principal estiver funcionando.
