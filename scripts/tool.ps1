<#
.Synopsis
This PowerShell script is used for check and test the Pap backend.
.Description
The tool.ps1 script is a versatile tool designed to simplify the process of Pap backend test and type check. It offers the following functionality:

- When executed without any options, it sets up the default environment for running Pap.

- If the `-Test` option is specified, the script will launch the pytest automatically.

- When the `-Check` option is provided, This script automatically performs Python static type checking。

The script's flexibility allows it to adapt to your specific needs, whether you're focused on development or simply coding.
.Parameter Check 
Whether to run the test.
.Parameter Test
Whether to run the static type check.
.Example
To run the test:
PS .\run.ps1 -Test

To run the static type check:
PS .\run.ps1 -Check
#>

[CmdletBinding()]
param (
    [switch] $Check,
    [switch] $Test
)

# Function to activate Python virtual environment
function Open-Venv {
    if (Test-Path "pap-venv") {
        .\pap-venv\Scripts\Activate
    }
    else {
        python -m venv pap-venv
        .\pap-venv\Scripts\Activate
        pip install -r requirements_windows.txt
    }
}

if ($Test) {
    Open-Venv
    pytest -o "python_paths=src-python/"
}

if ($Check) {
    Open-Venv
    mypy src-python/
}

deactivate