@echo off
echo.
echo ========================================
echo    🏆 PREMIUM EDA ANALYTICS DASHBOARD
echo ========================================
echo.
echo 🎯 Features:
echo   • Executive Summary Dashboard
echo   • Real EDA insights from 10,127+ customers
echo   • Premium UI with gradient effects
echo   • Interactive business intelligence
echo   • No customer tables - pure analytics focus
echo.
echo 📊 Analytics Included:
echo   • Income-based churn analysis
echo   • Age demographic insights  
echo   • Strategic risk assessments
echo   • AI-powered recommendations
echo.

cd UI
echo 📦 Installing dependencies...
call npm install --silent

echo.
echo 🚀 Starting Premium Dashboard...
echo 🌐 Access: http://localhost:3000
echo.
echo Press Ctrl+C to stop
call npm start

pause

