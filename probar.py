import subprocess
import re

def remove_color_codes(text):
    # Expresión regular para eliminar códigos de color ANSI
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def subliter(domain):
    subdomains = []
    command = ['python3', 'Sublist3r-master/sublist3r.py', '-d', domain]
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode == 0:
        cleaned_output = remove_color_codes(result.stdout)
        output_lines = cleaned_output.splitlines()
        for line in output_lines:
            if line.startswith('[-]') or line.startswith('[!]'):
                continue
            match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b|((?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,6}\b', line)
            if match:
                subdomains.append(match.group())
    
    return subdomains

def main():
    domain = 'agetic.gob.bo'
    subdomains = subliter(domain)
    for subdomain in subdomains:
        print(subdomain)

if __name__ == '__main__':
    main()
