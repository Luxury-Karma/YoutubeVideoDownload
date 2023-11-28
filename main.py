import os
import subprocess

from pytube import YouTube
from pytube import Playlist
from moviepy.video.io.VideoFileClip import VideoFileClip
import sys
import argparse
import re



def on_progress(stream, chunk, remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - remaining

    # Calculate percentage completion
    progress = (bytes_downloaded / total_size) * 100

    # Print the progress
    print(f"\rDownloading: {progress:.2f}% complete", end='')


def download_video(video_url, output_path) -> str:
    yt = YouTube(video_url, on_progress_callback=on_progress)
    print(f'\nThe video {yt.title} start is download\n')
    if not os.path.isfile(f'{output_path}\\{yt.title}.mp3') or not os.path.isfile(f'{output_path}\\{yt.title}.mp3'):
        video_file_path = yt.streams.filter(progressive=True, file_extension='mp4').desc().get_highest_resolution().download(output_path)
        return video_file_path
    print("This download was all ready in the directory.")
    return "all ready Downloaded"


def download_and_convert_to_mp3(video_url, output_path, del_mp4=True):
    try:
        video_file_path = download_video(video_url, output_path)
        if video_file_path == "all ready Downloaded":
            return
        print('downloaded videos\nStarting conversion to music')
        convert_video_to_mp3(video_file_path, output_path)

        print("\nConversion completed successfully.")
        if del_mp4:
            os.remove(video_file_path)
    except Exception as e:
        print(f"An error occurred: {e}")


def convert_video_to_mp3(input_file, output_path):
    video = VideoFileClip(input_file)
    video_title: str = video.filename
    video_title = video_title.split('\\')[-1]
    video_title = video_title.strip('.mp4')
    output_file = os.path.join(output_path, f"{video_title}.mp3")
    video.audio.write_audiofile(output_file)
    video.close()


def argument_handler():
    parser = argparse.ArgumentParser(description='A youtube downloader script')
    parser.add_argument('-u', '--url', help='Url to the video you want to download on youtube',  type=str)
    parser.add_argument('-mp', '--mp34', help='Output file path', type=str, default='mp4', required='-u' in sys.argv)
    parser.add_argument('-o', '--output', help='path to the output file', type=str, default=os.getcwd(), required='-u' in sys.argv)
    parser.add_argument('-p', '--program', help='run as it was a program with a menu', type=str, default=True)

    return parser.parse_args()


def directory_sanitization(prompt: str):
    while True:
        input_path = input(prompt)
        if os.path.exists(input_path) and os.path.isdir(input_path):
            return os.path.abspath(input_path)
        else:
            # Raise a ValueError if the path is not a valid directory
            raise ValueError(f"{input_path} is not a valid existing directory.")


def youtube_url_sanitization(prompt: str):
    # Define a regular expression pattern for YouTube video URLs
    youtube_url_pattern = re.compile(
        r"^(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})"
    )

    while True:
        input_url = input(prompt)
        # Check if the input URL matches the YouTube URL pattern
        match = youtube_url_pattern.match(input_url)
        if input_url.lower() == 'quit' or input_url.lower() == 'q':
            return 'quit'
        if match:
            # Return the sanitized URL
            return "https://www.youtube.com/watch?v=" + match.group(6)
        else:
            # Raise a ValueError if the input is not a valid YouTube video URL
            raise ValueError(f"{input_url} is not a valid YouTube video URL.")


def download_one_video():
    saving_directory = directory_sanitization("enter where you want the video downloaded")
    url = youtube_url_sanitization('Enter the youtube URL')
    download_video(video_url=url, output_path=saving_directory)


def download_one_music():
    saving_directory = directory_sanitization("enter where you want the music downloaded")
    url = youtube_url_sanitization('Enter the youtube URL')
    download_and_convert_to_mp3(video_url=url,output_path=saving_directory)


def download_multiple_video_by_file():
    file_path = input('Enter text file path: ')
    file_data = ''
    with open(file_path, 'r') as f:
        file_data = f.read()
    file_data = file_data.split('\n')
    file_data = [line.strip() for line in file_data if line.strip()]
    download_path = directory_sanitization('Where to download the content?: ')
    downloaded_video = []
    for e in file_data:
        video_path = download_video(video_url=e, output_path=download_path)
        if video_path == "all ready Downloaded":
            continue
        downloaded_video.append(video_path)

    return download_path, downloaded_video

def download_multiple_music_by_file():
    output_path, video_path = download_multiple_video_by_file()
    for e in video_path:
        convert_video_to_mp3(e, output_path)
        os.remove(e)

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


def download_multiple_music(del_mp4: bool = True):
    music_path, output_path = download_multiple_video_by_url()
    for e in music_path:
        convert_video_to_mp3(e, output_path)
        if del_mp4:
            os.remove(e)




def user_menu_sanitisation(prompt:str, maximum_input:int):
    while True:
        u_input = input(prompt)
        try:
            u_input = int(u_input)
            if u_input >= 1 and u_input <= maximum_input:
                return f'{u_input}'
        except:
            print(f"try again. The input wasn't an allowed number.\n it should be in between 1 and {maximum_input}")

def download_playlist_video():
    playlist_url = input('Enter the link to the playlist: ')
    playlist = Playlist(playlist_url)
    download_path = directory_sanitization('Enter where to download the playlist: ')
    video_downloaded = []
    for video in playlist.video_urls:
        video_path = download_video(video, download_path)
        if video_path == "all ready Downloaded":
            continue
        video_downloaded.append(video_path)
    return download_path, video_downloaded

def download_playlist_music():
    output_path, video_path = download_playlist_video()
    for e in video_path:
        convert_video_to_mp3(e, output_path)
        os.remove(e)




def main_menue():
    menu = {
        "1": ["\033[92mdownload a video\033[0m", download_one_video],
        "2": ["\033[92mdownload multiple videos\033[0m", download_multiple_video_by_url, '\033[94m'],
        "3": ["\033[92mdownload videos from file\033[0m", download_multiple_video_by_file, '\033[94m'],
        "4": ["\033[92mdownload videos from youtube playlist\033[0m", download_playlist_video, '\033[94m'],
        "5": ["\033[94mdownload a music\033[0m", download_one_music],
        "6": ["\033[94mdownload multiple music\033[0m", download_multiple_music, '\033[94m'],
        "7": ["\033[94mdownload music from file\033[0m", download_multiple_music_by_file, '\033[94m'],
        "8": ["\033[94mdownload musics from youtube playlist\033[0m", download_playlist_music],
        "9": ["\033[91mquit\033[0m", quit]
    }
    menu_maximum_number = len(menu)
    while True:
        for e in menu:
            print(f'{e}: {menu[e][0]}')
        menu[user_menu_sanitisation(f"enter a number in between 1 and {menu_maximum_number}: ", menu_maximum_number)][1]()


if __name__ == "__main__":
    args = argument_handler()
    if args.url:
        if args.mp34 == 'mp4':
            download_video(args.url, args.output)
        if args.mp34 == 'mp3':
            download_and_convert_to_mp3(args.url, args.output)
    elif args.program:
        main_menue()

