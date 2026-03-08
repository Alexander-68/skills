# PowerShell hints for multi-platform scripts

Here are the key points and best practices for writing PowerShell scripts that run flawlessly on both Windows and Linux:

## **1\. File Systems and Paths**

This is where cross-platform scripts break most often. Windows is forgiving; Linux is not.

* **Respect Case Sensitivity:** Linux file systems are strictly case-sensitive; Windows is case-insensitive. If your script creates a file named Data.json but later tries to read data.json, it will work on Windows but crash on Linux. Always match cases exactly.  
* **Ditch the Backslash (\\):** Windows uses \\ for file paths, while Linux uses /. Fortunately, PowerShell 7 translates forward slashes (/) seamlessly on Windows. **Always use / in your scripts.**  
* **Use Join-Path:** Better yet, avoid hardcoding separators entirely when building paths programmatically. Use Join-Path \-Path $dir \-ChildPath $file and let PowerShell handle the OS-specific formatting.  
* **Don't Hardcode Root Drives:** Linux doesn't have C:\\. If you need a temporary directory, use \[System.IO.Path\]::GetTempPath() instead of hardcoding C:\\Temp or /tmp.

## **2\. Command and Alias Discipline**

Never use aliases in a cross-platform script. What saves you keystrokes on Windows will trigger native binaries on Linux.

* **Avoid Common Aliases:** Do not use ls, sort, date, curl, or wget. On Windows, ls is an alias for Get-ChildItem. On Linux, ls calls the native GNU ls binary, which returns raw strings instead of the rich PowerShell objects your script is expecting.  
* **Use Full Cmdlet Names:** Always use Get-ChildItem, Sort-Object, Get-Date, and Invoke-WebRequest. (Pro-tip: You can use Shift+Alt+E in VS Code to auto-expand all aliases in your script).

## **3\. Handling OS-Specific Logic**

Sometimes you just can't avoid OS-specific commands (like interacting with system services). PowerShell 7 provides built-in automatic variables to handle this gracefully.

Use if/else blocks with these variables to branch your logic:

* $IsWindows  
* $IsLinux  
* $IsMacOS

PowerShell

```

if ($IsLinux) {
    # Run Linux-specific commands (e.g., systemctl)
} elseif ($IsWindows) {
    # Run Windows-specific commands (e.g., Get-Service)
}

```

## **4\. Leave the "Windows-isms" Behind**

If your script relies on underlying Windows architecture, it will fail on Linux.

* **No WMI or COM:** Get-WmiObject and COM objects (New-Object \-ComObject) do not exist on Linux.  
* **No Registry:** Avoid querying HKLM:\\ or HKCU:\\. Linux uses configuration files (usually in /etc/), not a centralized registry.  
* **Check Cmdlet Availability:** Before running a module-specific command, verify it exists on the host system.

```
if (Get-Command "Get-ActiveDirectoryUser" -ErrorAction SilentlyContinue) { ... }

```

## **5\. Execution and Formatting**

How the script is saved and executed matters just as much as the code inside it.

* **Use the Shebang:** For Linux to know how to execute your .ps1 file natively, put this exact line at the very top of your script: \#\!/usr/bin/env pwsh  
* **Line Endings:** Windows uses CRLF (Carriage Return \+ Line Feed) for line breaks, while Linux uses LF. If you write a script on Windows with CRLF and try to execute it via the shebang on Linux, it will often throw an error. Configure your code editor (like VS Code) or Git repository to save .ps1 files with LF line endings.  
* **Encoding:** PowerShell 7.5 defaults to **UTF-8 without BOM** (Byte Order Mark). Leave it this way; Linux tools despise the Windows BOM.

---

