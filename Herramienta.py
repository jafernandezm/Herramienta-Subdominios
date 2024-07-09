import subprocess
import sys
import re




def run_dmitry(domain):
    command = ['dmitry', '-s', 'http://{}'.format(domain)]
    result = subprocess.run(command, capture_output=True, text=True)
    print(result)
    return result.stdout

def dns_scan(domain):
    # Asegúrate de que la ruta al archivo de lista de palabras sea correcta
    wordlist_path = './dnscan/subdomains-1000.txt'
    
    # Estructura correcta de la lista command, separando cada argumento
    command = ['dnscan/dnscan.py', '-d', domain, '-w', wordlist_path, '-t', '50']
    
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        output = result.stdout
        # Filtrar dominios y direcciones IP usando expresiones regulares
        records = re.findall(r'^([\w.-]+)\. \d+ IN (CNAME|A) (.+)', output, re.MULTILINE)
        
        # Almacenar resultados en un array de diccionarios
        results = []
        for record in records:
            if record[1] == 'CNAME':
                results.append({'sitio': record[0]})
            elif record[1] == 'A':
                results.append({'sitio': record[0], 'ip': record[2]})
        
        return results
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
        print("Usage: python3 analyze_domain.py <domain>")
        return
    
    domain = sys.argv[1]
    dnsscan = dns_scan(domain)
    #como guardo los dominios en un txt
    with open('dominios.txt', 'w') as file:
        for d in dnsscan:
            file.write(d['sitio'] + '\n')
    resultados = httprobe()
    print(resultados)
    

    
    #save_response_to_file(response, 'dmitry_output.txt')

if __name__ == '__main__':
    main()
