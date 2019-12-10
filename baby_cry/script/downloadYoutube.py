from pytube import YouTube
def downloadVideo(url):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
    stream.download('./', 'fromYoutube')
