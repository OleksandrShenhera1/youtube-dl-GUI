from PyQt6.QtCore import pyqtSignal, QObject
import yt_dlp
import subprocess

class VideoWorker(QObject):
    finished = pyqtSignal(str, str)
    error = pyqtSignal(str)
    info_add = pyqtSignal(dict, list)
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

                result = subprocess.run(["yt-dlp", "-F", self.url], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                formats = result.stdout
                formats_result = result.stdout.splitlines()
                #print(formats)

                end_info = f"{info['title']}, duration: {str(info['duration'])} sec."
                self.finished.emit(end_info, self.url)
                self.info_add.emit(video_dict, formats_result)

        except Exception as e:
            self.error.emit(str(e))

class DownloadWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    def __init__(self, url, settings, recode, output_dir):
        super().__init__()
        self.url = url
        self.settings = settings
        self.recode = recode
        self.output_dir = output_dir
        self.is_running = True

    def run(self):
        if not self.is_running:
            return

        def hook(d):
            if d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                downloaded = d.get('downloaded_bytes', 0)
                if total:
                    percent = downloaded / total * 100
                    self.progress.emit(percent)
            elif d['status'] == 'finished':
                self.progress.emit(100)

                self.progress.emit(-1)

        ydl_opts = {'format': f'{self.settings}', 'outtmpl': f'{self.output_dir}/%(title)s.%(ext)s', 'progress_hooks': [hook], 'verbose': True}
        if self.recode:
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': self.recode,
            }]
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
                self.finished.emit()
        except Exception as e:
            print(str(e))
            return

    def stop(self):
        self.is_running = False

