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

$FoldersToSync = @("scripts", "templates", "docs")
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
try {
    $pyVer = & python --version 2>&1
    Write-Host "  -> Python rilevato: $pyVer" -ForegroundColor Green
} catch {
    Write-Warning "  ! ATTENZIONE: Python non e presente nel PATH. Installare Python 3.10+ da python.org o Microsoft Store."
}

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host " SETUP COMPLETATO! WORKSPACE PRONTO ALL'USO                       " -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "Istruzioni rapide per il Tecnico / Agente AI:" -ForegroundColor Yellow
Write-Host "1. Spostarsi nella cartella: cd $TargetLocalDir"
Write-Host "2. Inizializzare un nuovo cliente: python scripts/itinfra.py init <slug> --client '<Nome>' --name '<Titolo>'"
Write-Host "3. Redigere i documenti OKF v0.2 con Antigravity dentro projects/<slug>/"
Write-Host "4. Pubblicare il progetto con Quality Gate automatico:"
Write-Host "   python scripts/itinfra.py publish <slug>"
Write-Host "5. Aggiornare i template in futuro:"
Write-Host "   python scripts/itinfra.py sync-engine"
Write-Host "=================================================================" -ForegroundColor Cyan
