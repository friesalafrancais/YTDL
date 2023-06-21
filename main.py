import PySimpleGUI as sg
from pathlib import Path
from pytube import YouTube

# Text font + size
main_f = ('Comic Sans MS', 15)
main_fs = ('Comic Sans MS', 12)

# PySimpleGUI theme
sg.theme('DarkBlue17')


# Function that creates the main window and its layout
def main_window():
    layout = [[sg.Text('Enter URL:', font=('Comic Sans MS', 14))],
              [sg.Input(key='-url-')],
              [sg.Button('Query Video', font=main_fs), sg.Exit(font=main_fs)]]

    return sg.Window('YTDL', layout, icon=r'icon.ico', grab_anywhere=True)


# Function that creates the video query window and its layout
def videoquery_window():
    layout = [[sg.Text('Title: ', font=main_f), sg.Text(my_video.title, font=main_f)],
              [sg.Text('Length: ', font=main_f), sg.Text(formatted_length, font=main_f)],
              [sg.Text('Author: ', font=main_f), sg.Text(my_video.author, font=main_f)],
              [sg.Text('')],
              [sg.Text('Download location:', font=main_f)],
              [sg.Input(key='-location-'), sg.FolderBrowse(font=main_fs)],
              [sg.Button('Download Video', font=main_fs, button_color=('white', '#cc2b2b')),
               sg.Button('Download Audio', font=main_fs, button_color=('White', '#349beb')),
               sg.Exit(font=main_fs)]]

    return sg.Window('YTDL', layout, icon=r'icon.ico', grab_anywhere=True)


# Used to convert the output of '.length' to a more readable Hours:Minutes:Seconds
def convert_video_length(length):
    hours, remainder = divmod(length, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


# Calls the 'main_window' function
MainWindow = main_window()

# Main event loop
while True:
    event, values = MainWindow.Read()

    # If the user clicks on the 'Exit' button, 'MainWindow closes, program breaks
    if event in (None, 'Exit'):
        MainWindow.close()
        break

    # If the user enters a URL and selects 'Query Video' the main window is closed and the 'videoqueryWindow' is opened
    elif event == 'Query Video':
        url = values['-url-']

        my_video = YouTube(url)

        formatted_length = convert_video_length(my_video.length)

        MainWindow.close()

        videoqueryWindow = videoquery_window()

        event, values2 = videoqueryWindow.Read()

        keepRunning = True

        while keepRunning is True:

            # If the user selects 'Exit' the 'videoqueryWindow' is closed and the 'MainWindow' is opened.
            if event in (None, 'Exit'):
                videoqueryWindow.close()
                MainWindow = main_window()
                break

            # If the user selects 'Download Video' the video will download to the desired folder
            # If no download location is selected, defaults to users 'Downloads' folder
            if event == 'Download Video':
                downloadLocation = values2['-location-']

                print('Downloading video...')

                if not values2['-location-']:
                    print('Download location not specified, defaulting to users "Downloads" folder!')
                    downloadLocation = str(Path.home() / 'Downloads')

                video = my_video.streams.get_highest_resolution()
                video.download(downloadLocation)

                print('Successfully downloaded!')

                # Setting 'keepRunning' to 'False' ends the while loop
                # This closes 'videoqueryWindow' and opens 'MainWindow'
                keepRunning = False

            # If the user selects 'Download Audio' the audio file will download to the desired folder
            # If no download location is selected, defaults to users 'Downloads' folder
            if event == 'Download Audio':
                downloadLocation = values2['-location-']

                print('Downloading audio...')

                audio_stream = my_video.streams.filter(only_audio=True).first()

                if not values2['-location-']:
                    print('Download location not specified, defaulting to users "Downloads" folder!')
                    downloadLocation = str(Path.home() / 'Downloads')

                audio_stream.download(output_path=downloadLocation)

                print('Successfully downloaded!')

                # Setting 'keepRunning' to 'False' ends the while loop
                # This closes 'videoqueryWindow' and opens 'MainWindow'
                keepRunning = False

        videoqueryWindow.Close()
        MainWindow = main_window()
