import sqlite3
import shutil
import os
import time
from datetime import datetime

# ✅ Verificar base de datos
def check_database(db_path='database.db'):
    if not os.path.exists(db_path):
        return 'error', 'Base de datos no encontrada'

    try:
        start = time.time()
        conn = sqlite3.connect(db_path, timeout=5)
        conn.execute('SELECT 1')
        conn.close()

        elapsed = (time.time() - start) * 1000
        return 'ok', f'BD responde en {elapsed:.2f}ms'

    except Exception as e:
        return 'error', str(e)


# ✅ Verificar disco
def check_disk():
    disk = shutil.disk_usage('/')
    percent = (disk.used / disk.total) * 100

    if percent > 95:
        return 'error', f'Disco crítico: {percent:.1f}%'
    elif percent > 80:
        return 'warning', f'Disco alto: {percent:.1f}%'
    else:
        return 'ok', f'Disco normal: {percent:.1f}%'


# ✅ Verificar backups
def check_backup():
    backup_dir = "backups"

    if not os.path.exists(backup_dir):
        return 'warning', 'No hay carpeta de backups'

    files = os.listdir(backup_dir)
    if not files:
        return 'error', 'No hay backups'

    latest = max([os.path.join(backup_dir, f) for f in files], key=os.path.getmtime)

    age = (time.time() - os.path.getmtime(latest)) / 3600

    if age > 24:
        return 'warning', f'Backup antiguo: {age:.1f}h'
    
    return 'ok', f'Backup reciente ({age:.1f}h)'


# ✅ Ejecutar todo
def run_all_checks():

    db_status, db_msg = check_database()
    disk_status, disk_msg = check_disk()
    backup_status, backup_msg = check_backup()

    checks = {
        "database": {"status": db_status, "msg": db_msg},
        "disk": {"status": disk_status, "msg": disk_msg},
        "backup": {"status": backup_status, "msg": backup_msg}
    }

    statuses = [db_status, disk_status, backup_status]

    if "error" in statuses:
        overall = "unhealthy"
    elif "warning" in statuses:
        overall = "degraded"
    else:
        overall = "healthy"

    return {
        "status": overall,
        "timestamp": datetime.utcnow().isoformat(),
        "checks": checks
    }
