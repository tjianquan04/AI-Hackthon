@echo off
echo 🚀 Starting Integrated Customer Churn Dashboard...
echo ================================================

echo.
echo 📊 Dashboard Features:
echo - Real EDA data from 10,127+ customers
echo - Live churn analytics and insights
echo - Interactive charts and visualizations
echo - Business-oriented explanations
echo.

cd UI
echo 📦 Installing dependencies...
call npm install

echo.
echo 🌐 Starting dashboard on http://localhost:3000
echo Press Ctrl+C to stop the dashboard
echo.
call npm start

pause


