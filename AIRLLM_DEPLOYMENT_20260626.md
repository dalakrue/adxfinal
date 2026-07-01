# AirLLM deployment

The independent **AI Assistant** tab is the only AirLLM owner. The former embedded Field 5 assistant and external NLP/OpenAI key form were removed.

Install with `pip install -r requirements-airllm.txt`, set `ADX_ENABLE_AIRLLM=1`, and set `ADX_AIRLLM_MODEL_ID` to a local model path or an explicitly approved model identifier. Downloads remain disabled unless `ADX_AIRLLM_ALLOW_DOWNLOAD=1`. The model is loaded lazily only after Send.
