from main import *
import os


def user_menu_sanitisation(prompt: str, maximum_input: int):
    while True:
        u_input = input(prompt)
        try:
            u_input = int(u_input)
            if u_input >= 1 and u_input <= maximum_input:
                return f'{u_input}'
        except:
            print(f"try again. The input wasn't an allowed number.\n it should be in between 1 and {maximum_input}")


def download_one_video():
    saving_directory = directory_sanitization("enter where you want the video downloaded")
    url = youtube_url_sanitization('Enter the youtube URL')
    download_video(video_url=url, output_path=saving_directory)


def download_multiple_video_by_url():
    saving_directory = directory_sanitization("Enter the path to save content: ")
    url_to_download = []
    adding_link = True
    while adding_link:
        url = youtube_url_sanitization('Enter the youtube URL to download: ')
        if url == 'quit':
            adding_link = False
            continue
        url_to_download.append(url)
    print('Starting the downloads')
    downloaded_video = []
    for e in url_to_download:
        video_link = download_video(e, saving_directory)
        if video_link == "all ready Downloaded":
            continue
        downloaded_video.append(video_link)

    return downloaded_video, saving_directory


def download_multiple_video_by_file():
    return download_video_from_file(input('Enter text file path: '),directory_sanitization('Enter the download path'))


def download_playlist_video():
    playlist_download(input('Enter the link to the playlist: '),directory_sanitization('Enter where to download the playlist: '))


def download_one_music():
    saving_directory = directory_sanitization("enter where you want the music downloaded")
    url = youtube_url_sanitization('Enter the youtube URL')
    download_and_convert_to_mp3(video_url=url, output_path=saving_directory)


def download_multiple_music(del_mp4: bool = True):
    music_path, output_path = download_multiple_video_by_url()
    for e in music_path:
        convert_video_to_mp3(e, output_path)
        if del_mp4:
            os.remove(e)


def download_multiple_music_by_file():
    output_path, video_path = download_multiple_video_by_file()
    for e in video_path:
        convert_video_to_mp3(e, output_path)
        os.remove(e)


def download_playlist_music():
    output_path, video_path = download_playlist_video()
    for e in video_path:
        convert_video_to_mp3(e, output_path)
        os.remove(e)


def main_menu():
    menu = {
        "1": ["\033[92mdownload a \033[91myoutube\033[92m video\033[0m", download_one_video],
        "2": ["\033[92mdownload multiple \033[91myoutube\033[92m videos\033[0m", download_multiple_video_by_url, '\033[94m'],
        "3": ["\033[92mdownload \033[91myoutube\033[92m videos from file\033[0m", download_multiple_video_by_file, '\033[94m'],
        "4": ["\033[92mdownload youtube videos from \033[92myoutube\033[92m playlist\033[0m", download_playlist_video, '\033[94m'],
        "5": ["\033[94mdownload a music on \033[91myoutube\033[0m", download_one_music],
        "6": ["\033[94mdownload multiple music on \033[91myoutube\033[0m", download_multiple_music, '\033[94m'],
        "7": ["\033[94mdownload music on \033[91myoutube\033[94m from file\033[0m", download_multiple_music_by_file, '\033[94m'],
        "8": ["\033[94mdownload musics from \033[91myoutube\033[0m \033[94mplaylist\033[0m", download_playlist_music],
        "9": ["\033[91mquit\033[0m", quit]
    }
    menu_maximum_number = len(menu)
    while True:
        for e in menu:
            print(f'{e}: {menu[e][0]}')
        menu[user_menu_sanitisation(f"enter a number in between 1 and {menu_maximum_number}: ", menu_maximum_number)][1]()
