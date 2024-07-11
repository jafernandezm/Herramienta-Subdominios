# Proyecto de Herramienta de Análisis de Dominios para Linux

Este proyecto proporciona una herramienta para analizar dominios utilizando las APIs de VirusTotal y WhiteIntel.

## Instalación

1. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

Asignar permisos de ejecución al script de instalación:
```
chmod +x instalar.sh 
./instalar.sh
```
## Uso
Para ejecutar la herramienta, usa el siguiente comando:
```
python3 Herramienta.py example.com

```

## Configuración
Antes de ejecutar la herramienta, asegúrate de configurar las claves API en el archivo .env. Crea un archivo .env en la raíz del proyecto con el siguiente contenido:
- [virustotal](https://www.virustotal.com/gui/home/upload)
- [whiteintel](https://whiteintel.io/login)

```
VIRUSTOTAL_API_KEY=tu_clave_api_de_virustotal
BEARER_WHITEINTEL=tu_clave_api_de_whiteintel

```

### Resultados
Los resultados del análisis se guardarán en dos archivos JSON, uno para positivos y otro para negativos, ambos nombrados según el dominio analizado.