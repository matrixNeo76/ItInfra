@echo off
setlocal
set "BASEDIR=%~dp0"

if "%~1"=="" goto help
if "%~1"=="help" goto help
if "%~1"=="-h" goto help
if "%~1"=="--help" goto help

if /I "%~1"=="update" (
    python "%BASEDIR%scripts\itinfra_sync.py" %2 %3 %4 %5
    exit /b %ERRORLEVEL%
)

if /I "%~1"=="check" (
    python "%BASEDIR%scripts\itinfra.py" check-share %2 %3 %4 %5
    exit /b %ERRORLEVEL%
)

if /I "%~1"=="publish" (
    if "%~2"=="" (
        echo [ERRORE] Specificare lo slug del progetto da pubblicare: it publish ^<slug^>
        exit /b 1
    )
    python "%BASEDIR%scripts\itinfra.py" publish %2 %3 %4 %5
    exit /b %ERRORLEVEL%
)

if /I "%~1"=="ui" goto open_ui
if /I "%~1"=="dashboard" goto open_ui

if /I "%~1"=="start" (
    echo [ITINFRA] Verifica rapida aggiornamenti...
    python "%BASEDIR%scripts\itinfra_sync.py"
    echo [ITINFRA] Avvio ambiente di sviluppo...
    where agy >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        start "" agy "%BASEDIR%"
        exit /b 0
    )
    where cursor >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        start "" cursor "%BASEDIR%"
        exit /b 0
    )
    where code >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        start "" code "%BASEDIR%"
        exit /b 0
    )
    echo [INFO] Nessun comando IDE trovato (agy/cursor/code). Workspace pronto in: %BASEDIR%
    exit /b 0
)

:: Tutti gli altri comandi vengono delegati direttamente a scripts/itinfra.py
python "%BASEDIR%scripts\itinfra.py" %*
exit /b %ERRORLEVEL%

:open_ui
python "%BASEDIR%scripts\itinfra.py" ui --open
exit /b %ERRORLEVEL%

:help
echo ===============================================================================
echo   ITINFRA — CLI RAPIDA A ZERO ATTRITO (v0.9.9)
echo ===============================================================================
echo   Uso: it ^<comando^> [opzioni]
echo.
echo   Comandi Rapidi:
echo     it start            Aggiorna il workspace e avvia l'IDE (Antigravity/Cursor)
echo     it update           Sincronizza template, script e guide dalla share centrale
echo     it check            Verifica la connessione e i permessi della share master
echo     it publish ^<slug^>   Esegue il Quality Gate e pubblica il progetto sul server
echo     it ui               Genera e apre l'Enterprise Generative UI Dashboard
echo.
echo   Comandi Documentali (delegati a itinfra.py):
echo     it init ^<slug^>      Inizializza un nuovo progetto IT
echo     it status ^<slug^>    Visualizza lo stato di avanzamento delle 7 fasi
echo     it validate ^<file^>  Valida la conformita formale OKF v0.2 di un documento
echo     it test-suite       Esegue l'Enterprise Test Suite di collaudo
echo ===============================================================================
exit /b 0
