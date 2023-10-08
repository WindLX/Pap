#!/bin/bash

# Function to activate Python virtual environment
activate_venv() {
    if [ -d ".venv" ]; then
        source .venv/bin/activate
    else
        python -m venv .venv --prompt pap
        source .venv/bin/activate
        pip install -r requirements.txt
    fi
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --help)
            less scripts/tool.sh.man
            shift
            ;;
        --test)
            Test=true
            shift
            ;;
        --check)
            Check=true
            shift
            ;;
        *)
            echo "Unknown argument: $1"
            exit 1
            ;;
    esac
done

# pytest
if [ "$Test" = true ]; then
    activate_venv
    pytest -o "python_paths=src-python/"
    deactivate
fi

# static typing check
if [ "$Check" = true ] && [ "$Dev" != true ]; then
    activate_venv
    mypy src-python/
    deactivate
fi

