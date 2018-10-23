for this lab, i was tasked to create a simple client server file transfer
system using TCP

with this program the user will be able to send any type of file over a
network using TCP connection

the program will be able to handle situations such as:
    -zero length files
    -files that do not exist
    -the file already exists on the server
    -work with and without the stammerProxy

to use the program:
   1st. run the server program located at
   	file-transfer-lab/Server/fileServer.py.
   2nd. run the client program located and
   	file-transfer-lab/Client/fileClient.py.
   3rd. in the fileClient.py program, you will be prompted to enter the name
   	of the file you wish to send to the server.

	-if the file is not empty, the file will be successfully transfered to
   	 the server if it does not already exist in the server. Then you will
   	 be prompted to enter the name of a different file if you wish to send
   	 one

   4th. to exit the program, type "exit" w/o quotes when asked to enter the
   name of the file. 
   
