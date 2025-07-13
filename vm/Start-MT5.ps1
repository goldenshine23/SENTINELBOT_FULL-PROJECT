Write-Output "🚀 Starting MetaTrader 5..."
Start-Process -FilePath "C:\Users\PROF\Desktop\SentinelBot_FullProject\vm\terminal64.exe"
Start-Sleep -Seconds 7

Write-Output "🔐 Logging into MT5 and activating symbols..."
python "C:\Users\PROF\Desktop\SentinelBot_FullProject\vm\MT5Bridge.py"

Write-Output "🤖 Starting SentinelBot strategy..."
Start-Process -WindowStyle Hidden -FilePath "python.exe" -ArgumentList "C:\Users\PROF\Desktop\SentinelBot_FullProject\vm\strategy_runner.py"

Write-Output "✅ Bot is now running in background."
