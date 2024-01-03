import os
import re


def youtube_url_sanitization(prompt: str) -> str:
    # Define a regular expression pattern for YouTube video URLs
    youtube_url_pattern = re.compile(
        r"^(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})"
    )
    input_sanitized = False
    word_to_end_input: list[str] = ['quit', 'q', '', ' ', 'end', 'fini', 'over']
    input_url = ''
    while not input_sanitized:
        input_url = input(f'{prompt}\nTo finish Enter one of these word : {word_to_end_input}')
        # Check if the input URL matches the YouTube URL pattern
        match = youtube_url_pattern.match(input_url)

        # Look if the user want to quit the URL matching
        if input_url.lower() in word_to_end_input:
            input_url = 'quit'
            input_sanitized = True
            continue

        # look if it is a URL
        elif match:
            input_url = "https://www.youtube.com/watch?v=" + match.group(6)
            input_sanitized = True
            continue

        # Nor a URL or a quit word
        else:
            # Raise a ValueError if the input is not a valid YouTube video URL
            raise ValueError(f"{input_url} is not a valid YouTube video URL.\nEnter a valid Youtube URL")

    return input_url

def is_youtube_url(prompt: str) -> bool:
    url = input(prompt)
    youtube_base_url_pattern = re.compile(r'^https://www\.youtube\.com/')
    if youtube_base_url_pattern.match(url):
        return url
    else:
        raise ValueError(f"{url} is not a valid YouTube URL.\nEnter a valid Youtube URL")


def directory_sanitization(prompt: str):
    sanitized = False
    input_path = ''
    while not sanitized:
        input_path = input(prompt)
        if os.path.isdir(input_path):
            sanitized = True
            continue
        else:
            # Raise a ValueError if the path is not a valid directory
            raise ValueError(f"{input_path} is not a valid existing directory.")
    return os.path.abspath(input_path)


def file_sanitization(prompt: str):
    sanitized = False
    input_path = ''
    while not sanitized:
        input_path = input(prompt)
        if os.path.isfile(input_path):
            sanitized = True
        else:
            # Raise a ValueError if the path is not a valid file
            raise ValueError(f"{input_path} is not a valid existing file.")
    return os.path.abspath(input_path)

def user_menu_sanitization(prompt: str, maximum_input: int):
    input_sanitized = False
    u_input = ''
    while not input_sanitized:
        u_input = input(prompt)
        try:
            u_input = int(u_input)

            if 1 <= u_input <= maximum_input:
                u_input = f'{u_input}'
                input_sanitized = True
                continue
        except Exception as ex:
            print(f"try again. The input wasn't an allowed number.\n it should be in between 1 and {maximum_input}\n{ex}")
            continue
    return u_input