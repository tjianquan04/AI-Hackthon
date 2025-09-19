@echo off
echo.
echo ========================================
echo      🎯 STREAMLINED EDA DASHBOARD
echo ========================================
echo.
echo ✨ Optimized Features:
echo   • No duplicate insights
echo   • Consolidated EDA sections  
echo   • Clean, focused layout
echo   • Premium visual design
echo.
echo 📊 Key Components:
echo   • KPI Cards - Core metrics
echo   • Income Analysis - Churn by income
echo   • Age Demographics - Age-based patterns
echo   • Risk Insights - Top 3 drivers only
echo   • Customer Segments - Value-based pie chart
echo.
echo 🚫 Removed Duplications:
echo   • Executive Summary (consolidated into KPIs)
echo   • Repeated EDA insights
echo   • Customer detail tables
echo   • Footer analytics summary
echo.

cd UI
echo 📦 Installing dependencies...
call npm install --silent

echo.
echo 🚀 Starting Streamlined Dashboard...
echo 🌐 Access: http://localhost:3000
echo.
call npm start

pause

