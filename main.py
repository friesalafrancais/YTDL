import PySimpleGUI as sg
import math
from pathlib import Path
from pytube import YouTube

# Text font + size
main_f = ('Comic Sans MS', 15)
main_fs = ('Comic Sans MS', 12)

# PySimpleGUI theme
sg.theme('DarkBlue17')


# Function that creates the main window and its layout
def main_window():
    layout = [[sg.Text("Enter URL:", font=('Comic Sans MS', 14))],
                    [sg.Input(key="-url-")],
                    [sg.Button('Query Video', font=main_fs), sg.Exit(font=main_fs)]]

    return sg.Window('YTDL', layout, icon=r'icon.ico', grab_anywhere=True)


# Calls the 'main_window' function
MainWindow = main_window()


# Used to round up the number from PyTube.length
def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier


# Main event loop
while True:
    event, values = MainWindow.Read()

    if event in (None, 'Exit'):
        MainWindow.close()
        break

    # If the user enters a URL and selects 'Query Video' the main window is closed and the 'videoqueryWindow' is opened
    elif event == 'Query Video':
        url = values["-url-"]

        my_video = YouTube(url)

        MainWindow.close()

        video_length = (my_video.length/60)

        videoqueryLayout = [[sg.Text("Title: ", font=main_f), sg.Text(my_video.title, font=main_f)],
                            [sg.Text("Length: ", font=main_f), sg.Text(round_up(video_length, 2), font=main_f), sg.Text("Minutes", font=main_f)],
                            [sg.Text("Author: ", font=main_f), sg.Text(my_video.author, font=main_f)],
                            [sg.Text("")],
                            [sg.Text("Download location:", font=main_f)],
                            [sg.Input(key="-location-"), sg.FolderBrowse(font=main_fs)],
                        [sg.Button('Download', font=main_fs, button_color=("white", "darkgreen")), sg.Exit(font=main_fs)]]

        videoqueryWindow = sg.Window('YTDL', videoqueryLayout, icon=r'icon.ico', grab_anywhere=True)

        event, values2 = videoqueryWindow.Read()

        keepRunning = True

        while keepRunning is True:

            # If the user selects 'Exit' the 'videoqueryWindow' is closed and the 'MainWindow' is opened.
            if event in (None, 'Exit'):
                videoqueryWindow.close()
                MainWindow = main_window()
                break

            # If the user selects 'Download' the video will download to the desired folder
            # If no download location is selected, defaults to users 'Downloads' folder
            if event == "Download":
                downloadLocation = values2["-location-"]

                print('Downloading video...')
                if not values2["-location-"]:
                    print("Download location not specified, defaulting to users 'Downloads' folder!")
                    downloadLocation = str(Path.home() / "Downloads")
                video = my_video.streams.get_highest_resolution()
                video.download(downloadLocation)

                print("Successfully downloaded!")

                # Setting 'keepRunning' to 'False' ends the loop
                # This closes 'videoqueryWindow' and opens 'MainWindow'
                keepRunning = False

        videoqueryWindow.Close()
        MainWindow = main_window()
