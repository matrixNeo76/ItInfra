@echo off
setlocal
echo ===============================================================================
echo   ITINFRA — AGGIORNAMENTO AUTOMATICO CLIENT
echo ===============================================================================
python "%~dp0scripts\itinfra_sync.py" %*
if %ERRORLEVEL% NEQ 0 (
    echo [ERRORE] Aggiornamento fallito o interrotto.
    exit /b %ERRORLEVEL%
)
echo ===============================================================================
echo   Allineamento completato con successo.
echo ===============================================================================
