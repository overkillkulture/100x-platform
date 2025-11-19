Add-Type -AssemblyName System.Windows.Forms,System.Drawing
$screens = [Windows.Forms.Screen]::AllScreens
$bounds = $screens[0].Bounds
$bmp = New-Object Drawing.Bitmap $bounds.Width, $bounds.Height
$graphics = [Drawing.Graphics]::FromImage($bmp)
$graphics.CopyFromScreen($bounds.Location, [Drawing.Point]::Empty, $bounds.Size)
$bmp.Save("C:\Users\joshb\100X Workspace\screenshot_workspace.png")
$bmp.Dispose()
$graphics.Dispose()
Write-Host "Screenshot saved to: C:\Users\joshb\100X Workspace\screenshot_workspace.png"
