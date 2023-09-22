#!/bin/bash

python -m venv ./pap-venv

source ./pap-venv/bin/activate

pip install -r requirements.txt

deactivate

echo "虚拟环境已创建并依赖项已安装。"
