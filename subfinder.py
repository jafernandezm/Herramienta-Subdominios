import subprocess

def subfinder_exec(domain):
    command = ['./subfinder', '-d', domain, '-o', f'{domain}.txt']
    result = subprocess.run(command, capture_output=True, text=True)
    # leer el .txt y meterlo en una lista
    with open(f'{domain}.txt', 'r') as file:
        subdomains = [line.strip() for line in file.readlines()]
    return subdomains
####