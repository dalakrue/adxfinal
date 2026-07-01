# Implementation command — AirLLM + navigation + self-calculating Tables 4/5

## Required behavior
1. AirLLM Open/Closed widget, session execution flag, status metric, and submit path use one synchronized state contract.
2. AirLLM is lazy-loaded only after Send. The deterministic canonical assistant remains fallback when package/model/runtime fails.
3. Explicit navigation transactions are authoritative during rerun; Field 4–9, Field 456, and Field 789 must not fall back to Settings.
4. Table 4 calculates its own NLP, regime, data-mining, technical, sentiment, conflict, coverage, reliability, and decision columns.
5. Table 5 calculates integrated evidence from Table 4 components and must always return BUY, SELL, or WAIT.
6. Missing components contribute neutral zero and reduce coverage/reliability. They must not create N/A decision cells and must not be silently copied from another tab.

## Table 4 formulas
- NLP score = mean(normalized NLP/news/sentiment directions)
- Regime score = mean(normalized regime directions)
- Data-mining score = mean(normalized mining/pattern directions)
- Technical score = mean(normalized technical/decision/bias directions)
- Sentiment score = 0.50*NLP + 0.25*Regime + 0.25*DataMining
- Field4 score = 0.52*Technical + 0.28*Sentiment + 0.20*Regime
- Conflict = (maximum component score - minimum component score)/2, clipped 0..1
- Coverage = available component cells / expected component cells
- Reliability = Coverage * (1 - 0.55*Conflict)
- Decision = BUY/SELL/WAIT with a stricter threshold under low coverage

## Table 5 formulas
- Actionable evidence = Field4 score * Reliability * (1 - Conflict)
- BUY evidence = max(0, actionable)*10
- SELL evidence = max(0, -actionable)*10
- WAIT evidence = max(0, 1-|actionable|)*10
- Integrated decision = BUY/SELL/WAIT using a 0.10 action threshold

## Deployment
```powershell
cd "<PROJECT_FOLDER>"
python -m pip install -r requirements.txt
# AirLLM is an optional heavy server dependency:
python -m pip install -r requirements-airllm.txt
streamlit run app.py
```

For Streamlit Cloud, use Python 3.12 and set the main file to `app.py`. Install the optional AirLLM requirements only on a server with enough RAM/disk for the selected model. Configure a local model path or explicitly permit model download through the deployment environment.
