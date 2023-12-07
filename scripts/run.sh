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

# Function to install node modules
install_modules() {
    if [ ! -d "node_modules" ]; then
        npm install
    fi
}

build_rust() {
    cd md/md_wasm
    cargo build --release
    wasm-pack build
    cd ../..

    cd sim
    cargo build --release
    wasm-pack build
    cd ..
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --help)
            less scripts/run.sh.man
            exit 0
            shift
            ;;
        --dev)
            Dev=true
            shift
            ;;
        *)
            echo "Unknown argument: $1"
            exit 1
            ;;
    esac
done

# Run the development environment
if [ "$Dev" = true ]; then
    build_rust
    install_modules
    npm run dev & 
fi

activate_venv
python src-python/app.py --dev=$Dev
deactivate
