import json
import time
import threading
import logging
import os

from process_manager import ProcessManager
from resource_checker import ResourceChecker
from socket_server import SocketServer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

CONFIG_PATH = os.path.join(PROJECT_ROOT, "config", "config.json")
LOG_PATH = os.path.join(PROJECT_ROOT, "logs", "sentinel.log")

os.makedirs("../logs", exist_ok=True)

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

with open(CONFIG_PATH) as f:
    config = json.load(f)

status_data = {
    "running": False,
    "cpu": 0,
    "ram": 0,
    "restarts": 0,
    "last_event": "Iniciado"
}

app_path = os.path.join(PROJECT_ROOT, config["app_path"])

print("Ruta final:", app_path)

process_manager = ProcessManager(
    app_path,
    config["app_name"]
)

resource_checker = ResourceChecker(
    config["max_ram_mb"],
    config["max_cpu_percent"]
)

def restart_app():
    proc = process_manager.get_process()
    if proc:
        process_manager.kill(proc)

    process_manager.start()
    status_data["restarts"] += 1
    status_data["last_event"] = "Reinicio manual"
    logging.info("Reinicio manual ejecutado")

def monitor():
    while True:

        proc = process_manager.get_process()

        if not proc:
            status_data["running"] = False
            status_data["last_event"] = "Aplicación caída - Reiniciando"
            logging.warning("Aplicación caída")

            process_manager.start()
            status_data["restarts"] += 1
            time.sleep(5)
            continue

        status_data["running"] = True

        try:
            check = resource_checker.check(proc)

            status_data["cpu"] = check["cpu"]
            status_data["ram"] = check["ram"]
            status_data["last_event"] = check["reason"]

            if check["overload"]:
                logging.warning(f"Reinicio por {check['reason']}")
                process_manager.kill(proc)
                status_data["restarts"] += 1

        except Exception as e:
            status_data["last_event"] = "Error monitoreo"
            logging.error(str(e))

        time.sleep(config["check_interval"])

if __name__ == "__main__":
    threading.Thread(target=monitor, daemon=True).start()

    socket_server = SocketServer(
        config["port"],
        status_data,
        restart_app
    )

    socket_server.start()