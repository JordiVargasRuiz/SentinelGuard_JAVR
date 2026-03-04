import psutil
import subprocess
import os

class ProcessManager:

    def __init__(self, app_path, app_name):
        self.app_path = app_path
        self.app_name = app_name

    def get_process(self):
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == self.app_name:
                return proc
        return None

    def start(self):
        if not os.path.exists(self.app_path):
            raise FileNotFoundError(f"No existe el ejecutable: {self.app_path}")

        subprocess.Popen(
            [self.app_path],
            cwd=os.path.dirname(self.app_path),
            shell=False
    )

    def kill(self, proc):
        proc.kill()