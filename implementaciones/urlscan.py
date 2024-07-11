import requests
import json

def urlscan_exec(domain):
    url = f"https://urlscan.io/api/v1/search/?q=domain:{domain}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica si la solicitud fue exitosa
        data = response.json()  # Intenta decodificar la respuesta JSON
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud HTTP: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error al decodificar la respuesta JSON: {e}")
        return []

    results = data.get('results', [])
    subdomains = []
    for result in results:
        page = result.get('page')
        if page:
            domain = page.get('url')
            if domain:  # Verifica que el dominio no sea None
                subdomains.append(domain)

    return subdomains
