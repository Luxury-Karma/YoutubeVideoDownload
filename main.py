import argparse
import re
import sys

from moviepy.video.io.VideoFileClip import VideoFileClip

from cli_interaction import *
from pytube import YouTube
from pytube import Playlist


def on_progress(stream, chunk, remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - remaining

    # Calculate percentage completion
    progress = (bytes_downloaded / total_size) * 100

    # Print the progress
    print(f"\rDownloading: {progress:.2f}% complete", end='')


def download_video(video_url, output_path) -> str:
    try:
        yt = YouTube(video_url, on_progress_callback=on_progress)
        print(f'\nThe video {yt.title} start is download\n')
        if not os.path.isfile(f'{output_path}\\{yt.title}.mp3') or not os.path.isfile(f'{output_path}\\{yt.title}.mp3'):
            video_file_path = yt.streams.filter(progressive=True,
                                                file_extension='mp4').desc().get_highest_resolution().download(
                output_path)
            return video_file_path
        print("This download was all ready in the directory.")
        return "all ready Downloaded"
    except:
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
        print(f"An error occurred: \033[91m{e}\033[0m")


def playlist_download(playlist_url: str, download_path: str):
    try:
        playlist = Playlist(playlist_url)
    except Exception as e:
        print(f'Playlist link error.\n \033[91mERROR:{e}\033[0m')
        return
    video_downloaded = []

    total_video_amount = len(playlist.video_urls)
    total_video_downloaded = 0

    for video in playlist.video_urls:
        print(f'\033[93mDownload complete: {total_video_downloaded}/{total_video_amount}\033[0m')
        video_path = download_video(video, download_path)
        if video_path == "all ready Downloaded":
            total_video_downloaded = total_video_downloaded + 1
            continue
        video_downloaded.append(video_path)
        total_video_downloaded = total_video_downloaded + 1
    return download_path, video_downloaded


def convert_video_to_mp3(input_file, output_path):
    try:
        video = VideoFileClip(input_file)
        video_title: str = video.filename
        video_title = video_title.split('\\')[-1]
        video_title = video_title.strip('.mp4')
        output_file = os.path.join(output_path, f"{video_title}.mp3")
        video.audio.write_audiofile(output_file)
        video.close()
        return
    except Exception as e:
        print(
            f'\033[91mError with file: {input_file} the file will not be created.\n\033[91mERROR CODE : {e} the program will continue\033[0m')
        return


def download_video_from_file(input_file: str, ouput_path):
    try:
        with open(input_file, 'r') as f:
            file_data = f.read()
        file_data = file_data.split('\n')
        file_data = [line.strip() for line in file_data if line.strip()]
        downloaded_video = []
    except Exception as e:
        print(f'Error with the file opening or format.\n\033[91mERROR : {e}\033[0m')
        return
    for e in file_data:
        video_path = download_video(video_url=e, output_path=ouput_path)
        if video_path == "all ready Downloaded":
            continue
        downloaded_video.append(video_path)

    return ouput_path, downloaded_video


def argument_handler():
    parser = argparse.ArgumentParser(description='A youtube downloader script')
    parser.add_argument('-u', '--url', help='Url to the video you want to download on youtube', type=str)
    parser.add_argument('-pl', '--playlist', help='Enter the URL of the playlist to download', type=str)
    parser.add_argument('-tl', '--textlist', help='Enter a text file with URL to download', type=str)
    parser.add_argument('-mp', '--mp34', help='Output file path', type=str, default='mp4',
                        required='-u' in sys.argv or '-pl' in sys.argv or '-tl' in sys.argv)
    parser.add_argument('-o', '--output', help='path to the output file', type=str, default=os.getcwd(),
                        required='-u' in sys.argv or '-pl' in sys.argv or '-tl' in sys.argv)
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


if __name__ == "__main__":
    args = argument_handler()
    if args.url:
        if args.mp34 == 'mp4':
            download_video(args.url, args.output)
        if args.mp34 == 'mp3':
            download_and_convert_to_mp3(args.url, args.output)
    elif args.textlist:
        if args.mp34 == 'mp4':
            download_video_from_file(args.textlist, args.output)
        if args.mp34 == 'mp3':
            output_path, video_path = download_video_from_file(args.textlist, args.output)
            for e in video_path:
                convert_video_to_mp3(e, output_path)
                os.remove(e)
        else:
            print('The mp34 is either mp3 or mp4.\n\033[91mexit\033[0m')
    elif args.playlist:
        if args.mp34 == 'mp4':
            playlist_download(args.playlist, args.output)
        if args.mp34 == 'mp3':
            output_path, video_path = playlist_download(args.playlist, args.output)
            for e in video_path:
                convert_video_to_mp3(e, output_path)
                os.remove(e)
        print('The mp34 is either mp3 or mp4.\n\033[91mexit\033[0m')

    else:
        main_menu()  # launch program mode
