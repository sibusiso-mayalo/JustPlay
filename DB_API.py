import mysql.connector
class DB_API:
    #This class handles all the interactions with the databse

    def __init__(self):
        self.databaseComm = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="TSHEZI960222CHAMSHE7",
            database="JustPlayDB")
        self.cursor = self.databaseComm.cursor()

    def createTable(self):
        #Create all the table and the relationships between them

        createTableUser = "CREATE TABLE Users (UserID INTEGER AUTOINCREMENT PRIMARY KEY, IP VARCHAR(16), Name VARCHAR(50)"
        createTableSongs = "CREATE TABLE Songs (SongID INTEGER AUTOINCREMENT PRIMARY KEY, Name VARCHAR (200), Size VARCHAR(10), Genre VARCHAR (50), UserID INTEGER FOREIGN KEY )"

        self.cursor.execute(createTableUser)
        self.cursor.execute(createTableSongs)
        self.cursor.commit()

    def get_all_IPs(self):
        #select all the ip addresses on the database (online users)
        self.cursor.execute("SELECT IP from Users")

        onlineClients = []
        for client in self.cursor:
            onlineClients.append(client)
        return onlineClients

    def get_playlist(self, genre):
        #get all the songs that are/(some)were queued to played based on the genre
        self.cursor.execute("SELECT Name FROM Playlist WHERE Genre LIKE '" + genre + "'")

        playlist = []
        for song in self.cursor:
            playlist.append(song)
        print("Playlst : ",playlist)
        return playlist

    def get_all_genres(self):
        self.cursor.execute("SELECT Name FROM Genres")

        genres = list()
        for genre in self.cursor:
            genres.append(genre)
        return genres

    def insert_new_user(self, ip, name):
        self.cursor.execute("INSERT INTO Users (Name,IP) VALUES " + (name,ip))
        self.cursor.commit()

    def queue_song(self, name, size, genre, userID, file):
        # insert into songs
        self.cursor.execute("INSERT INTO Songs (SongID, Name, Size, Genre, UserID, File) VALUES " + (name,size,genre, userID, file) )
        self.cursor.commit()

