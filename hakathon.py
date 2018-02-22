import threading
import sys
import os
import time

def checker():
    c = "python checker.py " + sys.argv[1]
    os.system(c)
    print ("\n")
    

def handler():
    #time.sleep(0.05)
    os.system('python tcp_server.py')
	
print "SMBKILL ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print ""
print ""
print "[*] Starting Services [*]\n"

print "[*] Starting handler :) [*]\n"
shell_handler = threading.Thread(target=handler)
shell_handler.start()
print "[*] Handler Started!!! [*]\n"
print 
print 
time.sleep(5)
print "\n[*] Scanning targets [*]"
checker()

