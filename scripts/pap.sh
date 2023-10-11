#!/bin/bash

# Function to activate Python virtual environment
activate_venv() {
    if [ -d ".venv" ]; then
        source .venv/bin/activate
    else
        python -m venv .venv --prompt pap
        source .venv/bin/activate
        pip install -r requirements_release.txt
    fi
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --help)
            less pap.sh.man
            exit 0
            shift
            ;;
        --update)
            Update=true
            shift
            ;;
        *)
            echo "Unknown argument: $1"
            exit 1
            ;;
    esac
done

if [ "$Update" = true ]; then
    latest_release=$(curl -s "https://api.github.com/repos/WindLX/Pap/releases/latest")
    download_url=$(echo "$latest_release" | grep "browser_download_url" | grep "PapPack.tar.gz" | cut -d '"' -f 4)
    if [ -z "$download_url" ]; then
        echo "Error: Unable to find download URL for Pap in the latest release."
        exit 1
    fi

    echo "Downloading PapPack.tar.gz..."
    curl -L -o PapPack.tar.gz "$download_url"

    echo "Extracting PapPack.tar.gz..."
    tar -xzf PapPack.tar.gz

    rm ./dist -r
    rm ./src-python -r
    rm ./README.md
    rm ./requirements_release.txt

    mv ./PapPack/dist ./dist
    mv ./PapPack/src-python ./src-python
    mv ./PapPack/README.md ./README.md
    mv ./PapPack/requirements_release.txt ./requirements_release.txt

    rm PapPack -r
    rm PapPack.tar.gz
    
    if [ -d ".venv" ]; then
        rm .venv -r
    fi
fi

activate_venv
python src-python/app.py
deactivate
