from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QListWidgetItem
from PyQt6.QtCore import QThread, Qt


from youtube_downloader import VideoWorker
from youtube_downloader import DownloadWorker
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

        self.selected_quality = None
        self.unique_url = set()
        self.video_dicts = {}
        self.formats_by_url = {}
        self.active_workers = []


    def add_video(self):
        url = self.url_line.text().strip()
        if url in self.unique_url:
            self.url_line.clear()
            QMessageBox.information(self, "Information", "This video already added to queue.")
            return

        if url:
            self.url_btn.setEnabled(False)

            thread = QThread(self)
            worker = VideoWorker(url)
            worker.moveToThread(thread)
            thread.started.connect(worker.run)
            worker.finished.connect(self.on_finished)
            worker.info_add.connect(self.on_add_info)
            worker.error.connect(self.on_error)
            worker.finished.connect(thread.quit)
            worker.finished.connect(worker.deleteLater)
            thread.finished.connect(thread.deleteLater)
            thread.start()

            self.active_workers.append((thread, worker))

            thread.finished.connect(lambda: self.cleanup_thread(thread))

        else:
            QMessageBox.warning(self, "Warning", "Enter url line before adding video.")



    def on_add_info(self, all_info, formats):
        url = all_info["webpage_url"]
        self.video_dicts[url] = all_info

        item = QListWidgetItem(all_info["title"])
        item.setData(Qt.ItemDataRole.UserRole, url)
        self.media_list.addItem(item)

        self.formats_by_url[url] = formats


    def on_finished(self, info, url):
        self.unique_url.add(url)
        self.url_btn.setEnabled(True)
        self.url_line.clear()
        QMessageBox.information(self, "Success", "Added to the queue.")

    def on_error(self, error):
        self.url_btn.setEnabled(True)
        QMessageBox.warning(self, f"Failure", f"Could not find a video {error}")

    def cleanup_thread(self, thread):
        self.active_workers = [tw for tw in self.active_workers if tw[0] != thread]

    def on_media_item_clicked(self, item):
        url = item.data(Qt.ItemDataRole.UserRole)
        formats = self.formats_by_url[url]
        video_info = self.video_dicts.get(url)
        if video_info:
            self.preview_widget.set_video(video_info)
            self.quality_combo.add_formats(formats)

    def on_quality_changed(self, text):
        self.selected_quality = text

    def on_download(self):
        item = self.media_list.currentItem()
        url = item.data(Qt.ItemDataRole.UserRole)
        quality = self.selected_quality
        output_dir = self.output_dir_line.text().strip()
        errors = []
        if not output_dir:
            errors.append("Choose output directory.")
        if not item:
            errors.append("Add media to download.")

        if errors:
            QMessageBox.warning(self, "Error", "\n".join(errors))
            return


        self.start_download(url, quality, output_dir)

    def start_download(self, url, quality, output_dir):
        self.start_btn.setEnabled(False)
        video = quality[:-1]
        settings = f"bestvideo[height={video}]+bestaudio/best[height={video}]"

        self.thread = QThread()
        self.worker = DownloadWorker(url, settings, output_dir)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.on_download_finished)

        self.thread.start()

    def on_download_finished(self):
        self.start_btn.setEnabled(True)
        QMessageBox.information(self, "Success", "Video downloaded successfully.")

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Choose path")
        if directory:
            self.output_dir_line.setText(directory)