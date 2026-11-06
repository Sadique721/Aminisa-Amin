Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "D:\current using file\Mine\1 social media automation handler file"
WshShell.Run """C:\Python314\pythonw.exe"" ""D:\current using file\Mine\1 social media automation handler file\engines\daily_5_images_scheduler.py"" --run-now", 0, False
