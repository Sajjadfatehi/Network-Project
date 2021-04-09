import socket
import  threading
from queue import Queue

print_lock=threading.Lock()

servises={
    'http':80,
    'tls':443,
    'smpt':25,
    'ftp':21,
    'telnet':23,
    'ssh':22
}
print("input host :\n")
host=input()
if host is None:
    host='8.8.8.8'

print("specific port\n")
mySpecificPort=int(input())
if mySpecificPort is None:
    mySpecificPort=10

print("service :\n")
service=input()
if service is None:
    service='http'


print("default time out :\n")
defTimeOut=int(input())
if defTimeOut is None:
    defTimeOut=1


startPort=1
endPort=101
print("port start and end limitation :\n")
portsLimit=input()
if len(portsLimit.split(" "))>=2 :
    myPorts=portsLimit.split(" ")
    startPort=int(myPorts[0])
    endPort=int(myPorts[1])


print("thread number :\n")
threadCount=int(input())
if threadCount is None or threadCount>1000:
    threadCount=200



def portScan(port) :
    mySocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket.setdefaulttimeout(defTimeOut)
    try:
        connect=mySocket.connect((host,port))
        with print_lock:
            print('port :',port,' is open')
        connect.close()
    except:
        pass    

queue=Queue()
queue2=Queue()

def threader():
    while True:
        worker=queue.get()
        portScan(worker)
        queue.task_done()

def specificPort(port):
    queue2.put(port)

for x in range(threadCount):
    thread=threading.Thread(target=threader)
    thread.daemon=True
    thread.start()

#for all ports
for worker in range(startPort,endPort):
    queue.put(worker)

queue.join()

portScan(mySpecificPort)

portScan(servises.get(service))
