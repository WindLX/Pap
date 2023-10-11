#!/bin/bash

# Function to activate Python virtual environment
activate_venv() {
    if [ -d ".venv" ]; then
        source .venv/bin/activate
    else
        python -m venv .venv --prompt pap
        source .venv/bin/activate
        pip install -r scripts/requirements.txt
    fi
}

# Function to install node modules
install_modules() {
    if [ ! -d "node_modules" ]; then
        npm install
    fi
}

pack() {
    if [ -d "PapPack" ]; then
        rm PapPack -r
    fi
    mkdir PapPack
    mkdir PapPack/data
    cp data/config.toml PapPack/data/ -r
    cp dist PapPack/dist -r
    cp src-python PapPack/src-python -r
    cp README.md PapPack/
    cp scripts/requirements_release.txt PapPack/
    cp scripts/pap.sh PapPack/
    cp scripts/pap.sh.man PapPack/
    rm PapPack/src-python/test -r
    chmod 774 scripts/pap.sh
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --help)
            less scripts/tool.sh.man
            exit 1
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
        --build)
            Build=true
            shift
            ;;
        --pack)
            Pack=true
            shift
            ;;
        --docker-build)
            DockerBuild=true
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
    exit 0
fi

# static typing check
if [ "$Check" = true ]; then
    activate_venv
    mypy src-python/
    deactivate
    exit 0
fi

# build frontend
if [ "$Build" = true ]; then
    install_modules
    npm run build
    exit 0
fi

if [ "$DockerBuild" = true ]; then
    install_modules
    npm run build
    pack
    docker build -t pap .
    rm PapPack -r
    exit 0
fi

# pack the whole project
if [ "$Pack" = true ]; then
    install_modules
    npm run build
    pack
    cp Dockerfile PapPack/
    tar -czf PapPack.tar.gz ./PapPack
    rm PapPack -r
    echo "Pack Fin"
    exit 0
fi
