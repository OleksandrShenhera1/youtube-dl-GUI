from PyQt6.QtCore import QThread, pyqtSignal, QObject
import yt_dlp

class VideoWorker(QObject):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    info_add = pyqtSignal(dict)
    def __init__(self, url):
        super().__init__()
        self.url = url


    def run(self):
        try:
            ydl_opts = {}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=False)

                video_dict = {
                    "title": info['title'],
                    "duration": info['duration'],
                    "author": info['uploader'],
                    "description": info['description'],
                    "thumbnail": info['thumbnail'],
                    "webpage_url": info['webpage_url'],
                }

                end_info = f"{info['title']}, duration: {str(info['duration'])} sec."
                self.finished.emit(end_info)
                self.info_add.emit(video_dict)
        except Exception as e:
            self.error.emit(str(e))




