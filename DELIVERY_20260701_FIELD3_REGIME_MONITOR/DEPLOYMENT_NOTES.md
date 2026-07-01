# Deployment Notes

1. Keep `app.py` as the Streamlit entry point used by the existing deployment.
2. Keep Python 3.12 as configured by the project.
3. Deploy the entire project folder so the three new modules and tests remain in their existing relative paths.
4. Use the existing Settings **Run Calculation + Open Lunch** action. The new Field 3 monitor is built in that transaction.
5. Open Lunch Field 3 after the run. Ordinary Streamlit reruns and display interactions read the saved payload and do not rebuild it.
6. The SQLite table `field3_regime_lifecycle_history_20260701` is created automatically in the existing project database.
7. A failed optional research dependency or model fit is isolated and reported as `FAILED_SAFELY`; it does not change the protected canonical decision.
8. Do not add API keys to source files. Continue using Streamlit deployment secrets.
