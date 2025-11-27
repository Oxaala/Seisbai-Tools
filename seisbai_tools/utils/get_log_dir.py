import os
import platform

def get_default_log_dir(app_name: str = "Seisbai") -> str:
    system = platform.system()
    
    if system == "Windows":
        base = os.getenv("LOCALAPPDATA", os.path.expanduser("~\\AppData\\Local"))
        log_dir = os.path.join(base, app_name, "logs")
    elif system == "Darwin":  # macOS
        log_dir = os.path.join(os.path.expanduser(f"~/Library/Logs/{app_name}"))
    else:  # Linux / outros
        if os.geteuid() == 0:
            log_dir = f"/var/log/{app_name}"
        else:
            log_dir = os.path.join(os.path.expanduser(f"~/.local/share/{app_name}/logs"))
    
    os.makedirs(log_dir, exist_ok=True)
    
    return log_dir