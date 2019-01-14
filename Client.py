import socket
import sys
from MessagesEnums import *
import pickle
import os

class Client:

    def __init__(self, serverIP, serverPort):
        try:
            self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.clientSocket.connect((serverIP, serverPort))
        except IOError as err:
            print("Setup error ", err)

    def sendFileToServer(self, filePath, genre, userID):
        try:
            details = (filePath, genre, userID)
            details = pickle.dumps(details)
            self.clientSocket.send(MessagesEnums.request_messages[3] + str(len(details)))
            self.clientSocket.send(details)

            messageType = self.receiveMessage(4096)
            print("Response from the server : ", messageType[7:])

        except IOError as error:
            print("Playlist request error : ", error)

    def get_all_genres(self):
        self.clientSocket.send( pickle.dump(MessagesEnums.request_messages[1]))
        messageType  = self.receiveMessage(1024)

        if messageType[:7] == MessagesEnums.response_messages[1]:
            genres = self.receiveMessage(int(messageType[7:]))
            return genres

    def get_playlist(self, genreName):
        pickle.d
        request = pickle.dumps(MessagesEnums.request_messages[0] + str(len(genreName)))
        self.clientSocket.send(request)
        self.clientSocket.send(pickle.dumps(genreName))
        messageType = self.receiveMessage(1024)

        if messageType[:7] == MessagesEnums.response_messages[0]: # check if the server response is the requested playlist
            playlist = self.receiveMessage(int(messageType[7:]))
            print("Playlist received " + playlist)
            return playlist

    def receiveMessage(self, size):
        #Receive continuous stream of data
        message = self.clientSocket.recv(size)
        message = pickle.loads(message)
        return message


    def close_connection(self):
        #close connection to the server
        self.clientSocket.send(MessagesEnums.request_messages[4])
        self.clientSocket.close()
        sys.exit()
        print("Closed connection.")
