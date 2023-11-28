import os
import subprocess

from pytube import YouTube
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
    # Create a YouTube object
    yt = YouTube(video_url, on_progress_callback=on_progress)

    # Get the highest resolution stream with both video and audio
    video_file_path = yt.streams.filter(progressive=True, file_extension='mp4').desc().get_highest_resolution().download(output_path)

    return video_file_path


def download_and_convert_to_mp3(video_url, output_path, del_mp4=True):
    try:
        video_file_path = download_video(video_url, output_path)
        print('downloaded videos\nStarting conversion to music')
        convert_video_to_mp3(video_file_path, output_path)

        print("\nConversion completed successfully.")
        if del_mp4:
            os.remove(video_file_path)
    except Exception as e:
        print(f"An error occurred: {e}")


def convert_video_to_mp3(input_file, output_path):
    video = VideoFileClip(input_file)
    video_title:str = video.filename
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


def download_multiple_video():
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
        downloaded_video.append(download_video(e, saving_directory))
    return downloaded_video, saving_directory


def download_multiple_music(del_mp4: bool = True):
    music_path, output_path = download_multiple_video()
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


def main_menue():
    menu = {
        "1": ["download a video", download_one_video],
        "2": ["download a music", download_one_music],
        "3": ["download multiple videos", download_multiple_video],
        "4": ["download multiple music", download_multiple_music]
    }
    menu_maximum_number = len(menu)
    for e in menu:
        print(f'{e}: {menu[e][0]}')

    menu[user_menu_sanitisation(f"enter a number in between 1 and {menu_maximum_number}", menu_maximum_number)][1]()


if __name__ == "__main__":
    args = argument_handler()
    if args.url:
        if args.mp34 == 'mp4':
            download_video(args.url, args.output)
        if args.mp34 == 'mp3':
            download_and_convert_to_mp3(args.url, args.output)
    elif args.program:
        main_menue()

