# SentinelGuard

**SentinelGuard** es una solución de monitorización y gestión de procesos diseñada para supervisar aplicaciones externas en entornos Windows. La plataforma observa de forma continua el consumo de recursos (CPU y memoria) de un ejecutable determinado, reiniciándolo automáticamente si se detecta una caída o un uso excesivo, y proporciona mecanismos de consulta y control remoto a través de un servidor de sockets y una interfaz gráfica intuitiva.

---

## 🧱 Estructura del proyecto

El código fuente se organiza en módulos claramente diferenciados:

- **`monitor/`**
  - `sentinel_monitor.py` – módulo principal que inicializa el demonio de vigilancia y el servidor de comunicaciones.
  - `process_manager.py` – abstracción para iniciar, localizar y terminar el proceso supervisado.
  - `resource_checker.py` – evalúa el uso de recursos y determina advertencias de sobrecarga.
  - `socket_server.py` – servidor TCP localhost que ofrece una API simple (`status`/`restart`).

- **`gui/`** – implementación de la interfaz de usuario con Tkinter (`sentinel_gui.py`), que visualiza el estado y permite reinicios manuales.
- <img width="405" height="328" alt="image" src="https://github.com/user-attachments/assets/4555abb6-bafa-4e4a-8af2-4288e10bdd44" />


- **`config/`** – configuración en formato JSON (`config.json`) con parámetros ajustables (ruta del ejecutable, umbrales, puerto, etc.).

- **`logs/`** – directorio de salida para los registros de eventos (`sentinel.log`).
<img width="410" height="688" alt="image" src="https://github.com/user-attachments/assets/c84a5062-fa95-4938-80a6-96e695f5ed10" />



- **`monitored_app/`** – contiene un ejemplo de aplicación empaquetada; en un despliegue real, se apunta a cualquier ejecutable de interés.

---

## ⚙️ Configuración

Edite el fichero `config/config.json` con los parámetros adecuados para su entorno:

```json
{
  "app_path": "C:/ruta/a/su/ejecutable.exe",
  "app_name": "nombre_proceso.exe",
  "port": 5001,
  "max_ram_mb": 800,
  "max_cpu_percent": 85,
  "check_interval": 3
}
```

- **app_path** – Ruta absoluta al binario que se va a supervisar.
- **app_name** – Nombre del proceso (tal como aparece en el Monitor de recursos).
- **port** – Puerto TCP de escucha (localhost únicamente).
- **max_ram_mb** – Umbral de memoria RAM (MB) que provoca un reinicio.
- **max_cpu_percent** – Umbral de CPU (%) que provoca un reinicio.
- **check_interval** – Frecuencia de comprobación, en segundos.

Asegúrese de que los valores sean coherentes con los requisitos de la aplicación objetivo.

---

## 🚀 Uso

1. **Instalar dependencias** (solo `psutil`):
   ```powershell
   pip install -r requirements.txt
   ```

2. **Iniciar el servicio de vigilancia**:
   ```powershell
   python monitor/sentinel_monitor.py
   ```
   El proceso configurado se lanzará y se mantendrá bajo supervisión permanente.

3. **Lanzar la interfaz gráfica** *(opcional)*:
   ```powershell
   python gui/sentinel_gui.py
   ```
   La ventana muestra estado, métricas y ofrece un botón para reiniciar manualmente.

4. **Comunicarse mediante socket**:
   Conéctese a `localhost:<port>` y envíe la cadena `status` para obtener un JSON
   con el estado actual, o `restart` para solicitar un reinicio.
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/179ab243-ac53-4d0a-b030-c0c4694e8394" />

---

## 📁 Registro de eventos

El sistema de logging escribe sucesos relevantes (reinicios, caídas, excedencias de
recursos, errores internos) en `logs/sentinel.log`. Cada entrada incluye una marca
de tiempo para facilitar auditorías y diagnóstico.

<img width="411" height="336" alt="image" src="https://github.com/user-attachments/assets/ab1f3484-9818-422a-b246-556cb406bb9f" />
<img width="411" height="336" alt="image" src="https://github.com/user-attachments/assets/adb3fbc4-651c-4c5d-8067-f19fe128454c" />

---

## 🧩 Extensibilidad

El diseño modular permite adaptaciones sencillas:

- Modifique los umbrales y parámetros en `config.json` sin tocar el código.
- Apunte a cualquier ejecutable actualizando `app_path` y `app_name`.
- Integre clientes personalizados mediante la API de sockets (`status`/`restart`).

También se puede extender la lógica de `ResourceChecker` o reemplazar el
servidor TCP por otro protocolo según las necesidades corporativas.

---

## 🛠️ Entorno de desarrollo

- El proyecto está desarrollado para Python 3.11 y probado en Windows.
- Dependencias mínimas: `psutil` y la biblioteca estándar de Python (`socket`,
  `threading`, `tkinter`, etc.).
- La interfaz de usuario utiliza Tkinter por su disponibilidad nativa.

Para contribuir, simplemente clone el repositorio, instale las dependencias y
utilice un entorno virtual adecuado. Se recomienda mantener estilo y tipado
simples; la base de código es modular y fácil de comprender.

---

> **Nota:** el presente documento está redactado en un estilo profesional y
> estructurado; puede traducirse al inglés o adaptarse a normas internas según
> sea necesario.
