from datetime import datetime
import shutil

def run_all_checks():
    disk = shutil.disk_usage('/')
    disk_percent = (disk.used / disk.total) * 100

    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {
            "disk": round(disk_percent, 2)
        }
    }
