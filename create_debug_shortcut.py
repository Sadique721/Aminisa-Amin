import os
import win32com.client

desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
shortcut_path = os.path.join(desktop, 'Chrome Developer Debug Mode.lnk')

shell = win32com.client.Dispatch('WScript.Shell')
shortcut = shell.CreateShortCut(shortcut_path)
shortcut.Targetpath = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
debug_dir = os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\DebugProfile')
shortcut.Arguments = f'--remote-debugging-port=9222 --remote-debugging-address=127.0.0.1 --user-data-dir="{debug_dir}"'
shortcut.IconLocation = r'C:\Program Files\Google\Chrome\Application\chrome.exe,0'
shortcut.Description = 'Google Chrome in Developer Debugging Mode (Port 9222)'
shortcut.save()
print(f'[+] SUCCESS: Created Desktop Shortcut: {shortcut_path}')
