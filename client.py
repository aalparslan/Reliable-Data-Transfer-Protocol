from socket import *
from time import sleep as SLEEP
from time import time
from ortak import ip_checksum
import sys



serverName = sys.argv[1]
clientName = ''
serverUDPPort = int(sys.argv[2])
clientUDPPort = int(sys.argv[4])
serverTCPPort = int(sys.argv[3])
clientTCPPort = int(sys.argv[5])
BUFFER_SIZE = 1000
SEGMENT_SIZE = 900
SEGMENT_SIZE_TCP = 1000
InputFileNameForTCPconnection = "tcpSent.txt"
InputFileNameForUDPconnection = "udpSent.txt"




milliseconds = lambda: int(time() * 1000)


def udpSend(serverName, clientName, serverUDPPort, clientUDPPort):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    fileUDP = open(InputFileNameForUDPconnection,'r', encoding="utf8")

    #specify senderudpport do not leave it to OS
    clientSocket.bind((clientName,clientUDPPort))
    data  = fileUDP.read()

    clientSocket.settimeout(2)
    offset = 0
    seq = 0
    while offset < len(data):
        if offset + SEGMENT_SIZE > len(data):
            segment = data[offset:]
        else:
            segment = data[offset:offset + SEGMENT_SIZE]
        offset += SEGMENT_SIZE

        ack_received = False
        while not ack_received:
            mtime = str(milliseconds())
            clientSocket.sendto((ip_checksum(segment + mtime) + str(seq)+ mtime + segment).encode('utf-8'), (serverName, serverUDPPort))
            try:
                message, address = clientSocket.recvfrom(BUFFER_SIZE)
                try:
                    message = message.decode()
                except UnicodeDecodeError:
                #    print("UnicodeDecodeError")
                    continue

            #    print("ACK message : " + message)
            except timeout:
                print ("Timeout")
            else:
                checksum = message[:2]
                ack_seq = message[5]
                timeOnTheOtherEndWhenThisSent = message[6:]


                # if(ip_checksum(message[2:]) == checksum):
                #     if(ack_seq != str(seq)):
                #         print("Acks not equal")
                # else:
                #     print("checksums not equal!")




                if(ip_checksum(message[2:]) == checksum and ack_seq == str(seq)):
                    ack_received = True
                #    print("sengment sent successfully!")
                #else:
                #    print("re-transmitting...")
    #    print("whiledan cikti!")
        seq = 1 - seq

    clientSocket.close()
    fileUDP.close()
    #print("file sent")



def tcpSend(serverName, clientName, serverTCPPort, clientTCPPort ):
    #open the file in reading mode to be sent.
    fileTCP = open(InputFileNameForTCPconnection,'r')
    clientSocket = socket(AF_INET, SOCK_STREAM)


    #specify senderTCPport do not leave it to OS
    clientSocket.bind((clientName,clientTCPPort))
    clientSocket.connect((serverName, serverTCPPort))



    data = fileTCP.read()

    offset = 0
    while offset < len(data):
        if offset + SEGMENT_SIZE_TCP > len(data):
            segment = data[offset:]
        else:
            segment = data[offset:offset + SEGMENT_SIZE_TCP]
        offset += SEGMENT_SIZE_TCP


        clientSocket.send(( segment + "ClientTime:" + str(milliseconds()) + "Deli-1-meter").encode())
        #Ttime = "ClientTime:" + str(milliseconds()) + "Deli-1-meter"
        #clientSocket.send((Ttime).encode())
        SLEEP(0.01)


    fileTCP.close()
    #print("file sent ")
    clientSocket.shutdown(SHUT_RDWR)
    clientSocket.close()






udpSend(serverName, clientName, serverUDPPort, clientUDPPort)
SLEEP(15)
tcpSend(serverName, clientName, serverTCPPort, clientTCPPort )
