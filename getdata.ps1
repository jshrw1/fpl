# Define variables for URLs and output paths
$BaseUrl = "https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data"
$OutputDir = "C:\Users\Joshua\Documents\python\jshrw1\fpl\data\raw"

# List of years
$Years = @("2020-21", "2021-22", "2022-23", "2023-24", "2024-25")

# List of files to download
$Files = @("players_raw.csv", "teams.csv")

# Function to create directories
function Create-Directories {
    param (
        [string]$Path
    )
    
    if (-not (Test-Path -Path $Path)) {
        Write-Output "Creating directory: $Path"
        New-Item -Path $Path -ItemType Directory | Out-Null
    }
}

# Function to download files
function Download-Files {
    param (
        [string]$Year,
        [string]$File
    )
    
    $DirectoryPath = Join-Path -Path $OutputDir -ChildPath $Year
    $FilePath = Join-Path -Path $DirectoryPath -ChildPath $File
    $Url = "$BaseUrl/$Year/$File"

    # Ensure directory exists
    Create-Directories -Path $DirectoryPath

    Write-Output "Downloading $File to $FilePath"
    Invoke-WebRequest -Uri $Url -OutFile $FilePath
}

# Main script execution
foreach ($Year in $Years) {
    foreach ($File in $Files) {
        Download-Files -Year $Year -File $File
    }
}
