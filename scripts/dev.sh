#!/bin/bash

npm run dev &

if [ -f "pap-venv/Scripts/activate" ]; then
    source pap-venv/bin/activate

    python ./src-python/app.py

    deactivate
fi
