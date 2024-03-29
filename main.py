import random
import math

def main():
    while True:
        main_menu()
        
        opcao = input("\nDigite o número da opção desejada: ")
        if opcao == '1':
            classe_ip = input("\nDigite a classe do IP (A, B ou C): ")
            num_hosts_fora_subredes = int(input("\nDigite o número total de hosts fora das sub-redes: "))
            num_subredes = int(input("\nDigite o número de sub-redes desejadas: "))
            if num_subredes == 0:
                endereco_ip, mascara, primeiro_ip, ultimo_ip, endereco_broadcast, ips_hosts = calcular_ip(classe_ip, num_hosts_fora_subredes)
                print("================================================================")
                print("\nEndereço IP gerado:", endereco_ip)
                print("\nMáscara de Sub-rede gerada:", mascara)
                print("\nPrimeiro IP útil:", primeiro_ip)
                print("\nÚltimo IP útil:", ultimo_ip)
                print("\nEndereço de Broadcast:", endereco_broadcast)
                print("\nEndereços IP dos hosts fora das sub-redes:")
                for host, ip in ips_hosts.items():
                    print(f"\nHost {host}: {ip}")
                print("================================================================")
            else:
                subrede_especifica = input("\nDeseja saber os detalhes de uma sub-rede específica? (S/N): ")
                if subrede_especifica.upper() == 'S':
                    subrede_desejada = input("\nDigite o número da sub-rede desejada: ")
                    endereco_ip, mascara, primeiro_ip, ultimo_ip, endereco_broadcast, ips_subredes, ips_hosts = calcular_ip_e_subredes(classe_ip, num_hosts_fora_subredes, num_subredes, subrede_desejada)
                    print("\nDetalhes da Sub-rede", subrede_desejada)
                    print("\nEndereço IP reservado:", ips_subredes[subrede_desejada])
                    print("\nMáscara de Sub-rede gerada:", mascara)
                    print("\nPrimeiro IP útil:", primeiro_ip)
                    print("\nÚltimo IP útil:", ultimo_ip)
                    print("\nEndereço de Broadcast:", endereco_broadcast)
                    print("\nEndereços IP dos hosts fora das sub-redes:")
                    for host, ip in ips_hosts.items():
                        print(f"\nHost {host}: {ip}")
                else:
                    endereco_ip, mascara, primeiro_ip, ultimo_ip, endereco_broadcast, ips_subredes, ips_hosts = calcular_ip_e_subredes(classe_ip, num_hosts_fora_subredes, num_subredes)
                    print("================================================================")
                    print("\nEndereço IP gerado:", endereco_ip)
                    print("\nMáscara de Sub-rede gerada:", mascara)
                    print("\nPrimeiro IP útil:", primeiro_ip)
                    print("\nÚltimo IP útil:", ultimo_ip)
                    print("\nEndereço de Broadcast:", endereco_broadcast)
                    print("\nEndereços IP reservados para as sub-redes:")
                    for subrede, ip in ips_subredes.items():
                        print(f"\nSub-rede {subrede}: {ip}")
                    print("\nEndereços IP dos hosts fora das sub-redes:")
                    for host, ip in ips_hosts.items():
                        print(f"\nHost {host}: {ip}")
                    print("================================================================")
        elif opcao == '2':
            print("\nSalvando os detalhes da rede em um arquivo de texto...")
            salvar_detalhes_rede(endereco_ip, mascara, primeiro_ip, ultimo_ip, endereco_broadcast, ips_subredes, ips_hosts)
        elif opcao == '3':
            print("\nSaindo do programa...")
            break
        elif opcao == '4':
            continue

def main_menu():
    print("\nPROGRAMA DE CRIAÇÃO DE REDES - JOÃO MIRANDA\n")
    print("\nSELECIONE UMA OPÇÃO:")    
    print("\n1. CALCULADORA IP")
    print("\n2. SALVAR DETALHES DA REDE EM UM ARQUIVO DE TEXTO")
    print("\n3. SAIR DO PROGRAMA")

def calcular_ip(classe, num_hosts_fora_subredes):
    if classe.upper() not in ['A', 'B', 'C']:
        return "\nErro: Classe de IP inválida. Escolha entre 'A', 'B' ou 'C'.", "", "", "", "", {}

    if classe.upper() == 'A':
        primeiro_octeto = random.randint(1, 126)
        mascara_cidr = 8 + int(math.ceil(math.log2(num_hosts_fora_subredes + 2)))  # Mínimo de 2 hosts
    elif classe.upper() == 'B':
        primeiro_octeto = random.randint(128, 191)
        mascara_cidr = 16 + int(math.ceil(math.log2(num_hosts_fora_subredes + 2)))  # Mínimo de 2 hosts
    else:  # classe == 'C'
        primeiro_octeto = random.randint(192, 223)
        mascara_cidr = 24 + int(math.ceil(math.log2(num_hosts_fora_subredes + 2)))  # Mínimo de 2 hosts

    ip = f"{primeiro_octeto}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
    
    # Calcula o primeiro IP útil
    primeiro_ip = f"{primeiro_octeto}.{random.randint(0, 255)}.{random.randint(0, 255)}.1"
    
    # Calcula o último IP útil
    ultimo_ip = f"{primeiro_octeto}.{random.randint(0, 255)}.{random.randint(0, 255)}.254"
    
    # Calcula o endereço de broadcast
    endereco_broadcast = f"{primeiro_octeto}.{random.randint(0, 255)}.{random.randint(0, 255)}.255"
    
    # Calcula a máscara de sub-rede
    mascara = cidr_para_mascara(mascara_cidr)

    # Calcula os endereços IP dos hosts fora das sub-redes
    ips_hosts = {}
    for i in range(1, num_hosts_fora_subredes + 1):
        host_ip = f"{primeiro_octeto}.{random.randint(0, 255)}.{random.randint(0, 255)}.{i + 1}"
        ips_hosts[f"Host {i}"] = host_ip
    
    return ip, mascara, primeiro_ip, ultimo_ip, endereco_broadcast, ips_hosts

def calcular_ip_e_subredes(classe, num_hosts_fora_subredes, num_subredes, subrede_desejada=None):
    if num_subredes == 0:
        return calcular_ip(classe, num_hosts_fora_subredes), {}, {}
    
    if classe.upper() not in ['A', 'B', 'C']:
        return "\nErro: Classe de IP inválida. Escolha entre 'A', 'B' ou 'C'.", "", "", "", "", {}

    if classe.upper() == 'A':
        primeiro_octeto = random.randint(1, 126)
        mascara_cidr = 8 + int(math.ceil(math.log2(num_hosts_fora_subredes + num_subredes + 2)))  # Mínimo de 2 hosts por sub-rede
    elif classe.upper() == 'B':
        primeiro_octeto = random.randint(128, 191)
        mascara_cidr = 16 + int(math.ceil(math.log2(num_hosts_fora_subredes + num_subredes + 2)))  # Mínimo de 2 hosts por sub-rede
    else:  # classe == 'C'
        primeiro_octeto = random.randint(192, 223)
        mascara_cidr = 24 + int(math.ceil(math.log2(num_hosts_fora_subredes + num_subredes + 2)))  # Mínimo de 2 hosts por sub-rede

    ip = f"{primeiro_octeto}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
    
    # Calcula o primeiro IP útil
    primeiro_ip = f"{primeiro_octeto}.{random.randint(0, 255)}.{random.randint(0, 255)}.1"
    
    # Calcula o último IP útil
    ultimo_ip = f"{primeiro_octeto}.{random.randint(0, 255)}.{random.randint(0, 255)}.254"
    
    # Calcula o endereço de broadcast
    endereco_broadcast = f"{primeiro_octeto}.{random.randint(0, 255)}.{random.randint(0, 255)}.255"
    
    # Calcula a máscara de sub-rede
    mascara = cidr_para_mascara(mascara_cidr)
    
    # Calcula os endereços IP reservados para as sub-redes
    ips_subredes = {}
    for i in range(1, num_subredes + 1):
        subrede_ip = f"{primeiro_octeto}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
        ips_subredes[f"\nSub-rede {i}"] = subrede_ip
    
    # Calcula os endereços IP dos hosts fora das sub-redes
    ips_hosts = {}
    for i in range(1, num_hosts_fora_subredes + 1):
        host_ip = f"{primeiro_octeto}.{random.randint(0, 255)}.{random.randint(0, 255)}.{i + 1}"
        ips_hosts[f"\nHost {i}"] = host_ip
    
    return (ip, mascara, primeiro_ip, ultimo_ip, endereco_broadcast), ips_subredes, ips_hosts

def salvar_detalhes_rede(endereco_ip, mascara, primeiro_ip, ultimo_ip, endereco_broadcast, ips_subredes, ips_hosts):
    with open("detalhes_rede.txt", "w") as file:
        file.write("\nDETALHES DA REDE\n\n")
        file.write(f"\nEndereço IP: {endereco_ip}\n")
        file.write(f"\nMáscara de Sub-rede: {mascara}\n")
        file.write(f"\nPrimeiro IP útil: {primeiro_ip}\n")
        file.write(f"\nÚltimo IP útil: {ultimo_ip}\n")
        file.write(f"\nEndereço de Broadcast: {endereco_broadcast}\n\n")
        file.write("\nEndereços IP reservados para as sub-redes:\n")
        for subrede, ip in ips_subredes.items():
            file.write(f"\nSub-rede {subrede}: {ip}\n")
        file.write("\n\nEndereços IP dos hosts fora das sub-redes:\n")
        for host, ip in ips_hosts.items():
            file.write(f"\nHost {host}: {ip}\n")

def cidr_para_mascara(cidr):
    bits = 0xffffffff ^ (1 << 32 - cidr) - 1
    return ".".join(map(str, [bits >> 24, (bits >> 16) & 0xff, (bits >> 8) & 0xff, bits & 0xff]))

if __name__ == "__main__":
    main()
