Get-Process terminal64 | Stop-Process
Write-Output "🛑 Stopping MetaTrader 5..."
Get-Process terminal64 -ErrorAction SilentlyContinue | Stop-Process -Force
Write-Output "✅ MT5 stopped successfully."
