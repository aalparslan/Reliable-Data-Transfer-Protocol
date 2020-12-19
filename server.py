

from socket import *
import sys
from time import time
from time import sleep as SLEEP
from ortak import ip_checksum



serverName = ''


serverUDPPort = int(sys.argv[1])
serverTCPPort = int(sys.argv[2])
BUFFER_SIZE = 1000
tcpBUFFER = 913

OutputNameFileForTCPconnection = "tcpReceived.txt"
OutputNameFileForUDPconnection = "udpReceivedd.txt"

totalTimeElapsedTransmittingUdp = 0
receivedUdpPacketCounter = 0
reTransmittedUdpPacketCounter = 0

totalTimeElapsedTransmittingTcp = 0
receivedTcpPacketCounter = 0
currentStime = 0

milliseconds = lambda: int(time() * 1000)


def  send(udpSocket, info, to ):
    mtime = str(milliseconds())
    checksum = ip_checksum(info + mtime)
    udpSocket.sendto((checksum + info + mtime ).encode("utf-8"), to)

def listenUDP(udpSocket):
    data, addr = udpSocket.recvfrom(BUFFER_SIZE)
    timeWhenPacketReceived = milliseconds()
    expected_seq = 0
    udpSocket.settimeout(10)
    fileUDP = open(OutputNameFileForUDPconnection, 'w')
    #print("Connection from", addr)
    try:
        while (data):
            try:
                data = data.decode("utf-8")
            except UnicodeDecodeError:
                #print("UnicodeDecodeError")
                negative_seq = str(1- expected_seq)
                send(udpSocket, "ACK" + negative_seq, addr)
                global reTransmittedUdpPacketCounter
                reTransmittedUdpPacketCounter = reTransmittedUdpPacketCounter +1
                #print("Wainting on re-transmission...")
                data, addr = udpSocket.recvfrom(BUFFER_SIZE)
                timeWhenPacketReceived = milliseconds()
                continue

            checksum = data[:2]
            seq = data[2]
            content = data[16:]
            timeOnTheOtherEndWhenThisSent = data[3:16]
            """
            print("\n")
            print("data :" + data)
            print("checksum :" + data[:2])
            print("seq :" + seq)
            print("content :" + content)
            print("timeOnTheOtherEndWhenThisSent :" + timeOnTheOtherEndWhenThisSent)
            print("checksum :" + ip_checksum(content+timeOnTheOtherEndWhenThisSent))
            """
            #print("\n")

            if(ip_checksum(content+timeOnTheOtherEndWhenThisSent) == checksum):

                send(udpSocket, "ACK" + seq,addr) #send to where it cane from.
                if seq == str(expected_seq):
                    ##### Write data here
                    #print("data is written")
                    fileUDP.write(content)
                    #update stats since there is no mistake in the for sure
                    global receivedUdpPacketCounter
                    receivedUdpPacketCounter =  receivedUdpPacketCounter + 1
                    global totalTimeElapsedTransmittingUdp
                    totalTimeElapsedTransmittingUdp = totalTimeElapsedTransmittingUdp + (timeWhenPacketReceived - int(timeOnTheOtherEndWhenThisSent))
                    expected_seq = 1 - expected_seq
                #else:
                #    print("data is not written -seqs are not equal")
            else:
                negative_seq = str(1- expected_seq)
                #print("data is not written -checksums are not equal")
                send(udpSocket, "ACK" + negative_seq, addr) #send to where it cane from.

                reTransmittedUdpPacketCounter = reTransmittedUdpPacketCounter + 1

            data, addr = udpSocket.recvfrom(BUFFER_SIZE)
            timeWhenPacketReceived = milliseconds()
    except timeout:
        print ("Timeout")
    else:
        fileUDP.close()
        udpSocket.close()
        #print("File received")

def stringExtractor(delimeter, rawString):
    idx = rawString.find(delimeter)
    return rawString[idx +11:idx+24]




def listenTCP(tcpSocket):

    connectionSocket, addr = tcpSocket.accept()

    mybuffer = ""

    # if there is a connection then open the file to be written.
    fileTCP = open(OutputNameFileForTCPconnection, 'w')
    #print("Connection from", addr)
    #print("File is coming via TCP")
    data = ""
    while(True):

        data = connectionSocket.recv(1000)
        timeWhenPacketReceived = milliseconds()
        if not data:
        #    print("np data")
            break
        else:
            mybuffer += "ServerTime:" + str(timeWhenPacketReceived)
            mybuffer +=  data.decode()

    strings = mybuffer.split('Deli-1-meter')
    for s in strings:

        result = s.find("ServerTime:")
        if(result != -1):
        #    print("\n")
            sTime = s[result+11:result+24]
            global currentStime
            try:
                currentStime = int(sTime)
            except ValueError:
                continue

        #    print("sTime --> " +sTime)

        result = s.find("ClientTime:")
        if(result != -1):
            cTime = s[result+11:result+24]
            global receivedTcpPacketCounter
            receivedTcpPacketCounter += 1
            try:
                Clienttime = int(cTime)
            except ValueError:
                continue
            else:
                global totalTimeElapsedTransmittingTcp
                totalTimeElapsedTransmittingTcp += currentStime - Clienttime
            #print("cTime ---> " +cTime)



    #write to a file
    #below removes ServerTime

    while True:
        indexOfsTime = mybuffer.find("ServerTime:")

        if(indexOfsTime == -1):
            break
        mybuffer = mybuffer[:indexOfsTime] + mybuffer[indexOfsTime+24:]

    #below removes ClientTime
    while True:
        indexOfcTime =  mybuffer.find("ClientTime:")
        if(indexOfcTime == -1):
            break
        mybuffer = mybuffer[: indexOfcTime] + mybuffer[indexOfcTime+24:]

    #below removes Deli-1-meter
    while True:
        indexOfDeli = mybuffer.find("Deli-1-meter")
        if(indexOfDeli == -1):
            break
        mybuffer = mybuffer[:indexOfDeli] + mybuffer[indexOfDeli+12:]


    fileTCP.write(mybuffer)

    fileTCP.close()
    #print("file received")
    connectionSocket.close()


# two sockets are created for udp and tcp
serverUDPSocket = socket(AF_INET, SOCK_DGRAM)
serverTCPSocket = socket(AF_INET, SOCK_STREAM)


#created sockets are binded to appropriate ports
serverUDPSocket.bind((serverName, serverUDPPort))
serverTCPSocket.bind((serverName, serverTCPPort))

#This line has the server listen for TCP connection requests from the client.
#The parameter specifies the maximum number of queued connections (at least 1).
serverTCPSocket.listen(1)

#print("The server is ready to receive")





listenUDP(serverUDPSocket)

listenTCP(serverTCPSocket)

print("TCP Packets Average Transmission Time: " + str(totalTimeElapsedTransmittingTcp/receivedTcpPacketCounter) + " ms")
print("UDP Packets Average Transmission Time: " + str ( totalTimeElapsedTransmittingUdp/receivedUdpPacketCounter) + " ms")
print("TCP Communication Total Transmission Time: " + str(totalTimeElapsedTransmittingTcp) + " ms")
print("UDP Communication Total Transmission Time: " + str(totalTimeElapsedTransmittingUdp) + " ms")
print("UDP Transmission Re-transferred Packets: " + str(reTransmittedUdpPacketCounter))
