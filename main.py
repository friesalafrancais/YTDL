import PySimpleGUI as sg
import math
from pathlib import Path
from pytube import YouTube

# Text font + size
main_f = ('Comic Sans MS', 15)
main_fs = ('Comic Sans MS', 12)

# PySimpleGUI theme
sg.theme('DarkBlue17')

# Creates the main window layout with some basic device info
mainWindowlayout = [[sg.Text("Enter URL:", font=('Comic Sans MS', 14))],
                    [sg.Input(key="-url-")],
                    [sg.Button('Query Video', font=main_fs), sg.Exit(font=main_fs)]]

MainWindow = sg.Window('YTDL', mainWindowlayout, icon=r'icon.ico', grab_anywhere=True)


def main_window():
    layout = [[sg.Text("Enter URL:", font=('Comic Sans MS', 14))],
                    [sg.Input(key="-url-")],
                    [sg.Button('Query Video', font=main_fs), sg.Exit(font=main_fs)]]

    return sg.Window('YTDL', layout, icon=r'icon.ico', grab_anywhere=True)

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

while True:
    event, values = MainWindow.Read()

    if event in (None, 'Exit'):
        MainWindow.close()
        break

    elif event == 'Query Video':
        url = values["-url-"]

        my_video = YouTube(url)

        MainWindow.close()

        video_length = (my_video.length/60)

        videoqueryLayout = [[sg.Text("Title: " + my_video.title, font=main_f)],
                            [sg.Text("Length: ", font=main_f), sg.Text(round_up(video_length, 2), font=main_f), sg.Text("Minutes", font=main_f)],
                            [sg.Text("Author: " + my_video.author, font=main_f)],
                            [sg.Text("Download location:")],
                            [sg.Input(key="-location-"), sg.FolderBrowse()],
                        [sg.Button('Download', font=main_fs, button_color=("white", "darkgreen")), sg.Exit(font=main_fs)]]

        videoqueryWindow = sg.Window('YTDL', videoqueryLayout, icon=r'icon.ico', grab_anywhere=True)

        event, values2 = videoqueryWindow.Read()

        keepRunning = True

        while keepRunning is True:

            if event in (None, 'Exit'):
                videoqueryWindow.close()
                MainWindow = main_window()
                break

            if event == "Download":
                downloadLocation = values2["-location-"]

                print('Downloading video...')
                if not values2["-location-"]:
                    print("User did not specify a download location, defaulting to users Downloads folder!")
                    downloadLocation = str(Path.home() / "Downloads")
                video = my_video.streams.get_highest_resolution()
                video.download(downloadLocation)

                print("Successfully downloaded!")

                keepRunning = False

        videoqueryWindow.Close()
        MainWindow = main_window()
