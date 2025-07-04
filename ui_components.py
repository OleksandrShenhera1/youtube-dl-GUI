from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, QGroupBox,
    QComboBox, QLabel, QLineEdit, QProgressBar, QTextEdit, QSizePolicy
)
import requests
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import pyqtSignal, Qt

class VideoFormat(QComboBox):
    def __init__(self, formats=None, parent=None):
        super().__init__(parent)
        if formats:
            self.add_formats(formats)

    def add_formats(self, formats):
        if not formats:
            return
        self.clear()
        if any("2160p" in f for f in formats):
            self.addItem("2160p")
        if any("1440p" in f for f in formats):
            self.addItem("1440p")
        if any("1080p" in f for f in formats):
            self.addItem("1080p")
        if any("720p" in f for f in formats):
            self.addItem("720p")
        if any("480p" in f for f in formats):
            self.addItem("480p")
        if any("360p" in f for f in formats):
            self.addItem("360p")

class DownloadFormat(QComboBox):
    def __init__(self, recode=None, parent=None):
        super().__init__(parent)
        if recode:
            self.add_recode(recode)

    def add_recode(self, recode):
        if not recode:
            return
        self.clear()
        if any("mp4" in r for r in recode):
            self.addItem("mp4")
        if any("mkv" in r for r in recode):
            self.addItem("mkv")
        if any("webm" in r for r in recode):
            self.addItem("webm")
        if any("avi" in r for r in recode):
            self.addItem("avi")



class VideoPreview(QWidget):
    def __init__(self, video_dict=None, parent=None):
        super().__init__(parent)
        main_layout = QVBoxLayout(self)

        self.url_line = QLineEdit()
        self.url_line.setPlaceholderText("video url")
        self.url_line.setReadOnly(True)
        main_layout.addWidget(self.url_line)

        center_layout = QHBoxLayout()
        main_layout.addLayout(center_layout)

        left_layout = QVBoxLayout()
        center_layout.addLayout(left_layout, stretch=2)

        self.thumbnail_label = QLabel()
        self.thumbnail_label.setObjectName("thumbnail")
        self.thumbnail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thumbnail_label.setFixedSize(360, 240)
        left_layout.addWidget(self.thumbnail_label)

        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.title_label.setWordWrap(True)
        left_layout.addWidget(self.title_label)

        right_layout = QVBoxLayout()
        center_layout.addLayout(right_layout, stretch=1)

        self.author_label = QLabel()
        right_layout.addWidget(self.author_label)

        self.description_edit = QTextEdit()
        self.description_edit.setReadOnly(True)
        #self.description_edit.setMaximumHeight(90)
        self.description_edit.setFixedWidth(350)
        self.description_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        right_layout.addWidget(self.description_edit)

        self.clear()

        if video_dict:
            self.set_video(video_dict)

    def set_video(self, video_dict):
        self.url_line.setText(video_dict.get('webpage_url', ''))
        self.title_label.setText(f"Title: {video_dict.get('title', '')}")
        self.author_label.setText(f"Author: {video_dict.get('author', '')}")
        self.description_edit.setText(video_dict.get('description', ''))

        thumb_url = video_dict.get('thumbnail')
        if thumb_url:
            try:
                response = requests.get(thumb_url)
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                self.thumbnail_label.setPixmap(pixmap.scaled(
                    self.thumbnail_label.width(),
                    self.thumbnail_label.height(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                ))
            except Exception:
                self.thumbnail_label.setText("No preview")
        else:
            self.thumbnail_label.setText("No preview")

    def clear(self):
        self.url_line.clear()
        self.title_label.clear()
        self.author_label.clear()
        self.description_edit.clear()
        self.thumbnail_label.clear()


def create_main_widget(parent_window):

    central_widget = QWidget()
    main_layout = QHBoxLayout(central_widget)

    # media-block (left)
    media_full_block = QGroupBox("Add-media")
    media_block = QVBoxLayout(media_full_block)

    # media url btn (left top)
    parent_window.url_line = QLineEdit()
    parent_window.url_line.setPlaceholderText("url:")
    parent_window.url_btn = QPushButton("Add")
    parent_window.url_btn.clicked.connect(parent_window.add_video)
    media_block.addWidget(parent_window.url_line)
    media_block.addWidget(parent_window.url_btn)

    # videos (left bottom)
    media = QGroupBox("Videos")
    media_show = QHBoxLayout(media)

    parent_window.media_list = QListWidget()
    parent_window.media_list.itemClicked.connect(parent_window.on_media_item_clicked)
    media_show.addWidget(parent_window.media_list)

    media_block.addWidget(media)

    main_layout.addWidget(media_full_block, stretch=1)

    # settings block (right top)
    right_box = QVBoxLayout()

    settings_block = QGroupBox("Settings")
    settings_layout = QVBoxLayout(settings_block)

    upper_settings = QHBoxLayout()

    parent_window.quality_combo = VideoFormat()
    parent_window.quality_combo.currentTextChanged.connect(parent_window.on_quality_changed)
    parent_window.status_bar = QProgressBar()
    parent_window.status_bar.setValue(0)

    upper_settings.addWidget(parent_window.quality_combo)
    upper_settings.addWidget(parent_window.status_bar)

    bottom_settings = QHBoxLayout()

    parent_window.video_sett_combo = DownloadFormat()
    parent_window.video_sett_combo.currentTextChanged.connect(parent_window.on_recode_changed)
    parent_window.output_dir_line = QLineEdit()
    parent_window.output_dir_line.setPlaceholderText("C:\\User\\Name\\Videos")
    parent_window.output_dir_btn = QPushButton("Browse")
    parent_window.output_dir_btn.clicked.connect(parent_window.browse_directory)
    parent_window.start_btn = QPushButton("Start")
    parent_window.start_btn.clicked.connect(parent_window.on_download)
    bottom_settings.addWidget(parent_window.video_sett_combo)
    bottom_settings.addWidget(parent_window.output_dir_line)
    bottom_settings.addWidget(parent_window.output_dir_btn)
    settings_layout.addLayout(upper_settings)
    settings_layout.addLayout(bottom_settings)

    start_settings = QHBoxLayout()
    start_settings.addWidget(parent_window.start_btn)
    settings_layout.addLayout(start_settings)
    right_box.addWidget(settings_block)


    preview_group = QGroupBox("Video preview")
    preview_layout = QHBoxLayout(preview_group)
    parent_window.preview_widget = VideoPreview()
    preview_layout.addWidget(parent_window.preview_widget)

    right_box.addWidget(preview_group, stretch=1)

    main_layout.addLayout(right_box, stretch=2)
    return central_widget

