$ErrorActionPreference = "Stop"
$PSScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ScriptPath = Join-Path $PSScriptRoot "search_go_refs.py"

if (Get-Command python -ErrorAction SilentlyContinue) {
  & python $ScriptPath @args
  exit $LASTEXITCODE
}

if (Get-Command py -ErrorAction SilentlyContinue) {
  & py -3 $ScriptPath @args
  exit $LASTEXITCODE
}

Write-Error "python or py not found in PATH"
