# Inizializzazione della Share Master Centrale per ITInfra (Release v0.9)
param(
    [string]$TargetShare = "\\fileserv01\dati01\workaure",
    [switch]$Force
)

$ErrorActionPreference = "Stop"

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host " ITInfra - Inizializzazione Share Master Centrale (v0.9)          " -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "Destinazione share: $TargetShare" -ForegroundColor Yellow

if (-not (Test-Path $TargetShare)) {
    Write-Error "ERRORE: Il percorso di rete $TargetShare non e raggiungibile o non esiste."
    exit 1
}

$RepoRoot = (Resolve-Path "$PSScriptRoot\..").Path

$RequiredDirs = @("scripts", "templates", "docs", "projects")
foreach ($dir in $RequiredDirs) {
    $dirPath = Join-Path $TargetShare $dir
    if (-not (Test-Path $dirPath)) {
        New-Item -ItemType Directory -Path $dirPath -Force | Out-Null
        Write-Host "[CREATA] $dirPath" -ForegroundColor Green
    } else {
        Write-Host "[OK] Cartella presente: $dirPath" -ForegroundColor DarkGray
    }
}

Write-Host "Sincronizzazione motore scripts/ verso la share centrale..." -ForegroundColor Yellow
$ScriptsSrc = Join-Path $RepoRoot "scripts"
$ScriptsDest = Join-Path $TargetShare "scripts"

Get-ChildItem -Path $ScriptsSrc -Filter "*.py" | ForEach-Object {
    $destFile = Join-Path $ScriptsDest $_.Name
    Copy-Item -Path $_.FullName -Destination $destFile -Force
    Write-Host "  -> Sincronizzato script: $($_.Name)" -ForegroundColor Green
}

Write-Host "Sincronizzazione template ufficiali templates/ verso la share centrale..." -ForegroundColor Yellow
$TplSrc = Join-Path $RepoRoot "templates"
$TplDest = Join-Path $TargetShare "templates"
robocopy $TplSrc $TplDest /E /NJH /NJS /NDL /NC /NS | Out-Null
Write-Host "  -> Template allineati." -ForegroundColor Green

Write-Host "Sincronizzazione documentazione docs/ verso la share centrale..." -ForegroundColor Yellow
$DocsSrc = Join-Path $RepoRoot "docs"
$DocsDest = Join-Path $TargetShare "docs"
robocopy $DocsSrc $DocsDest /E /NJH /NJS /NDL /NC /NS | Out-Null
Write-Host "  -> Documentazione allineata." -ForegroundColor Green

$RootFiles = @("README.md", "ROADMAP.md", "AGENTS.md", "CLAUDE.md", "INTEGRAZIONE-REPO.md", "00-INDEX.md")
foreach ($f in $RootFiles) {
    $srcPath = Join-Path $RepoRoot $f
    if (Test-Path $srcPath) {
        $destPath = Join-Path $TargetShare $f
        Copy-Item -Path $srcPath -Destination $destPath -Force
        Write-Host "  -> Sincronizzato file master: $f" -ForegroundColor Green
    }
}

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host " INIZIALIZZAZIONE SHARE MASTER COMPLETATA CON SUCCESSO!           " -ForegroundColor Cyan
Write-Host " Storage pronto: $TargetShare                                    " -ForegroundColor Cyan
Write-Host " I client LAN possono sincronizzarsi tramite setup_client_workspace.ps1" -ForegroundColor Yellow
Write-Host "=================================================================" -ForegroundColor Cyan
