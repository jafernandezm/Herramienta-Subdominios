import subprocess
import sys
import re
import requests
from implementaciones.sublister_exe import sublist3r_exe
from implementaciones.virustotal import get_subdomains_VirusTotal
from implementaciones.subfinder import subfinder_exec
from implementaciones.urlscan import urlscan_exec
from implementaciones.whiteintel_exec import whiteintel_exec
from implementaciones.unicosDominios import UniqueUnion

import json
import os

def get_amass(domain):
    try:
        command = [f'amass enum -d {domain} -timeout 1 -nocolor']
        amass_result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True).stdout.split()
        subdomains = [cadena for cadena in amass_result if 'gob.bo' in cadena]
        return subdomains
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando amass: {e}")
        return []


def get_crt(domain):
    try:
        subdomains = []
        response = requests.get(f'https://crt.sh/?q={domain}&output=json')
        response.raise_for_status()
        for i in response.json():
            subdomains.append(i['common_name'])
            subdomains.append(i['name_value'])
        return subdomains
    except requests.RequestException as e:
        print(f"Error obteniendo subdominios de crt.sh: {e}")
        return []

def run_dmitry(domain):
    try:
        command = ['dmitry', '-s', f'http://{domain}']
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando dmitry: {e}")
        return ""

def dns_scan(domain):
    try:
        wordlist_path = './dnscan/subdomains-10000.txt'
        command = ['dnscan/dnscan.py', '-d', domain, '-w', wordlist_path, '-t', '50']
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout
        records = re.findall(r'^([\w.-]+)\. \d+ IN (CNAME|A) (.+)', output, re.MULTILINE)
        subdomains = [record[0] for record in records]
        return subdomains
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando dnscan: {e}")
        return []

import subprocess

def httpx(union):
    if os.getenv('PATH_HTTPX'):
        PATH_HTTPX = os.getenv('PATH_HTTPX')
    else:
        PATH_HTTPX = '~/go/bin/httpx'
    try:
        unique_elements = union.get_unique_elements()
        domains = ','.join(unique_elements)
        command = f'~/go/bin/httpx -u {domains} -probe -json'
        result = subprocess.run(command, capture_output=True, text=True, shell=True, check=True)
        json_objects = []
        for line in result.stdout.splitlines():
            try:
                json_obj = json.loads(line)
                json_objects.append(json_obj)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
        return json_objects
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando httpx: {e}")
        return []


def filtrar_dominios(json_objects, domain):
    dominios_positivos = []
    dominios_negativos = []

    for obj in json_objects:
        #status_code = obj.get('status_code')
        url = obj.get('url', None)
        host = obj.get('host', None)
        tech = obj.get('tech', None)
        status_code = obj.get('status_code', None)
        # Filtrar dominios por código de estado 200 y 301
        if (status_code == 200 or status_code == 301 or status_code == 302 or status_code == 303 or status_code == 304 or status_code == 307 or status_code == 308):
            dominios_positivos.append({'url': url, 'host': host, 'status_code': status_code, 'tech': tech})
        else:
            dominios_negativos.append({'url': url, 'host': host, 'status_code': status_code, 'tech': tech})

    # Guardar en archivos JSON
    with open(f'resultados/{domain}/{domain}_positivos.json', 'w') as f_positivos:
        json.dump(dominios_positivos, f_positivos, indent=2)

    with open(f'resultados/{domain}/{domain}_negativos.json', 'w') as f_negativos:
        json.dump(dominios_negativos, f_negativos, indent=2)

    return dominios_positivos, dominios_negativos



def save_response_to_file(response, filename):
    with open(filename, 'w') as file:
        file.write(response)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 Herramienta.py <domain>")
        return
    #subdmains=[]
    domain = sys.argv[1]
    #resultados
    union = UniqueUnion()
    print('amass runing...')
    resultados_amass = get_amass(domain)
    union.add_elements(resultados_amass)
    print(f"Se encontraron {len(resultados_amass)} subdominios")
    print('-------')
    
    print('dns_scan runing...')
    resultados_dns_scan = dns_scan(domain)
    union.add_elements(resultados_dns_scan)
    #mostrar cantidad de subdominios encontrados
    print(f"Se encontraron {len(resultados_dns_scan)} subdominios")
    
    print('-------')
    #print(resultados_dns_scan)
    print('virusTotal runing...')
    resultado_virtual_total = get_subdomains_VirusTotal(domain)
    union.add_elements(resultado_virtual_total)
    print(f"Se encontraron {len(resultado_virtual_total)} subdominios")
    print('-------')
    #print('csrt runing...')
    #subdomains = set(resultados_dns_scan).union(resultado_virtual_total)
    print('subfinder runing...')
    resultado_subfinder = subfinder_exec(domain)
    union.add_elements(resultado_subfinder)
    print(f"Se encontraron {len(resultado_subfinder)} subdominios")
    print('-------')
    #sublist3r_exe(domain)
    print('sublist3r runing...')
    resultado_sublist3r_exe = sublist3r_exe(domain)
    union.add_elements(resultado_sublist3r_exe)
    print(f"Se encontraron {len(resultado_sublist3r_exe)} subdominios")
    print('urlscan runing...')
    resultado_urlscan = urlscan_exec(domain)
    union.add_elements(resultado_urlscan)
    print(f"Se encontraron {len(resultado_urlscan)} subdominios")
    print('whiteintel runing...')
    resultado_whiteintel = whiteintel_exec(domain)
    union.add_elements(resultado_whiteintel)
    print(f"Se encontraron {len(resultado_whiteintel)} subdominios")
    print('---------------------------------')
    print('-------Resultados-------')
    union.save_unique_elements_to_file(domain,f'resultado_{domain}.txt')
    resultado=httpx(union)
    #print(resultado)
    dominios_positivos,dominios_negativos=filtrar_dominios(resultado,domain)
    
    print(f"Se encontraron {len(dominios_positivos)} subdominios positivos")
    print(f"Se encontraron {len(dominios_negativos)} subdominios negativos")
    #union.print_unique_elements()
    
if __name__ == '__main__':
    main()
