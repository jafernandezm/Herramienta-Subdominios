import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

VIRUSTOTAL_API_KEY = os.getenv('VIRUSTOTAL_API_KEY')

def get_subdomains_VirusTotal(domain):
    url = f"https://www.virustotal.com/vtapi/v2/domain/report?apikey={VIRUSTOTAL_API_KEY}&domain={domain}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud HTTP: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error al decodificar la respuesta JSON: {e}")
        return []

    subdomains = data.get('subdomains', [])
    return subdomains


