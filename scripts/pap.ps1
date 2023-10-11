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

if ($Update -eq $true) {
    $latestRelease = Invoke-WebRequest -Uri "https://api.github.com/repos/WindLX/Pap/releases/latest" | ConvertFrom-Json
    $downloadUrl = ($latestRelease.assets | Where-Object { $_.name -eq "PapPack.tar.gz" }).browser_download_url

    if (-z $downloadUrl) {
        Write-Error "Error: Unable to find download URL for Pap in the latest release."
        exit 1
    }

    Write-Output "Downloading PapPack.tar.gz..."
    Invoke-WebRequest -Uri $downloadUrl -OutFile "PapPack.tar.gz"

    Write-Output "Extracting PapPack.tar.gz..."
    Expand-Archive -Path "PapPack.tar.gz" -DestinationPath .\

    Remove-Item .\dist -Recurse -Force
    Remove-Item .\src-python -Recurse -Force
    Remove-Item .\README.md -Force
    Remove-Item .\requirements_release.txt -Force

    Move-Item .\PapPack\dist .\dist
    Move-Item .\PapPack\src-python .\src-python
    Move-Item .\PapPack\README.md .\README.md
    Move-Item .\PapPack\requirements_release.txt .\requirements_release.txt

    Remove-Item .\PapPack -Recurse -Force
    Remove-Item .\PapPack.tar.gz -Force

    if (Test-Path -Path ".venv") {
        Remove-Item .\.venv -Recurse -Force
    }
}

Open-Venv
try {
    python src-python/app.py
}
finally {
    deactivate
}