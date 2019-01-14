import Tkinter as tk
import tkFileDialog
import sys
import ttk as ttk
from Client import *

class UserInterface:

    def __init__(self):
        self.clientObject = Client("127.0.0.1",2000)

    def select_new_song(self, event):
        filePath = tkFileDialog.askopenfilename(title = 'Select a file',filetypes=[('AVI','*.avi'), ('MP3','*.mp3'),('mp4','*.mp4')])
        self.addToList( filePath[filePath.rfind("/")+1:]  ) #song name
        self.clientObject.sendFileToServer(filePath, self.genreComb.get(), 1)

    def addToList(self,fileName):
        #Add the name of the song (s) to the list widget
        if type(fileName) is list:
            self.songsList.insert(tk.END, (item for item in fileName))
        else:
            self.songsList.insert(tk.END,fileName)

    def changePlayList(self, event):
        #Populate playlist widget based on the selected genre
        new_playlist = self.clientObject.get_playlist( self.genreComb.get())

        if not new_playlist:
            self.songsList.delete(0, tk.END)
            self.songsList.insert(tk.END, (song for song in new_playlist))

    def make_components(self):
        window = tk.Tk()

        #Add title, default geometry and background color
        window.title("Just Play")
        window.geometry("980x500")

        #Labels
        welcomeLable = tk.Label(text="Welcome to Just Play v1.0", font=('Helvetica',30,'bold'))
        welcomeLable.grid(row=0, column=0, columnspan=2)

        #Video display widget - to display the video that is playing
        videoDisplay = tk.Canvas(window, height=400, width=700, bg='black')
        videoDisplay.grid(column=0, row=1)

        #Listbox widget - to display the songs in the queue
        self.songsList = tk.Listbox(window, width=30, height=23, selectbackground='grey')
        self.songsList.grid(column=1, row=1)

        #This frame is used to fit multiple buttone in one grid cell
        frameButton = tk.Frame(window)

        #ComboBox widget - to display all the available genres
        self.genreComb = ttk.Combobox(frameButton)
        self.genreComb['values'] = self.clientObject.get_all_genres()
        self.genreComb.grid(column=0, row=0)
        self.genreComb.bind("<<ComboboxSelected>>", self.changePlayList)

        #Buttons - Add a song to the queue and also exit the application
        addSongButton = tk.Button(frameButton, text="Add song")
        addSongButton.bind("<Button-1>", self.select_new_song)
        addSongButton.grid(column=1, row=0)

        exitButton = tk.Button(frameButton, text="Close")
        exitButton.bind("<Button-1>", self.close_app)
        exitButton.grid(column=2, row=0)

        #display the frame with buttons to the user interface
        frameButton.grid(column=0, row=2)
        window.mainloop()

    def close_app(self, event):
        sys.exit()

def main():
    inter = UserInterface()
    inter.make_components()

if __name__ == '__main__':
    main()
