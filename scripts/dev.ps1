Start-Process -NoNewWindow -FilePath "npm" -ArgumentList "run dev"

if (Test-Path "pap-venv\Scripts\Activate.ps1") {
  .\pap-venv\Scripts\Activate.ps1
}

python .\src-python\app.py

deactivate
