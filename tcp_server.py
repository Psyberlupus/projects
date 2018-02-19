import threading
import socket

bind_ip = "0.0.0.0"
bind_port = 1337

server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
server.bind((bind_ip , bind_port))
server.listen(1)
print ('[*] Listening on port : ', bind_port)

#client handling system
def handle_client(client_socket):
  request = client_socket.recv(1024)
  client_socket.send('\r\n')
  request = request + client_socket.recv(1024)
  print request
  while request:

     comm = raw_input("Command ->" )
     comm = comm + '\r\n'
     client_socket.send(comm)
     client_socket.send('\r\n')
     print "\r\n"
     
     request = client_socket.recv(1024)
     #print "recv1 "
     #print request
     #print "result\r\n"
     
     client_socket.send('\r\n')
     request = client_socket.recv(1024)
     
     while request:
            	 
           print request
           if (raw_input("Continue? (c)") == 'c'):
              request = client_socket.recv(1024)
           else: 
              break

     
     
  client_socket.close()

while True:
  client , addr = server.accept()
  print ("[*] Accepted Connection from "   ,  (addr[0],addr[1]))
  client_handler = threading.Thread(target=handle_client, args=(client,))
  client_handler.start()

  
