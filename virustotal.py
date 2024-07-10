
import requests
import json


VIRUSTOTAL_API_KEY = '0bb035867ad4189f1ad82c124dea6315d1cb7fd7e70f67f06b26feaf4b54e429'

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



