<#
.Synopsis
This PowerShell script is used for python type check, test the Pap backend, build the Pap frontend, pack the whole project.
.Description
The tool.ps1 script is a versatile tool designed to simplify the process of Pap backend test, type check, build and pack. It offers the following functionality:

- When executed without any options, it will DO NOTHING.

- If the `-Test` option is specified, the script will launch the pytest automatically.

- When the `-Check` option is provided, This script will automatically perform Python static type checking。

- When the `-Build` option is provided, This script will build the frontend part

- When the `-Pack` option is provided, This script will pack the whole project

The script's flexibility allows it to adapt to your specific needs, whether you're focused on development or simply coding.
.Parameter Check 
Whether to run the test.
.Parameter Test
Whether to run the static type check.
.Parameter Build
Whether to build the frontend.
.Parameter Pack
Whether to pack the whole project.
.Example
To run the test:
PS .\tool.ps1 -Test

To run the static type check:
PS .\tool.ps1 -Check

To run the build:
PS .\tool.ps1 -Build

To run the pack:
PS .\tool.ps1 -Pack
#>

[CmdletBinding()]
param (
    [switch] $Check,
    [switch] $Test,
    [switch] $Build,
    [switch] $Pack,
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

if ($Test) {
    Open-Venv
    pytest -o "python_paths=src-python/"
    deactivate
} elseif ($Check) {
    Open-Venv
    mypy src-python/
    deactivate
} elseif ($Build) {
    Open-Node
    npm run build
} elseif ($Pack) {
    Open-Node
    npm run build
    if (Test-Path "PapPack") {
        Remove-Item -Path .\PapPack -Recurse -Force
    }
    New-Item -Path .\PapPack -ItemType Directory
    New-Item -Path .\PapPack\data -ItemType Directory
    Copy-Item -Path .\data\config.toml -Destination .\PapPack\data\ -Recurse
    Copy-Item -Path .\dist -Destination .\PapPack\dist -Recurse
    Copy-Item -Path .\src-python -Destination .\PapPack\src-python -Recurse
    Copy-Item -Path .\README.md -Destination .\PapPack\
    Copy-Item -Path .\scripts\requirements_release.txt -Destination .\PapPack\
    Copy-Item -Path .\scripts\pap.sh -Destination .\PapPack\
    Copy-Item -Path .\scripts\pap.sh.man -Destination .\PapPack\
    Remove-Item -Path .\PapPack\src-python\test -Recurse -Force
    Set-ItemProperty -Path .\scripts\pap.sh -Name IsReadOnly -Value $false
    Set-ItemProperty -Path .\scripts\pap.sh -Name Attributes -Value 'Normal'
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    [System.IO.Compression.ZipFile]::CreateFromDirectory(".\PapPack", "PapPack.zip")
    Remove-Item -Path .\PapPack -Recurse -Force
    Write-Output "Pack Fin"
} else {
    Write-Output "please choose a switch below neither this script will do nothing."
    Write-Output "1. -Check"
    Write-Output "2. -Test"
    Write-Output "3. -Build"
    Write-Output "4. -Pack"
}
