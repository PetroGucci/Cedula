import requests
import os
from dotenv import load_dotenv

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
    # print("\n📡 Código de estado HTTP:", response.status_code)

    try:
        data = response.json()
        if not data.get("error"):
            persona = data["data"]
            print("\n✅ Información encontrada:")
            print(f"👤 Nombre: {persona['primer_nombre']} {persona['segundo_nombre']} {persona['primer_apellido']} {persona['segundo_apellido']}")
            print(f"🎂 Fecha de nacimiento: {persona['fecha_nac']}")
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
