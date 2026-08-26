[CmdletBinding(SupportsShouldProcess)]
param(
    [string]$TaskName = 'Sajtagent Worktree Maintenance',
    [ValidateRange(1, 3650)]
    [int]$MinimumAgeDays = 14
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$maintenanceScript = Join-Path $PSScriptRoot 'worktree-maintenance.ps1'
if (-not (Test-Path -LiteralPath $maintenanceScript -PathType Leaf)) {
    throw "Maintenance script is missing: $maintenanceScript"
}

$pwsh = (Get-Command pwsh -ErrorAction Stop).Source
$arguments = "-NoProfile -NonInteractive -ExecutionPolicy Bypass -File `"$maintenanceScript`" -Apply -MinimumAgeDays $MinimumAgeDays"
$action = New-ScheduledTaskAction -Execute $pwsh -Argument $arguments -WorkingDirectory (Split-Path -Parent $PSScriptRoot)
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At '03:00'
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew
$userId = [Security.Principal.WindowsIdentity]::GetCurrent().Name
$principal = New-ScheduledTaskPrincipal -UserId $userId -LogonType Interactive -RunLevel Limited
$task = New-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -Principal $principal

if ($PSCmdlet.ShouldProcess($TaskName, 'Register guarded weekly worktree maintenance')) {
    Register-ScheduledTask -TaskName $TaskName -InputObject $task -Force | Out-Null
    Write-Host "Registered '$TaskName' for Sundays at 03:00 as $userId."
}
