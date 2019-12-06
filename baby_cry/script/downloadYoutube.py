from pytube import YouTube
yt = YouTube("https://www.youtube.com/watch?v=E0W5sJZ2d64&t=2s")

stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
stream.download('./', 'fromYoutube')
