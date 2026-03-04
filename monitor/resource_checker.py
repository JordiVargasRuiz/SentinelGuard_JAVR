class ResourceChecker:

    def __init__(self, max_ram_mb, max_cpu):
        self.max_ram_mb = max_ram_mb
        self.max_cpu = max_cpu

    def check(self, proc):
        cpu = proc.cpu_percent(interval=1)
        ram = proc.memory_info().rss / (1024 * 1024)

        status = {
            "cpu": round(cpu, 2),
            "ram": round(ram, 2),
            "overload": False,
            "reason": "Operando normal"
        }

        if cpu > self.max_cpu:
            status["overload"] = True
            status["reason"] = "CPU alta"

        elif ram > self.max_ram_mb:
            status["overload"] = True
            status["reason"] = "RAM alta"

        return status