[CmdletBinding()]
param(
    [string]$OutputDirectory = "$HOME\Videos\Jadel-Pages-Meta-App-Review"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Urls = [ordered]@{
    Home         = "https://jadelapp-meta.streamlit.app/"
    Privacy      = "https://jadelapp-meta.streamlit.app/?view=privacy"
    Terms        = "https://jadelapp-meta.streamlit.app/?view=terms"
    DataDeletion = "https://jadelapp-meta.streamlit.app/?view=data-deletion"
    ReviewDemo   = "https://jadelapp-meta.streamlit.app/?view=review-demo"
}

[System.IO.Directory]::CreateDirectory($OutputDirectory) | Out-Null

Write-Host "META_APP_REVIEW_PREFLIGHT=START"

foreach ($Name in $Urls.Keys) {
    try {
        $Response = Invoke-WebRequest -Uri $Urls[$Name] -Method Head -MaximumRedirection 5 -TimeoutSec 30
        if ($Response.StatusCode -lt 200 -or $Response.StatusCode -ge 400) {
            throw "HTTP_$($Response.StatusCode)"
        }
        Write-Host "URL_CHECK=PASS name=$Name status=$($Response.StatusCode)"
    }
    catch {
        Write-Host "URL_CHECK=FAIL name=$Name detail=$($_.Exception.Message)"
        throw "META_APP_REVIEW_URL_PREFLIGHT=FAIL"
    }
}

$Browser = $null
$Candidates = @(
    "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
    "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe",
    "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe"
)

foreach ($Candidate in $Candidates) {
    if (Test-Path -LiteralPath $Candidate -PathType Leaf) {
        $Browser = $Candidate
        break
    }
}

if ($null -eq $Browser) {
    throw "SUPPORTED_BROWSER_NOT_FOUND"
}

$Checklist = @"
Jadel Pages API — Meta App Review recording checklist

[ ] Streamlit app is deployed from jadeldiaz01-png/jadelapp-meta main
[ ] META_APP_ID, META_APP_SECRET, META_REDIRECT_URI and META_GRAPH_VERSION are configured in Streamlit Secrets
[ ] Facebook Login redirect URI is exactly https://jadelapp-meta.streamlit.app/
[ ] Account used for recording has an app role while the app is in development mode
[ ] Account administers the Facebook test Page
[ ] Notifications, email, chat, password managers and terminals are closed
[ ] Browser zoom is 100% or 110%
[ ] Recording resolution is 1920x1080
[ ] Microphone level was tested
[ ] No tokens, secrets, passwords or personal messages are visible
[ ] The test post is deleted before ending the recording

Output directory:
$OutputDirectory
"@

$ChecklistPath = Join-Path $OutputDirectory "RECORDING_CHECKLIST.txt"
[System.IO.File]::WriteAllText($ChecklistPath, $Checklist, [System.Text.UTF8Encoding]::new($false))

$BrowserArguments = @(
    "--new-window",
    $Urls.Home,
    $Urls.Privacy,
    $Urls.Terms,
    $Urls.DataDeletion,
    $Urls.ReviewDemo
)

Start-Process -FilePath $Browser -ArgumentList $BrowserArguments

$ObsCandidates = @(
    "$env:ProgramFiles\obs-studio\bin\64bit\obs64.exe",
    "${env:ProgramFiles(x86)}\obs-studio\bin\64bit\obs64.exe"
)

$Obs = $ObsCandidates | Where-Object { Test-Path -LiteralPath $_ -PathType Leaf } | Select-Object -First 1

if ($Obs) {
    Start-Process -FilePath $Obs
    Write-Host "OBS_START=PASS"
}
else {
    Write-Host "OBS_NOT_FOUND=INFO"
    Write-Host "Use Windows Snipping Tool screen recording or install OBS Studio."
}

Write-Host "CHECKLIST_PATH=$ChecklistPath"
Write-Host "OUTPUT_DIRECTORY=$OutputDirectory"
Write-Host "META_APP_REVIEW_PREFLIGHT=PASS"
Write-Host "NEXT=Start recording manually and follow docs/META_APP_REVIEW_SCREENCAST.md"
