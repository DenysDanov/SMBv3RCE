from colorama import Fore, Back, Style
import socket
import struct
import sys
from netaddr import IPNetwork


pkt = b'\x00\x00\x00\xc0\xfeSMB@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00$\x00\x08\x00\x01\x00\x00\x00\x7f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00x\x00\x00\x00\x02\x00\x00\x00\x02\x02\x10\x02"\x02$\x02\x00\x03\x02\x03\x10\x03\x11\x03\x00\x00\x00\x00\x01\x00&\x00\x00\x00\x00\x00\x01\x00 \x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\n\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00'
f = open('./hosts.txt','rt')
subnet = f.read().split('\n')
result = []

hello_msg = f'''
\n\n
{"*"*28}
                                
           _______  ______  
|\     /|(  ____ \(  __  \ 
| )   ( || (    \/| (  \  )
| |   | || |      | |   ) |
| |   | || |      | |   | |
| |   | || |      | |   ) |
| (___) || (____/\| (__/  )
(_______)(_______/(______/ 
                                       
          
          
{"*"*28}
'''
print(Fore.GREEN + hello_msg)
print(Fore.CYAN + f'{len(subnet)} IP got')
for s_ip in subnet:
    try:
        for ip in IPNetwork(s_ip):
            print(Fore.CYAN + f"[INFO]\t{ip} \t| Checking...")
            sock = socket.socket(socket.AF_INET)
            sock.settimeout(3)

            try:
                sock.connect(( str(ip),  445 ))
            except Exception as e:
                print(Fore.RED + f'[ERROR]\t{ip} \t| {e}')  
                sock.close()
                continue

            sock.send(pkt)
            nb, = struct.unpack(">I", sock.recv(4))
            res = sock.recv(nb)

            if res[68:70] != b"\x11\x03" or res[70:72] != b"\x02\x00":
                print(Fore.RED + f"[INFO]\t{ip} \t| Not vulnerable.")
            else:
                result.append(str(ip))
                print(Fore.GREEN + f"[SUCCESS]\t{ip} \t| Vulnerable")
    except KeyboardInterrupt:
        print(Fore.WHITE + 'Interrupted')
        break
    
    except Exception as e:
        print(Fore.RED + f'[Error]\t{e}')
        continue

try:
    open('result.txt','wt').write("\n".join(result))
except Exception as e:
    print(Fore.RED + f'[Error]\tFile output error {e}')
else:
    print(Fore.GREEN + f'Successfully saved {len(result)} IP adresses')

print(Fore.RESET)