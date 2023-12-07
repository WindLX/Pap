<#
.Synopsis
This PowerShell script is used for build the developing or running environment automatically and run Pap.
.Description
The run.ps1 script is a versatile tool designed to simplify the process of creating and configuring your development or running environment while seamlessly running Pap. It offers the following functionality:

- When executed without any options, it sets up the default environment for running Pap.

- If the `-Dev` option is specified, the script configures and launches a specialized development environment tailored for Pap development. This includes any necessary tools, libraries, and configurations.

The script's flexibility allows it to adapt to your specific needs, whether you're focused on development or simply running Pap.
.Parameter Dev 
Whether to run the developing environment.
.Example
To run the script with default settings (no development environment and no frontend build):
PS .\run.ps1

To run the development environment:
PS .\run.ps1 -Dev
#>

[CmdletBinding()]
param (
    [switch] $Dev
)

# Function to activate Python virtual environment
function Open-Venv {
    if (Test-Path ".venv") {
        .\.venv\Scripts\Activate
    }
    else {
        python -m venv .venv --prompt pap
        .\.venv\Scripts\Activate
        pip install -r scripts/requirements.txt
    }
}

# Function to install node modules
function Open-Node {
    if (-not(Test-Path "node_modules")) {
        npm install
    }
}

function Build-Rust {
    Set-Location .\md\md_wasm
    cargo build --release
    wasm-pack build
    Set-Location ..\..

    Set-Location .\sim
    cargo build --release
    wasm-pack build
    Set-Location ..
}

# Run the development environment
if ($Dev) {
    Build-Rust
    Open-Node
    Start-Process npm -ArgumentList "run dev" -NoNewWindow
}

Open-Venv
try {
    if ($Dev) {
        python src-python/app.py --dev=$Dev
    }
    else {
        python src-python/app.py
    }
}
finally {
    deactivate
}