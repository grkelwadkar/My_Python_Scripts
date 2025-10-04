import os
import win32api
import win32con

def get_file_version_safe(file_path):
    try:
        info = win32api.GetFileVersionInfo(file_path, '\\')
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        version = f"{ms >> 16}.{ms & 0xFFFF}.{ls >> 16}.{ls & 0xFFFF}"
        return version
    except Exception as e:
        return f"No version info ({str(e)})"

# Example usage
folder = r"C:\Users\grkel\Downloads\Executables"
for file_name in os.listdir(folder):
    full_path = os.path.join(folder, file_name)
    if os.path.isfile(full_path):
        version = get_file_version_safe(full_path)
        print(f"{file_name}: {version}")