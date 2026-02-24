@echo off
title Dashboard Servicos Nao Realizados - Streamlit
echo =============================================
echo   Iniciando Dashboard de Servicos...
echo =============================================
echo.

cd /d "c:\Users\gabriel.antonio\Desktop\Antigravity\Projeto Dashboard\Dash - Serviços não realizados"

echo Abrindo navegador em http://localhost:8502
timeout /t 3 /nobreak >nul
start http://localhost:8502

python -m streamlit run dashboard_servicos.py --server.port 8502 --server.headless true

pause
