import dns.resolver
import argparse
import socket
import requests
def get_dns_servers(domain):
    try:
        answers = dns.resolver.resolve(domain, 'NS')
        dnsList=[rdata.to_text() for rdata in answers]
        dnsIpList = []
        try:
            for domainDns in dnsList:
                dns_ips = dns.resolver.resolve(domainDns)
                for ip in dns_ips:
                    dnsIpList.append(ip.to_text())
        except dns.resolver.NoAnswer:
                print(f'No IP address found for {domain}')
        except dns.resolver.NXDOMAIN:
                print(f'{domain} does not exist')
        except Exception as e:
                print(f'An error occurred while resolving {domain}: {e}')
        #print(dnsIpList)
        return dnsIpList
    except dns.resolver.NoAnswer:
        print(f'No answer for {domain}')
        return []
    except dns.resolver.NXDOMAIN:
        print(f'{domain} does not exist')
        return []
    except Exception as e:
        print(f'An error occurred: {e}')
        return []

def consultar_dns(subDominios, servidores_dns):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = servidores_dns
    listSubdomain = []
    for subdominio in subDominios:
        #print(f'testing {subdominio}')
        try:
            respuesta = resolver.resolve(subdominio, 'A')
            for ip in respuesta:
                listSubdomain.append(subdominio)
                #print(f'{subdominio} tiene la dirección IP: {ip}')
        except dns.resolver.NXDOMAIN:
            #print(f'{subdominio} no existe.')
            continue
        except dns.resolver.Timeout:
            #print(f'La consulta ha expirado.')
            continue
        except dns.resolver.NoNameservers:
            #print(f'No hay servidores DNS disponibles.')
            continue
        except Exception as e:
            continue
            #print(f'Ha ocurrido un error: {e}')
    return listSubdomain
