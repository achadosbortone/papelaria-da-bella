@echo off
chcp 65001 >nul
cd /d "%~dp0"

rem ===== PREENCHA AQUI (sem aspas e sem espacos sobrando) =====
set ML_CLIENT_ID=COLE_AQUI_O_APP_ID
set ML_CLIENT_SECRET=COLE_AQUI_A_SECRET_KEY
rem Deixe os dois abaixo vazios ate ser aprovado como afiliado
set ML_MATT_TOOL=
set ML_MATT_WORD=
rem =============================================================

where py >nul 2>nul
if %errorlevel%==0 (py gerar_site.py) else (python gerar_site.py)

echo.
echo ------------------------------------------------------------
echo Se acima aparece "Site gerado", envie para o GitHub os arquivos
echo da pasta docs: index.html e dados.json.
echo ------------------------------------------------------------
start "" "%~dp0docs"
pause
