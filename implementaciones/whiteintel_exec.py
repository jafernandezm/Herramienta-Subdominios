
import os
from dotenv import load_dotenv
import requests
load_dotenv()
import json

BEARER_WHITEINTEL=os.getenv('BEARER_WHITEINTEL')

def whiteintel_exec(domain):
    # por post
    url = f"https://whiteintel.io/url_handler.php"
    headers = {
        'Authorization': f'Bearer {BEARER_WHITEINTEL}',
        'Content-Type': 'application/json'
    }
    data = {
        "domain": domain
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        data = response.json()
        # del json necestio entrar a leak_urls_customer y luego sacar solo url
        resultados = data.get('leak_urls_customer', [])
        subdomains = []
        for resultado in resultados:
            url = resultado.get('url')
            if url:
                subdomains.append(url)
            
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud HTTP: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error al decodificar la respuesta JSON: {e}")
        return []
    return subdomains


    
