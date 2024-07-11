import subprocess
import os

def subfinder_exec(domain):
    if os.getenv('PATH_SUBFINDER'):
        PATH_SUBFINDER = os.getenv('PATH_SUBFINDER')
    else:
        PATH_SUBFINDER = '~/go/bin/subfinder'
    subdomains= []
    #command = ['~/go/bin/subfinder', '-d', domain, '-o', f'{domain}.txt']
    command = f'{PATH_SUBFINDER} -d {domain} -o {domain}.txt'
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    # leer el .txt y meterlo en una lista
    with open(f'{domain}.txt', 'r') as file:
        subdomains = [line.strip() for line in file.readlines()]
    #borrar el archivo
    subprocess.run(['rm', f'{domain}.txt'])
    return subdomains
