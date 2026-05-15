import socket
from concurrent.futures import ThreadPoolExecutor

def scanner_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)
        resultat = sock.connect_ex((ip, port))
        sock.close()
        if resultat == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "inconnu"
            return {'port': port, 'service': service}
    except:
        pass
    return None

def scanner_ports(ip, port_debut, port_fin):
    ports_ouverts = []
    with ThreadPoolExecutor(max_workers=200) as executor:
        resultats = executor.map(
            lambda p: scanner_port(ip, p), 
            range(port_debut, port_fin + 1)
        )
    for r in resultats:
        if r is not None:
            ports_ouverts.append(r)
    return sorted(ports_ouverts, key=lambda x: x['port'])