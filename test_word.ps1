$word = New-Object -ComObject Word.Application
Write-Host "Word application successfully created! Version: $($word.Version)"
$word.Quit()
