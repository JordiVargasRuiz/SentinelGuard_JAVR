import tkinter as tk
import socket
import json

PORT = 5001

def get_status():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", PORT))
        s.send("status".encode())
        data = s.recv(4096)
        s.close()
        return json.loads(data.decode())
    except:
        return None

def send_restart():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", PORT))
        s.send("restart".encode())
        s.close()
    except:
        pass

def update_ui():
    data = get_status()

    if data:
        estado_label.config(
            text="ACTIVO" if data["running"] else "CAÍDO",
            fg="green" if data["running"] else "red"
        )

        cpu_label.config(text=f"CPU: {data['cpu']} %")
        ram_label.config(text=f"RAM: {data['ram']} MB")
        restart_label.config(text=f"Reinicios: {data['restarts']}")
        event_label.config(text=f"Evento: {data['last_event']}")

    else:
        estado_label.config(text="Monitor no disponible", fg="orange")

    root.after(2000, update_ui)

root = tk.Tk()
root.title("SentinelGuard Dashboard")
root.geometry("400x300")
root.configure(bg="#1e1e1e")

tk.Label(root, text="Estado del Servicio",
         bg="#1e1e1e", fg="white", font=("Arial", 14)).pack(pady=10)

estado_label = tk.Label(root, text="Cargando...",
                        bg="#1e1e1e", font=("Arial", 16))
estado_label.pack(pady=5)

cpu_label = tk.Label(root, bg="#1e1e1e", fg="white", font=("Arial", 12))
cpu_label.pack()

ram_label = tk.Label(root, bg="#1e1e1e", fg="white", font=("Arial", 12))
ram_label.pack()

restart_label = tk.Label(root, bg="#1e1e1e", fg="white", font=("Arial", 12))
restart_label.pack()

event_label = tk.Label(root, bg="#1e1e1e", fg="white", font=("Arial", 10))
event_label.pack(pady=10)

tk.Button(root, text="Reiniciar Manualmente",
          command=send_restart,
          bg="#444", fg="white").pack(pady=10)

update_ui()
root.mainloop()