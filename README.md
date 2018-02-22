# projects
SMBKILLER  for all windows hosts in subnet. EternalExploits ;> XD
Looks for anonymously accessable named pipes in every windows version
Looks for ms017_010 vulnerability patch

1. exp.py -----> the main exploit script
2. hakathon.py = main.py ----> The main program caller.
3. checker.py ------> Calls exp.py and checks the host passed
4. tcp_server.py -----> Open 1337 port and handle a shell connection with hacked systems.

Prototype run :>

python hakathon.py <ip_address of windows system>