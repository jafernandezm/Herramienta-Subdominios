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

def get_amass(domain):
    command = [f'amass enum -d {domain} -timeout 1 -nocolor']
    amass_result = subprocess.run(command,shell=True,capture_output=True,text=True).stdout.split()
    subdomains = [cadena for cadena in amass_result if 'gob.bo' in cadena]
    return subdomains


def get_crt(domain):
    subdomains=[]
    response = requests.get('https://crt.sh/?q=%s&output=json' % domain)
    for i in response.json():
        subdomains.append(i['common_name'])
        subdomains.append(i['name_value'])
    return subdomains

def run_dmitry(domain):
    command = ['dmitry', '-s', 'http://{}'.format(domain)]
    result = subprocess.run(command, capture_output=True, text=True)
    #print(result)
    return result.stdout

def dns_scan(domain):
    # Asegúrate de que la ruta al archivo de lista de palabras sea correcta
    wordlist_path = './dnscan/subdomains-10000.txt'
    
    # Estructura correcta de la lista command, separando cada argumento
    command = ['dnscan/dnscan.py', '-d', domain, '-w', wordlist_path, '-t', '50']
    
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        output = result.stdout
        # Filtrar dominios usando expresiones regulares
        records = re.findall(r'^([\w.-]+)\. \d+ IN (CNAME|A) (.+)', output, re.MULTILINE)
        
        # Almacenar resultados en una lista de subdominios
        subdomains = [record[0] for record in records]
        
        return subdomains
    else:
        print(f"Error: {result.stderr}")
        return {}

import subprocess

def httpx(union):
    unique_elements = union.get_unique_elements()
    domains = ','.join(unique_elements)
    command = f'~/go/bin/httpx -u {domains} -probe -json'
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    
    # Procesar cada línea de la salida como JSON y devolver la lista de objetos JSON
    json_objects = []
    for line in result.stdout.splitlines():
        try:
            json_obj = json.loads(line)
            json_objects.append(json_obj)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    
    return json_objects

def filtrar_dominios(json_objects, domain):
    dominios_positivos = []
    dominios_negativos = []

    for obj in json_objects:
        status_code = obj.get('status_code')
        url = obj.get('url', None)
        host = obj.get('host', None)
        status_code = obj.get('status_code', None)
        # Filtrar dominios por código de estado 200 y 301
        if (status_code == 200 or status_code == 301 or status_code == 302 or status_code == 303 or status_code == 304 or status_code == 307 or status_code == 308):
            dominios_positivos.append({'url': url, 'host': host, 'status_code': status_code})
        else:
            dominios_negativos.append({'url': url, 'host': host, 'status_code': status_code})

    # Guardar en archivos JSON
    with open(f'{domain}_positivos.json', 'w') as f_positivos:
        json.dump(dominios_positivos, f_positivos, indent=2)

    with open(f'{domain}_negativos.json', 'w') as f_negativos:
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
    print(f"Se encontraron {len(resultados_amass)} subdominios")
    print('-------')
    union.add_elements(resultados_amass)
    print('dns_scan runing...')
    resultados_dns_scan = dns_scan(domain)
    #mostrar cantidad de subdominios encontrados
    print(f"Se encontraron {len(resultados_dns_scan)} subdominios")
    union.add_elements(resultados_dns_scan)
    print('-------')
    #print(resultados_dns_scan)
    print('virusTotal runing...')
    resultado_virtual_total = get_subdomains_VirusTotal(domain)
    print(f"Se encontraron {len(resultado_virtual_total)} subdominios")
    union.add_elements(resultado_virtual_total)
    print('-------')
    #print('csrt runing...')
    #subdomains = set(resultados_dns_scan).union(resultado_virtual_total)
    print('subfinder runing...')
    resultado_subfinder = subfinder_exec(domain)
    print(f"Se encontraron {len(resultado_subfinder)} subdominios")
    union.add_elements(resultado_subfinder)
    print('-------')
    #sublist3r_exe(domain)
    print('sublist3r runing...')
    resultado_sublist3r_exe = sublist3r_exe(domain)
    print(f"Se encontraron {len(resultado_sublist3r_exe)} subdominios")
    union.add_elements(resultado_sublist3r_exe)

    print('urlscan runing...')
    resultado_urlscan = urlscan_exec(domain)
    print(f"Se encontraron {len(resultado_urlscan)} subdominios")
    union.add_elements(resultado_urlscan)
    
    print('whiteintel runing...')
    resultado_whiteintel = whiteintel_exec(domain)
    print(f"Se encontraron {len(resultado_whiteintel)} subdominios")
    union.add_elements(resultado_whiteintel)
    print('---------------------------------')
    
    print('-------Resultados-------')

#    union.save_unique_elements_to_file(f'resultado_{domain}.txt')
    resultado=httpx(union)
    #print(resultado)
    dominios_positivos,dominios_negativos=filtrar_dominios(resultado,domain)
    
    print(f"Se encontraron {len(dominios_positivos)} subdominios positivos")
    print(f"Se encontraron {len(dominios_negativos)} subdominios negativos")
    #union.print_unique_elements()
    
if __name__ == '__main__':
    main()
