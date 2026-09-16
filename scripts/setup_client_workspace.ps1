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

$RootFiles = @("README.md", "ROADMAP.md", "AGENTS.md", "CLAUDE.md", "INTEGRAZIONE-REPO.md", "00-INDEX.md")
foreach ($f in $RootFiles) {
    $srcFile = Join-Path $CentralShare $f
    $dstFile = Join-Path $TargetLocalDir $f
    if (Test-Path $srcFile) {
        Copy-Item -Path $srcFile -Destination $dstFile -Force
    }
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
Write-Host " SETUP COMPLETATO! WORKSPACE PRONTO ALL'USO                       " -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "Istruzioni rapide per il Tecnico / Agente AI:" -ForegroundColor Yellow
Write-Host "1. Spostarsi nella cartella: cd $TargetLocalDir"
Write-Host "2. Verificare i permessi share: python scripts/itinfra.py check-share"
Write-Host "3. Inizializzare un nuovo cliente: python scripts/itinfra.py init <slug> --client '<Nome>' --name '<Titolo>'"
Write-Host "4. Redigere i documenti OKF v0.2 con Antigravity dentro projects/<slug>/"
Write-Host "5. Pubblicare il progetto con Quality Gate automatico:"
Write-Host "   python scripts/itinfra.py publish <slug>"
Write-Host "6. Aggiornare i template in futuro:"
Write-Host "   python scripts/itinfra.py sync-engine"
Write-Host "=================================================================" -ForegroundColor Cyan

