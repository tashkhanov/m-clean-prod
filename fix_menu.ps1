
$path = "d:\Freelance\mclean_project\static\css\style.css"
$content = Get-Content $path
$newContent = New-Object System.Collections.Generic.List[string]

$added = $false
foreach ($line in $content) {
    if ($line -match "^\.mega-menu\s*{" -and -not $added) {
        $newContent.Add(".mega-menu-wrapper {")
        $newContent.Add("    position: relative;")
        $newContent.Add("}")
        $newContent.Add("")
        $newContent.Add("/* Hide the default underline animation for mega trigger links */")
        $newContent.Add(".mega-menu-wrapper > .header__nav-link::after {")
        $newContent.Add("    display: none !important;")
        $newContent.Add("}")
        $newContent.Add("")
        $newContent.Add("/* The mega menu panel — full width under header */")
        $added = $true
    }
    $newContent.Add($line)
}

$newContent | Set-Content $path -Encoding UTF8
