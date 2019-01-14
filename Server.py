import os
from socket import *
import threading
from MessagesEnums import *
from DB_API import *
import pickle

class Server:

    def __init__(self):
        #Bind socket
        self.serverSock = socket(AF_INET, SOCK_STREAM)
        self.serverSock.bind(("127.0.0.1", 2000))
        self.serverSock.listen(5)
        self.onlineClients = dict() #This should/can be a map but in the meantime a dict will do

        self.dbBhandler = DB_API()
        print ("Setup finished.")

    def listen_for_connections(self):
        #listen for incoming requests
        print("Listening for connections..")
        while True:
            client, address = self.serverSock.accept()

            if self.onlineClients.get(client) == None:
                self.onlineClients[client] = address
                print ("New connection ", address)

            #Thread that will handle incoming messages
            messageThread = threading.Thread(target = self.handle_client_messages,args=('handle_client_messages',client))
            messageThread.start()

    def handle_client_messages(self, name, clientSockt):

        message = self.receiveMessage(clientSockt, 4096)

        if message[:7] == MessagesEnums.request_messages[0]:
            #Get playlist from the databse and send it to the client
            recvSize = int(message[7:])
            genreName = self.receiveMessage(clientSockt, recvSize)

            playlist = pickle.dumps(self.dbBhandler.get_playlist(genreName)) #get playlist from the db
            clientSockt.send(MessagesEnums.response_messages[0] + str(len(playlist)))
            clientSockt.send(playlist)

        elif message[:7] == MessagesEnums.request_messages[1]:
            #Get all genres from the database

            genres = self.dbBhandler.get_all_genres()
            genres = pickle.dumps(genres)
            clientSockt.send(MessagesEnums.response_messages[1] + str(len(genres)))
            clientSockt.send(genres)

        elif message[:7] == MessagesEnums.request_messages[2]:
            print()

        elif message[:7] == MessagesEnums.request_messages[3]:
            data = self.receiveMessage(clientSockt, int(message[7:]))

            filePath = data[0]
            genre = data[1]
            userID = data[2]
            fileSize = os.path.getsize(filePath)
            fileName = filePath[filePath.rfind("/")+1:]

            binary_file = self.get_file(filePath)
            if not (file == None):
                #Now send file to the database.  after that
                self.dbBhandler.queue_song(fileName, fileSize, genre, userID, binary_file)
                #send response to client
                clientSockt.send( MessagesEnums.response_messages[3] + " File received.")

        elif message[:7] == MessagesEnums.request_messages[4]:
            self.remove_client(clientSockt) #Remove client from online clients, closed connection

        else:
            clientSockt.send( MessagesEnums.response_messages[4] + " Uknonwn request.")

    def receiveMessage(self, clientSocket, size):
        messageStream = clientSocket.recv(size)
        messageStream = pickle.loads(messageStream)
        return messageStream

    def close_server(self):
        self.serverSock.close()
        print("Server closed.")

    def get_file(self, filename):
        try:
            if os.path.isfile(filename):
                fileSize = os.path.getsize(filename)
                redFile = ""

                #download the file
                with open(filename, 'rb') as fileBits: #read binary
                    redFile = fileBits.read()

                    while fileSize != len(redFile):
                        redFile += fileBits.read()
                return redFile
            else:
                print("The file is not found.")
                return None
        except IOError as e:
            print("Error : ", e)
            return None

    def remove_client(self, client):
        self.onlineClients.remove(client)
        print("Removed client:", client)

def main():
    server = Server()
    server.listen_for_connections()

if __name__ == '__main__':
    main()
