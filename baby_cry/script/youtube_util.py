from pytube import YouTube

def download_audio(url):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
    stream.download('./lullaby/', 'from_youtube')
