<#
.Synopsis
This PowerShell script is used for python type check, test the Pap backend, build the Pap frontend.
.Description
The tool.ps1 script is a versatile tool designed to simplify the process of Pap backend test, type check and build. It offers the following functionality:

- When executed without any options, it will DO NOTHING.

- If the `-Test` option is specified, the script will launch the pytest automatically.

- When the `-Check` option is provided, this script will automatically perform Python static type checking.

- When the `-Build` option is provided, this script will build the frontend part.

The script's flexibility allows it to adapt to your specific needs, whether you're focused on development or simply coding.
.Parameter Check 
Whether to run the test.
.Parameter Test
Whether to run the static type check.
.Parameter Build
Whether to build the frontend.
.Example
To run the test:
PS .\tool.ps1 -Test

To run the static type check:
PS .\tool.ps1 -Check

To run the build:
PS .\tool.ps1 -Build
#>

[CmdletBinding()]
param (
    [switch] $Check,
    [switch] $Test,
    [switch] $Build
)

# Function to install node modules
function Open-Node {
    if (-not(Test-Path "node_modules")) {
        npm install
    }
}

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

function Build-Rust {
    cargo install wasm-pack
    Set-Location .\md\md_wasm
    cargo build --release
    wasm-pack build
    Set-Location ..\..
}

if ($Test) {
    Open-Venv
    pytest -o "python_paths=src-python/"
    deactivate
}
elseif ($Check) {
    Open-Venv
    mypy src-python/
    deactivate
}
elseif ($Build) {
    Build-Rust
    Open-Node
    npm run build
}
else {
    Write-Output "please choose a switch below neither this script will do nothing."
    Write-Output "1. -Check"
    Write-Output "2. -Test"
    Write-Output "3. -Build"
}
