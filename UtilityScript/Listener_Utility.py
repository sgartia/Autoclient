#Socket client example in python
 
import socket   #for sockets
import sys  #for exit
 
#create an INET, STREAMing socket
try:
    s = socket.socket(socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
     
print 'Socket Created'
 
host = '172.30.31.10';
port = 45678;

 
#Connect to remote server
s.connect((host , port))
 
print 'Socket Connected to ' + host + ' on ip ' + str(port)
 
#Send some data to remote server
message = "GET / HTTP/1.1\r\n\r\n"
 
try :
    #Set the whole string
    s.sendall(message)
except socket.error:
    #Send failed
    print 'Send failed'
    sys.exit()
 
print 'Message send successfully'
 
#Now receive data
reply = s.recv(4096)
 
print reply
