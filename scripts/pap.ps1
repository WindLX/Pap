<#
.Synopsis
This PowerShell script is used for automating the setup of a running environment and execute Pap and update.
.Description
The pap.ps1 script is a versatile tool designed to simplify the process of creating and updating your running environment while seamlessly running Pap. It offers the following functionality:

- When executed without any options, it sets up the default environment for running Pap.

- If the `-Update` option is specified, the script update the version of Pap from remote repository

The script's flexibility allows it to adapt to your specific needs, whether you're focused on development or simply running Pap.
.Parameter Update
Whether to update.
.Example
To run the script with default settings:
PS .\pap.ps1

To update the version of Pap before running:
PS .\pap.ps1 -Dev
#>

[CmdletBinding()]
param (
    [switch] $Update,
)

# Function to activate Python virtual environment
function Open-Venv {
    if (Test-Path ".venv") {
        .\.venv\Scripts\Activate
    }
    else {
        python -m venv .venv --prompt pap
        .\.venv\Scripts\Activate
        pip install -r requirements_release.txt
    }
}

if ($Update) {
    if (Test-Path ".venv") {
        Remove-Item -Path .\.venv -Recurse -Force
    }
}

Open-Venv
try {
    python src-python/app.py
}
finally {
    deactivate
}