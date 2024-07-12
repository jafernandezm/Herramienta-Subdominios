import subprocess
from tqdm import tqdm
import re

# Leer los dominios del archivo
with open("dominios.txt", "r") as file:
    dominios = [line.strip() for line in file]

# Agrupar los dominios en grupos de 10
grupos = [dominios[i:i+10] for i in range(0, len(dominios), 10)]

# Variable para almacenar el último número procesado
ultimo_numero = 0

# Configurar la barra de progreso
total_grupos = len(grupos)
pbar_grupos = tqdm(total=total_grupos, desc="Grupos", unit="grupo")

# Recorrer cada grupo de dominios
for grupo in grupos:
    # Configurar la barra de progreso para el grupo actual
    total_dominios_grupo = len(grupo)
    pbar_dominios = tqdm(total=total_dominios_grupo, desc="Dominios", unit="dominio", leave=False)

    # Recorrer cada dominio en el grupo
    for dominio in grupo:
        # Ejecutar la herramienta con el dominio actual
        comando = f"python3 Herramienta.py {dominio}"
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)

        # Buscar el número dentro de la salida
        numero_match = re.search(r"Se encontraron (\d+) subdominios", resultado.stdout)
        if numero_match:
            numero = int(numero_match.group(1))
            if numero > ultimo_numero:
                ultimo_numero = numero

        # Actualizar la barra de progreso del grupo
        pbar_dominios.update(1)

    # Cerrar la barra de progreso del grupo
    pbar_dominios.close()

    # Actualizar la barra de progreso de los grupos
    pbar_grupos.update(1)

# Cerrar la barra de progreso de los grupos
pbar_grupos.close()

# Guardar el último número en un archivo
with open("ultimo_numero.txt", "w") as file:
    file.write(str(ultimo_numero))