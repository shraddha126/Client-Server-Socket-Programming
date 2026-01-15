 
"""
NUID:002301041
Secret flag: 0dfd2a5fc714afadb63a6e19be2a3700e77b9c418262943770bb4281a1fc66bf

Client Program for Solving Arithmetic Problems through College Lab Remote Server 

This program is designed in such a way that, it connects to a remote server located in the college labs to solve arithmetic problems. 
To access the server, we need to connect our laptop to the college's VPN. Once connected, the server will send math problems, and the 
client program will calculate the answersand send them back to the server. The program continues until the server says the task is complete 
or there is an error.

Steps of how the Program works:
1. Connecting to the Server: 
   a. In the First step, the client connects to the college's VPN to access the server in the lab. 
   b. After establishing the connection, the program uses the server's IP address and port number to make a network 
      connection through TCP.
   c. If the connection fails (for example, if the VPN is not connected or the server is down), the program will stop with an 
      error message.

2. Sending an Introductory Message: 
   a. Once connected, the client sends a message to introduce itself to the server, using the NUID for identification. 
      This lets the server know who is trying to connect.

3. Receiving and Solving Math Problems: 
   a. The server sends a math problem, like "3 + 4" or "5 * 6", and the client extracts the expression from the message.
   b. The client calculates the result using Pythons built-in evaluation function (eval) and sends the answer back to the server.

4. Checking for Success or Failure: 
   a. After sending the answer, the server will respond:
     - If the answer is correct, the server sends a success message along with a "secret flag" (a special code).
     - The client prints the success message and secret flag and then stops running.
     - If the answer is incorrect or something else goes wrong, the server sends a failure message, and the client stops 
       running.

5. Handling Errors: 
     If there are any problems while communicating with the server (such as the server not responding), 
     the program stops and shows an error message so that the user knows what went wrong.

6. Closing the Connection: 
     After all tasks are complete, the program closes the connection to the server and stops. This is necessary to make 
     sure the connection is properly terminated.

"""

import socket
import sys

#Configuring the server
serverhostname="10.188.57.42"  #IP address of the server
serverport=5220  #Port number
buffersize=4096  #Buffer size=4KB
nuid="002301041"  #NUID

clientsocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create and connect client socket  
try:
    #Connected to the server using hostname and port
    clientsocket.connect((serverhostname, serverport))
    print(f"Connected to server at {serverhostname}:{serverport}")
except Exception as e:
    #If the connection fails:
    print(f"Failed to connect to server: {e}")
    sys.exit(1)

intro_msg=f"EECE7374 INTR {nuid}"      # Sending introductory message
try:
    clientsocket.send(intro_msg.encode('utf-8'))
    print(f"Sent: {intro_msg}")
except Exception as e:
    #If sending fails then end the program
    print(f"Failed to send introductory message: {e}")
    sys.exit(1)

#To receive and reply to messages from the server
while True:
    try:
        #The message recieved from the server is decoded and printed
        server_message=clientsocket.recv(buffersize).decode('utf-8')
        print(f"Received: {server_message}")
 
        if server_message.startswith("EECE7374 EXPR"):    #Server sends an expression to evaluate
            expression=server_message.split(' ', 2)[2]    #Extracting expression from the message
            result=eval(expression)                       #Solving the expression

            #Sending result to the server
            result_message=f"EECE7374 RSLT {result}"
            clientsocket.send(result_message.encode('utf-8'))
            print(f"Sent: {result_message}")

        #If there is success from server side-
        elif server_message.startswith("EECE7374 SUCC"):
            print("Success! Received secret flag:", server_message.split()[2])   # Print success message and the secret flag from the server
            break  #Exit loop if there is a success

        #If there is failure from server side-
        elif server_message.startswith("EECE7374 FAIL"):
            print("Failed! Incorrect result or protocol error.")
            break  #Exit the loop if there is a failure

    except Exception as e:
        print(f"Error during communication: {e}")        #To handle any communication errors during message receiving or sending
        break

#Close the socket after the communication ends
clientsocket.close()
