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

### Prediction Lab

Responsável por registrar previsões e verificar o que realmente aconteceu depois.

### Machine Learning

Será adicionado somente após a coleta de dados suficientes e validação da qualidade dos dados.

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
