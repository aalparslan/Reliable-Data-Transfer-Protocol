# Reliable-Data-Transfer-Protocol

In this study, communication of two nodes using socket programming is performed. In this assignment a file is sent to any receiver that is running the server.py. Python is used as the programming language. Firstly, using UDP a file named "transfer_file_UDP.txt" is sent from the client to the server. After a timeout interval, using TCP a file named "transfer_file_TCP.txt" is sent from the client to the server. Both of these files need to be at the same directory with the client.py. Since, client reads from the file whose name is as same as the file that server writes to, client.py and server.py should be in different directories if they run on the same computer. 

 A reliable data transfer protocol is implemented on the top of the unreliable UDP protocol. This RDT is has similarities with go-back-n protocol. This RDT is designed simply based on the idea that there is only one segment on the fly at a time.  

Time stamps are sent with data to measure the time on the fly. As soon as the data sent from the client, time is measured and sent with the data and as soon as the server receives the data, time measured in the server too. Time in the both ends synchronized by binding them to the same NTP server.  

Command below is used:  

-sudo ntpdate pool.ntp.org  


ortak.py is the file that is used to calculate checksum on the both ends. Therefore, it needs to be present on both sides.  

 
In the beginning, a way to test RDT or to measure time was needed therefore, sending data via UDP and TCP is implemented without any time measurement or any RDT protocol.  
After sending the first data using TCP and UDP with at most ten lines of code, development path was more obvious. At that time, things that needs to be developed were listed as following: 

 

- Figuring out how simulator works  
- Setting up the environment for reading files and writing to files 
- RDT protocol for sending data reliably 
- Time synchronization 
- Time measurement on both sides 
- parsing the data and the time on the receiving side 

 

Major problems faced as following:  

- When the ACKs are coming from the server if they lost or corrupted, data from the client needs to be retransmitted. Therefore, a timeout value is needed. However, if the delay that is given as the output to the simulator is also affected from this timeout. If the delay is much more than the timeout value that is set to retransmit data, client keeps time outing every time a delayed segment transmitted. One is on the simulator and since the client is timeout another one that is same as the one on the fly is retransmitted. In such a case there are two exact segments on the fly. The first one is accepted by the server and ACKed and the other one is negatively ACKed. By the design of this implementation, client needs to timeout to pass the second phase which is accepting TCP segments and therefore a timeout value is needed. If this value is set so that no delay value can be more than the timeout value, client would not time out and second phase would not start. Therefore, a limit for delay is needed and it is for this implementation at most 8 seconds. If a delay value that is more than 8 seconds is given, in the client and server codes timeout values needs to be increased. 

 
- While sending data using UDP the computer running server.py using python3.x version and client was using python3.x version and these versions has a different way of encoding and decoding bases. Due to this difference, encoding and decoding was very problematic. To avoid this issue server.py and client.py needs to be run using python3 only. 

 
- Calculating time was also an issue in TCP. Since TCP is a connection-oriented protocol, its ".recv" function only returns the data when its buffer is full. If it's not full data waits in there. Therefore, time measurement was error-prone.  

 
- When data transmission via UDP is finished, client starts sending via TCP. However, server needs to timeout. If does not timeout, client sends the data too early that is to say while TCP connection was not listening by server. 

 
- Sometimes simulator corrupts the data in a way that that is not decoded by the sender. At these times, servers throw a UnicodeDecodeErrorr. 

  

After the study, followings aspects of data transmission are learnt: 

  
- By implementing a RDT on the top of the UDP, reliable and fast data transmission can be achieved.  
- By using NTP servers two computers can be synchronized timewise. 
- To send the data to the network it needs to be encoded by some base and decoded back on the other end by the same base. 
- TCP sockets in python3 are blocking sockets but can be turned in to nonblocking sockets. 

  
 

Completing the assignment took four days  

 

 

 
