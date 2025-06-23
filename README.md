# PharmacyCompare

Este proyecto es una aplicación web Flask para comparar inventarios y precios de productos entre farmacias.

## Requisitos
- Python 3.8 o superior
- pip

## Instalación y configuración del ambiente

1. **Clona el repositorio o descarga el código fuente.**

   Para clonar con Git:
   ```sh
   git clone https://github.com/usuario/PharmacyCompare.git
   cd PharmacyCompare
   ```

2. **Crea un entorno virtual (recomendado):**

   En Windows:
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```
   En Mac/Linux:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instala las dependencias:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Configura las variables de entorno (opcional):**
   Puedes crear un archivo `.env` en la raíz del proyecto para definir la clave secreta y otras variables:
   ```env
   SESSION_SECRET=una_clave_secreta_muy_dificil_de_adivinar_12345
   FLASK_ENV=development
   ```

5. **Inicializa la base de datos:**
   La base de datos SQLite se crea automáticamente al iniciar la app por primera vez.

6. **Ejecuta la aplicación:**
   ```sh
   python app.py
   ```
   Luego abre tu navegador en [http://localhost:5000](http://localhost:5000)

7. **Si tienes problemas al iniciar sesión o con variables de entorno:**
   Si al iniciar la aplicación ves un error como:
   
   ```
   ModuleNotFoundError: No module named 'dotenv'
   ```
   o
   ```
   ImportError: cannot import name 'find_dotenv' from 'dotenv'
   ```
   
   Debes instalar el paquete `python-dotenv` ejecutando:
   ```sh
   pip install python-dotenv
   ```
   Esto es necesario para que Flask pueda cargar las variables de entorno desde el archivo `.env`.

## Notas de seguridad
- En desarrollo, puedes dejar `SESSION_COOKIE_SECURE=False` para evitar problemas con CSRF en HTTP.
- Para producción, asegúrate de usar HTTPS y una clave secreta fuerte.

## Estructura del proyecto
- `app.py`: Archivo principal de la aplicación Flask.
- `requirements.txt`: Dependencias del proyecto.
- `pharmacy_data.py`, `forms.py`, `models.py`: Lógica y modelos de la app.
- `templates/`: Archivos HTML (Jinja2).
- `static/`: Archivos estáticos (CSS, JS, imágenes).

---

¡Listo! Si tienes dudas, revisa el código o consulta la documentación de Flask.
