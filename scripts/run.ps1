<#
.Synopsis
This PowerShell script is used for build the developing or running environment automatically and run Pap.
.Description
The run.ps1 script is a versatile tool designed to simplify the process of creating and configuring your development or running environment while seamlessly running Pap. It offers the following functionality:

- When executed without any options, it sets up the default environment for running Pap.

- If the `-Dev` option is specified, the script configures and launches a specialized development environment tailored for Pap development. This includes any necessary tools, libraries, and configurations.

- When the `-Build` option is provided (only applicable when `-Dev` is not enabled), the script initiates the frontend build process. This step is crucial for generating the necessary frontend assets for your Pap application.

The script's flexibility allows it to adapt to your specific needs, whether you're focused on development or simply running Pap.
.Parameter Dev 
Whether to run the developing environment.
.Parameter Build
Whether to build the frontend part. Note that this option is only valid if `-Dev` is not enabled.
.Example
To run the script with default settings (no development environment and no frontend build):
PS .\run.ps1

To run the development environment:
PS .\run.ps1 -Dev

To build the frontend part (only valid if -Dev is not enabled):
PS .\run.ps1 -Build
#>

[CmdletBinding()]
param (
    [switch] $Dev,
    [switch] $Build
)

# Function to activate Python virtual environment
function Open-Venv {
    if (Test-Path ".venv") {
        .\.venv\Scripts\Activate
    }
    else {
        python -m venv .venv prompt=pap
        .\.venv\Scripts\Activate
        pip install -r requirements_windows.txt
    }
}

# Function to install node modules
function Open-Node {
    if (-not(Test-Path "node_modules")) {
        npm install
    }
}

# Run the development environment
if ($Dev) {
    Open-Node
    Start-Process npm -ArgumentList "run dev" -NoNewWindow
}

# Build the frontend (only if not in Dev mode)
if ($Build -and !$Dev) {
    Open-Node
    npm run build
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