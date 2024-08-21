Set-ExecutionPolicy Unrestricted -Scope CurrentUser -Force

# Define suas credenciais de cliente
$clientId = ""
$clientSecret = ""
$cid = ""

function Get-CrowdstrikeAccessToken {
    param (
        [string]$clientId,
        [string]$clientSecret
    )

    $url = "https://api.us-2.crowdstrike.com/oauth2/token"
    $grantType = "client_credentials"

    $body = @{
        "client_id"     = $clientId
        "client_secret" = $clientSecret
        "grant_type"    = $grantType
    }

    try {
        $response = Invoke-RestMethod -Method Post -Uri $url -Body $body
        return $response.access_token
    }
    catch {
        Write-Host "Error getting access token: $_"
        return $null
    }
}

function ToCheck-CrowdStrike {
    param (
        [string]$accessToken
    )
    $url = "https://api.us-2.crowdstrike.com/policy/combined/sensor-update-builds/v1?platform=windows"

    try {
        $headers = @{
            "Authorization" = "Bearer $accessToken"
            "Accept"        = "application/json"
        }
        
        $response = Invoke-RestMethod -Method Get -Uri $url -Headers $headers

        $resources = $response.resources
        if ($resources -and $resources.Count -gt 1) {
            $versionToCompare = $resources[1].sensor_version
            $crowdStrikeVersion = (Get-WmiObject -Class Win32_Product | Where-Object {$_.Name -eq "CrowdStrike Sensor Platform"}).Version

            $versionToCompareArray = $versionToCompare.Split('.') | ForEach-Object { [int]$_ }
            $crowdStrikeVersionArray = $crowdStrikeVersion.Split('.') | ForEach-Object { [int]$_ }

            $versionsEqual = $true
            for ($i = 0; $i -lt $versionToCompareArray.Count; $i++) {
                if ($crowdStrikeVersionArray[$i] -lt $versionToCompareArray[$i]) {
                    $versionsEqual = $false
                    break
                }
                elseif ($crowdStrikeVersionArray[$i] -gt $versionToCompareArray[$i]) {
                    break
                }
            }

            if ($versionsEqual) {
                Write-Host "Seu sensor está atualizado."
                exit  
            } else {
                Write-Host "Seu sensor está desatualizado."
            }
        } else {
            Write-Host "Não foi possível obter informações suficientes da API."
        }
    } catch {
        Write-Host "Ocorreu um erro ao consultar a API: $_"
    }
}


function Get-CrowdstrikeInstallerSHA256 {
    param (
        [string]$accessToken
    )

    $url = "https://api.us-2.crowdstrike.com/sensors/combined/installers/v1?limit=1&filter=platform%3A%22windows%22"

    try {
        $headers = @{
            "Authorization" = "Bearer $accessToken"
            "Accept"        = "application/json"
        }

        $response = Invoke-RestMethod -Method Get -Uri $url -Headers $headers
        if ($response.resources -and $response.resources.Count -gt 0) {
            return $response.resources[0].sha256
        }
        else {
            Write-Host "No resources found in API response."
            return $null
        }
    }
    catch {
        Write-Host "Error getting installer SHA256: $_"
        return $null
    }
}

function Download-CrowdstrikeInstaller {
    param (
        [string]$installerUrl,
        [string]$accessToken
    )

    try {
        $headers = @{
            "Authorization" = "Bearer $accessToken"
            "Accept"        = "application/octet-stream"
        }

        $filename = "installerSensor.exe"
        Invoke-RestMethod -Method Get -Uri $installerUrl -Headers $headers -OutFile $filename
        return $filename
    }
    catch {
        Write-Host "Error downloading installer: $_"
        return $null
    }
}

# Obter o token de acesso da API do Crowdstrike
$accessToken = Get-CrowdstrikeAccessToken -clientId $clientId -clientSecret $clientSecret

ToCheck-CrowdStrike -accessToken $accessToken


if ($accessToken) {
    # Obter o valor do "sha256" do instalador
    $sha256Value = Get-CrowdstrikeInstallerSHA256 -accessToken $accessToken

    if ($sha256Value) {
        # Formatar a URL do endpoint de download do instalador
        $installerUrl = "https://api.us-2.crowdstrike.com/sensors/entities/download-installer/v1?id=$sha256Value"

        # Baixar o instalador
        $installerFilename = Download-CrowdstrikeInstaller -installerUrl $installerUrl -accessToken $accessToken

        if ($installerFilename) {
            # Iniciar o processo do instalador
            New-Item -Path "C:\Temp\Crowdstrike" -ItemType Directory -Force -ErrorAction SilentlyContinue
            Move-Item -Path "C:\Windows\System32\installerSensor.exe" -Destination "C:\Temp\Crowdstrike\"
            Start-Process -FilePath "C:\Temp\Crowdstrike\installerSensor.exe" -ArgumentList "-s", "/install", "/quiet", "/norestart", "CID=$cid", "/forcedowngrade"                
        }
        else {
            Write-Host "Failed to download installer."
        }
    }
    else {
        Write-Host "Failed to get installer SHA256."
    }
    Out-File -Append -FilePath 'C:\Temp\CrowdStrike\script.log' -Force
}
else {
    Write-Host "Failed to get access token."
}

Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force