import subprocess
import re
import sublist3r

  

def sublist3r(domain):
    no_threads = 10  # Número de hilos que Sublist3r usará
    savefile = None  # No guardaremos los resultados en un archivo
    ports = None  # No escanearemos puertos
    silent = True  # No mostramos salida detallada
    verbose = False  # No mostramos salida detallada
    enable_bruteforce = False  # No habilitamos fuerza bruta
    engines = None  # Usamos todos los motores de búsqueda disponibles
    
    subdomains = sublist3r.main(domain, no_threads, savefile, ports, silent, verbose, enable_bruteforce, engines)
    #print(subdomains)
    return subdomains

def main():
    domain = 'agetic.gob.bo'
    subdomains = subliter(domain)
    print(subdomains)

if __name__ == '__main__':
    main()
