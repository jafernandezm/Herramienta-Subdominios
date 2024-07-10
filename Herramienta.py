import subprocess
import sys
import re
import requests
from sublister_exe import sublist3r_exe
from virustotal import get_subdomains_VirusTotal
from subfinder import subfinder_exec
from unicosDominios import UniqueUnion

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
    wordlist_path = './dnscan/subdomains-1000.txt'
    
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
        return None


def httprobe():
    command = 'cat dominios.txt | ./httprobe'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout

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
    print('dns_scan runing...')
    union = UniqueUnion()
    resultados_dns_scan = dns_scan(domain)
    #mostrar cantidad de subdominios encontrados
    print(f"Se encontraron {len(resultados_dns_scan)} subdominios")
    union.add_elements(resultados_dns_scan)
    #print(resultados_dns_scan)
    print('virusTotal runing...')
    resultado_virtual_total = get_subdomains_VirusTotal(domain)
    print(f"Se encontraron {len(resultado_virtual_total)} subdominios")
    union.add_elements(resultado_virtual_total)
    #print('csrt runing...')
    #subdomains = set(resultados_dns_scan).union(resultado_virtual_total)
    print('subfinder runing...')
    resultado_subfinder = subfinder_exec(domain)
    print(f"Se encontraron {len(resultado_subfinder)} subdominios")
    union.add_elements(resultado_subfinder)
    union.print_unique_elements()
    



if __name__ == '__main__':
    main()
