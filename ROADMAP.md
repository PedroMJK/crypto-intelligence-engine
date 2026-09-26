# Roadmap — Crypto Intelligence Engine

## Status

Legenda:

* [ ] Not started
* [x] Completed
* [~] In progress

---

# Phase 0 — Planning

* [x] Define general objective
* [x] Define conceptual architecture
* [x] Define initial technologies
* [x] Define validation strategy
* [x] Create initial documentation

---

# Phase 1 — Foundation

* [x] Create Python virtual environment
* [x] Define Python version
* [x] Create requirements.txt
* [x] Create .gitignore
* [x] Create .env.example
* [x] Create project folder structure
* [x] Initialize Git
* [x] Create centralized configuration
* [x] Configure logging
* [x] Configure tests
* [x] Create first test

---

# Phase 2 — Market Data Engine

* [x] Create market data client
* [x] Connect WebSocket
* [x] Receive trades
* [x] Receive ticker
* [x] Receive candles
* [x] Receive order book
* [x] Validate incoming messages
* [x] Track event timestamps
* [x] Detect duplicated events
* [x] Detect out-of-order events
* [x] Implement reconnection
* [x] Implement exponential backoff
* [x] Implement error handling
* [x] Implement backpressure
* [x] Create data buffers
* [x] Track dropped messages
* [x] Track processing latency

---

# Phase 3 — Scanner

* [x] Get trading pairs
* [x] Filter relevant pairs
* [x] Create price filter
* [x] Create liquidity filter
* [x] Create volume filter
* [x] Create activity filter
* [x] Create ranking

---

# Phase 4 — Market Pressure Engine

* [x] Buy volume
* [x] Sell volume
* [x] Buy/Sell ratio
* [x] Volume delta
* [x] Trades per second
* [x] Price velocity
* [x] Price acceleration
* [x] Volume anomaly
* [x] Pressure score
* [x] Pressure transition

---

# Phase 5 — Advanced Analysis

* [x] Technical indicators
  * [x] Simple Moving Average (SMA)
  * [x] Exponential Moving Average (EMA)
  * [x] Relative Strength Index (RSI)
  * [x] Moving Average Convergence Divergence (MACD)
  * [x] Average True Range (ATR)
* [x] Market structure
  * [x] Swing High / Swing Low detection
  * [x] Structural point classification (HH, HL, LH, LL)
  * [x] Structural trend detection
  * [x] Break of Structure (BOS)
  * [x] Structure change detection
* [x] Support and resistance
  * [x] Support / resistance level detection
  * [x] Nearby level clustering
  * [x] Touch detection
  * [x] Level strength
  * [x] Level break detection
* [x] Volatility
* [x] Order book imbalance
* [x] Multi-timeframe analysis
* [x] Market regime
* [x] Anomaly detection

---

# Phase 6 — Intelligence Engine

* [x] Technical score
* [x] Flow score
* [x] Momentum score
* [x] Volume score
* [x] Structure score
* [x] Confidence engine
* [x] Contradiction engine
* [x] Ensemble engine

---

# Phase 7 — Prediction Lab

* [x] Register analyses
  * [x] Define immutable analysis record
  * [x] Add in-memory analysis registry
* [x] Register predictions
  * [x] Define immutable prediction record
  * [x] Add in-memory prediction registry
* [x] Save features
  * [x] Define immutable feature snapshot
  * [x] Add in-memory feature registry
* [x] Evaluate result after 1 minute
* [x] Evaluate result after 5 minutes
* [x] Evaluate result after 15 minutes
* [x] Evaluate result after 30 minutes
* [x] Calculate metrics
  * [x] Define immutable prediction metrics
  * [x] Add prediction metrics calculator
* [x] Create statistical report
  * [x] Define immutable statistical report
  * [x] Add statistical report generator

---

# Phase 8 — Backtesting

* [x] Create dataset
  * [x] Define immutable backtest sample
  * [x] Define immutable backtest dataset
* [x] Create simulator
  * [x] Add backtest simulator
* [x] Prevent look-ahead bias
  * [x] Add temporal look-ahead guard
  * [x] Integrate guard into backtest simulator
* [x] Calculate accuracy
* [x] Calculate precision
* [x] Calculate recall
* [x] Calculate confusion matrix
* [x] Compare models

---

# Phase 9 — Machine Learning

* [x] Create feature pipeline
* [x] Prepare dataset
* [x] Split training/validation/test datasets
* [x] Create baseline
* [x] Random Forest
* [x] XGBoost
* [x] LightGBM
* [x] Probability calibration
* [ ] Compare with traditional rules
* [ ] Create ensemble

---

# Phase 10 — Paper Trading

* [ ] Create position simulator
* [ ] Register simulated entries
* [ ] Register simulated exits
* [ ] Simulate fees
* [ ] Simulate slippage
* [ ] Create performance metrics

---

# Phase 11 — API

* [ ] FastAPI
* [ ] Endpoints
* [ ] Internal WebSocket
* [ ] Health check
* [ ] API documentation

---

# Phase 12 — Dashboard

* [ ] React
* [ ] TypeScript
* [ ] Tailwind
* [ ] Scanner
* [ ] Asset details
* [ ] Market Pressure
* [ ] Prediction Lab
* [ ] History
* [ ] Charts

---

# Phase 13 — Infrastructure

* [ ] Docker
* [ ] Docker Compose
* [ ] CI
* [ ] Automated tests
* [ ] Test environment deployment
* [ ] Monitoring

---

# Current Task

Compare with traditional rules.
