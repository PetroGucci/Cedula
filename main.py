import requests
import os
from dotenv import load_dotenv
from datetime import datetime  # Importar datetime para manejar fechas

# Cargar variables de entorno desde .env
load_dotenv()

APP_ID = os.getenv("APP_ID")
TOKEN = os.getenv("TOKEN")

def consultar_cedula(nacionalidad, cedula):
    url = "https://api.cedula.com.ve/api/v1"
    params = {
        "app_id": APP_ID,
        "token": TOKEN,
        "nacionalidad": nacionalidad.upper(),
        "cedula": cedula
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, params=params, headers=headers)

    print("\n=== Consulta de Cédula Venezolana ===")

    try:
        data = response.json()
        if not data.get("error"):
            persona = data["data"]
            
            # Construir el nombre completo sin errores si faltan datos
            nombre_completo = " ".join([
                persona.get("primer_nombre", ""),
                persona.get("segundo_nombre", ""),
                persona.get("primer_apellido", ""),
                persona.get("segundo_apellido", "")
            ]).strip()

            # Formatear la fecha de nacimiento al formato DD-MM-YYYY
            fecha_nac = persona.get("fecha_nac", "")
            try:
                fecha_nac_obj = datetime.strptime(fecha_nac, "%Y-%m-%d")
                fecha_nac_formateada = fecha_nac_obj.strftime("%d-%m-%Y")
            except ValueError:
                fecha_nac_formateada = fecha_nac  # Si hay error, usar la fecha original

            print("\n✅ Información encontrada:")
            print(f"👤 Nombre: {nombre_completo}")
            print(f"🎂 Fecha de nacimiento: {fecha_nac_formateada}")
            print(f"🆔 RIF: {persona['rif']}")
        else:
            print("❌ Error desde la API:", data.get("error_str"))
    except requests.exceptions.JSONDecodeError:
        print("❌ La respuesta no es JSON válida. Verifica que el APP_ID, el TOKEN y los datos enviados sean correctos.")
        print("🔍 Respuesta recibida:\n", response.text)

if __name__ == "__main__":
    print("=== Consulta de Cédula Venezolana ===")
    nacionalidad = input("Ingresa tu nacionalidad (V o E): ").strip().upper()
    cedula = input("Ingresa tu número de cédula: ").strip()

    if not APP_ID or not TOKEN:
        print("❗ ERROR: Faltan APP_ID o TOKEN en el archivo .env")
    elif not cedula.isdigit() or nacionalidad not in ("V", "E"):
        print("❗ ERROR: Datos inválidos. Asegúrate de ingresar una nacionalidad válida y un número de cédula numérico.")
    else:
        consultar_cedula(nacionalidad, cedula)
