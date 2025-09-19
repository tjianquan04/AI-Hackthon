@echo off
echo Starting Customer Churn Analytics Dashboard (Streamlit)
echo.
echo Installing/updating dependencies...
pip install -r requirements.txt

echo.
echo Starting Streamlit dashboard...
echo Dashboard will open at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the dashboard
echo.

streamlit run app.py


