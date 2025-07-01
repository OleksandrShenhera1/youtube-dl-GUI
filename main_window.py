from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtCore import QThread
from PyQt6.QtGui import QIcon

from youtube_downloader import VideoWorker

from config import STYLESHEET
from ui_components import create_main_widget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("YouTube Download Client")
        self.setGeometry(100, 100, 1200, 800)

        main_widget = create_main_widget(self)
        self.setCentralWidget(main_widget)
        self.setStyleSheet(STYLESHEET)

        self.unique_url = set()
        self.video_dicts = {}

    def add_video(self):
        url = self.url_line.text().strip()
        if url in self.unique_url:
            self.url_line.clear()
            QMessageBox.information(self, "Information", "This video already added to queue.")
            return

        if url:
            self.unique_url.add(url)

            self.thread = QThread()
            self.worker = VideoWorker(url)
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.on_finished)
            self.worker.info_add.connect(self.on_add_info)
            self.worker.error.connect(self.on_error)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.start()

        else:
            QMessageBox.warning(self, "Warning", "Enter url line before adding video.")

    def on_add_info(self, all_info):
        print(all_info)
        url = all_info["webpage_url"]
        self.video_dicts[url] = all_info
    def on_finished(self, info):
        self.media_list.addItem(info)
        self.url_line.clear()
        QMessageBox.information(self, "Success", "Added to the queue.")

    def on_error(self, error):
        QMessageBox.warning(self, f"Failure", f"Could not find a video {error}")


    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Choose path")
        if directory:
            self.output_dir_line.setText(directory)