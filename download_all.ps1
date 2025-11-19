# PowerShell script to download all pages from sitemap
$pages = Get-Content "pages_to_download.txt"
$baseUrl = "https://conciousnessrevolution.io/"
$downloaded = 0
$failed = 0

Write-Host "Starting download of $($pages.Count) pages..." -ForegroundColor Green

foreach ($page in $pages) {
    if ($page -eq "" -or $page -eq "/") { continue }

    $url = $baseUrl + $page
    $outputFile = $page

    # Skip if already exists
    if (Test-Path $outputFile) {
        Write-Host "✓ Already exists: $page" -ForegroundColor Yellow
        continue
    }

    Write-Host "Downloading: $page" -ForegroundColor Cyan
    curl.exe -s -o $outputFile $url

    if ($LASTEXITCODE -eq 0) {
        $downloaded++
        Write-Host "✓ Downloaded: $page" -ForegroundColor Green
    } else {
        $failed++
        Write-Host "✗ Failed: $page" -ForegroundColor Red
    }

    # Small delay to be nice to the server
    Start-Sleep -Milliseconds 200
}

Write-Host "`n=== Download Complete ===" -ForegroundColor Green
Write-Host "Downloaded: $downloaded" -ForegroundColor Green
Write-Host "Failed: $failed" -ForegroundColor Red
Write-Host "Total: $($pages.Count)" -ForegroundColor White
