python -m venv .\pap-venv

.\pap-venv\Scripts\Activate.ps1

pip install -r requirements.txt

deactivate

Write-Host "虚拟环境已创建并依赖项已安装。"
