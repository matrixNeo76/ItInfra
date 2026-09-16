# Setup Workspace Locale Tecnico Windows 11 (Release v0.9)
param(
    [string]$TargetLocalDir = "C:\itinfra",
    [string]$CentralShare = "\\fileserv01\dati01\workaure"
)

$ErrorActionPreference = "Stop"

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host " ITInfra - Setup Workspace Locale Tecnico Windows 11 (v0.9)      " -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "Cartella locale (SSD): $TargetLocalDir" -ForegroundColor Yellow
Write-Host "Share master centrale: $CentralShare" -ForegroundColor Yellow

if (-not (Test-Path $CentralShare)) {
    Write-Error "ERRORE: La share centrale $CentralShare non e raggiungibile. Verificare la connessione di rete LAN / VPN aziendale."
    exit 1
}

if (-not (Test-Path $TargetLocalDir)) {
    New-Item -ItemType Directory -Path $TargetLocalDir -Force | Out-Null
    Write-Host "[CREATA] Cartella di lavoro locale: $TargetLocalDir" -ForegroundColor Green
} else {
    Write-Host "[OK] Cartella locale esistente: $TargetLocalDir" -ForegroundColor DarkGray
}

$LocalProjects = Join-Path $TargetLocalDir "projects"
if (-not (Test-Path $LocalProjects)) {
    New-Item -ItemType Directory -Path $LocalProjects -Force | Out-Null
}

$FoldersToSync = @("scripts", "templates", "docs", "skills", ".agents", ".vscode")
foreach ($folder in $FoldersToSync) {
    $src = Join-Path $CentralShare $folder
    $dst = Join-Path $TargetLocalDir $folder
    if (Test-Path $src) {
        Write-Host "Sincronizzazione $folder..." -ForegroundColor Yellow
        robocopy $src $dst /E /NJH /NJS /NDL /NC /NS | Out-Null
        Write-Host "  -> [OK] $folder allineata." -ForegroundColor Green
    }
}

$RootFiles = @("README.md", "ROADMAP.md", "AGENTS.md", "CLAUDE.md", "INTEGRAZIONE-REPO.md", "00-INDEX.md", "update.cmd", "it.cmd")
foreach ($f in $RootFiles) {
    $srcFile = Join-Path $CentralShare $f
    $dstFile = Join-Path $TargetLocalDir $f
    if (Test-Path $srcFile) {
        Copy-Item -Path $srcFile -Destination $dstFile -Force
    }
}

# Registrazione di TargetLocalDir nel PATH utente (comando 'it' ovunque)
try {
    $UserPath = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::User)
    if ($UserPath -notlike "*$TargetLocalDir*") {
        $NewUserPath = "$UserPath;$TargetLocalDir"
        [System.Environment]::SetEnvironmentVariable("Path", $NewUserPath, [System.EnvironmentVariableTarget]::User)
        $env:Path = "$env:Path;$TargetLocalDir"
        Write-Host "[OK] Cartella '$TargetLocalDir' registrata nel PATH utente (comando 'it' disponibile ovunque)." -ForegroundColor Green
    }
} catch {
    Write-Warning "  ! Impossibile aggiornare automaticamente il PATH utente. Aggiungere manualmente $TargetLocalDir."
}

# Creazione del Launcher 1-Clic sul Desktop Utente
$ServerHost = "fileserv01"
if ($CentralShare -match '^\\\\([^\\]+)\\') {
    $ServerHost = $matches[1]
}

$DesktopPath = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::Desktop)
if (Test-Path $DesktopPath) {
    $LauncherPath = Join-Path $DesktopPath "ITInfra - Aggiorna e Avvia.cmd"
    $LauncherContent = @"
@echo off
setlocal
title ITInfra - Avvio Workspace
echo ===============================================================================
echo   ITINFRA -- VERIFICA AGGIORNAMENTI E AVVIO WORKSPACE
echo ===============================================================================
cd /d "$TargetLocalDir"

:: Test rapido connettivita porta 445 (SMB) con timeout 1.5s
powershell -NoProfile -ExecutionPolicy Bypass -Command "`$tcp = New-Object System.Net.Sockets.TcpClient; `$ar = `$tcp.BeginConnect('$ServerHost', 445, `$null, `$null); `$wh = `$ar.AsyncWaitHandle; if (`$wh.WaitOne(1500, `$false)) { `$tcp.EndConnect(`$ar); `$tcp.Close(); exit 0 } else { `$tcp.Close(); exit 1 }" >nul 2>nul

if %ERRORLEVEL% EQU 0 (
    echo [RETE] Server master raggiungibile. Sincronizzazione in corso...
    if exist "scripts\itinfra_sync.py" (
        python scripts\itinfra_sync.py
    )
) else (
    echo [RETE] Server centrale non raggiungibile (Modalita Offline).
    echo        I progetti locali rimangono completamente operativi.
)

echo.
echo [AVVIO] Apertura ambiente di sviluppo...
where agy >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    start "" agy "$TargetLocalDir"
    exit /b 0
)
where cursor >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    start "" cursor "$TargetLocalDir"
    exit /b 0
)
where code >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    start "" code "$TargetLocalDir"
    exit /b 0
)
echo [OK] Workspace pronto in: $TargetLocalDir
pause
"@
    [System.IO.File]::WriteAllText($LauncherPath, $LauncherContent, [System.Text.Encoding]::ASCII)
    Write-Host "[OK] Collegamento Desktop generato: $LauncherPath" -ForegroundColor Green
}

$ConfigFile = Join-Path $TargetLocalDir ".itinfra_config.json"
$ConfigData = @"
{
  "central_share": "$($CentralShare -replace '\\', '\\\\')",
  "workspace_mode": "local_technician"
}
"@

[System.IO.File]::WriteAllText($ConfigFile, $ConfigData, [System.Text.Encoding]::UTF8)
Write-Host "[OK] File di configurazione generato: $ConfigFile" -ForegroundColor Green

Write-Host "Verifica ambiente Python locale..." -ForegroundColor Yellow
$pyInstalled = $false
try {
    $pyVer = & python --version 2>&1
    if ($pyVer -match "Python 3") {
        Write-Host "  -> Python rilevato: $pyVer" -ForegroundColor Green
        $pyInstalled = $true
    }
} catch {
    $pyInstalled = $false
}

if (-not $pyInstalled) {
    Write-Host "  ! Python non rilevato nel PATH. Tentativo installazione automatica tramite Windows Package Manager (winget)..." -ForegroundColor Yellow
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        Write-Host "  -> Installazione silenziosa di Python 3.12 in corso..." -ForegroundColor Cyan
        & winget install --id Python.Python.3.12 -e --silent --accept-source-agreements --accept-package-agreements
        # Aggiornamento variabile PATH della sessione corrente
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        try {
            $pyVer = & python --version 2>&1
            Write-Host "  -> [SUCCESSO] Python installato e pronto: $pyVer" -ForegroundColor Green
            $pyInstalled = $true
        } catch {
            Write-Host "  -> [INFO] Installazione completata. Riavviare il terminale per ricaricare il PATH di sistema." -ForegroundColor Cyan
        }
    } else {
        Write-Warning "  ! winget non disponibile. Scaricare e installare Python 3.12 dal Microsoft Store o da https://www.python.org/downloads/ (spuntando 'Add python.exe to PATH')."
    }
}

if ($pyInstalled) {
    Write-Host "Installazione dipendenze minime (pyyaml, cryptography, smbprotocol)..." -ForegroundColor Yellow
    try {
        & python -m pip install --quiet --upgrade pyyaml cryptography smbprotocol
        Write-Host "  -> [OK] Librerie Python installate con successo." -ForegroundColor Green
    } catch {
        Write-Warning "  ! Impossibile installare automaticamente le librerie. Eseguire manualmente: pip install pyyaml cryptography smbprotocol"
    }
}

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host " SETUP COMPLETATO! WORKSPACE PRONTO ALL'USO (ZERO ATTRITO)        " -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "Modalita di avvio e comandi per il Tecnico:" -ForegroundColor Yellow
Write-Host "1. MODALITA DESKTOP (1-Clic):"
Write-Host "   Fai doppio clic sull'icona 'ITInfra - Aggiorna e Avvia' sul tuo Desktop."
Write-Host "2. MODALITA TERMINALE (Comandi Brevi a 1 parola):"
Write-Host "   it start           -> Aggiorna e apre l'editor"
Write-Host "   it update          -> Sincronizza template e script"
Write-Host "   it check           -> Verifica connessione e permessi share"
Write-Host "   it publish <slug>  -> Esegue Quality Gate e pubblica su server"
Write-Host "3. MODALITA CHAT (In Antigravity):"
Write-Host "   Digita semplicemente 'aggiorna', 'controlla' o 'pubblica <slug>'."
Write-Host "=================================================================" -ForegroundColor Cyan

