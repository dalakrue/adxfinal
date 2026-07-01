# Deployment instructions

1. Use Python 3.12 as declared by `.python-version` and `runtime.txt`.
2. Install dependencies: `python -m pip install -r requirements.txt`.
3. Run verification: `pytest -q tests/test_upgrade_20260626.py tests/test_requested_acceptance_20260626.py`.
4. Start locally: `streamlit run app.py`.
5. For Streamlit Cloud, set the main file path to `app.py` and deploy from the project root.
6. In Settings, use the single **Run Calculation + Open Lunch** action. Confirm the page routes to Lunch and all five surfaces show the same canonical identity.
7. Do not promote the shadow abstention threshold unless genuine out-of-sample promotion evidence passes every configured gate.
