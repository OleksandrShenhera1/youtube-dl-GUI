from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, QGroupBox,
    QComboBox, QLabel, QLineEdit, QProgressBar, QTextEdit, QCheckBox, QTextBrowser
)

from PyQt6.QtGui import QPixmap

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
    media_block.addWidget(parent_window.url_line)
    media_block.addWidget(parent_window.url_btn)

    # videos (left bottom)
    media = QGroupBox("Videos")
    media_show = QHBoxLayout(media)

    parent_window.media_list = QListWidget()
    media_show.addWidget(parent_window.media_list)

    media_block.addWidget(media)

    main_layout.addWidget(media_full_block, stretch=1)

    # settings block (right top)
    right_box = QVBoxLayout()

    settings_block = QGroupBox("Settings")
    settings_layout = QVBoxLayout(settings_block)

    upper_settings = QHBoxLayout()

    parent_window.quality_combo = QComboBox()
    parent_window.status_bar = QProgressBar()
    parent_window.status_bar.setValue(0)

    upper_settings.addWidget(parent_window.quality_combo)
    upper_settings.addWidget(parent_window.status_bar)

    bottom_settings = QHBoxLayout()

    parent_window.video_sett_combo = QComboBox()
    parent_window.output_dir_line = QLineEdit()
    parent_window.output_dir_line.setPlaceholderText("C:\\User\\Name\\Videos")
    parent_window.output_dir_btn = QPushButton("Browse")

    bottom_settings.addWidget(parent_window.video_sett_combo)
    bottom_settings.addWidget(parent_window.output_dir_line)
    bottom_settings.addWidget(parent_window.output_dir_btn)

    settings_layout.addLayout(upper_settings)
    settings_layout.addLayout(bottom_settings)

    right_box.addWidget(settings_block)

    preview_group = QGroupBox("Video preview")
    preview_layout = QHBoxLayout(preview_group)
    parent_window.preview_label = QLabel()

    preview_layout.addWidget(parent_window.preview_label)

    right_box.addWidget(preview_group, stretch=1)

    main_layout.addLayout(right_box, stretch=2)
    return central_widget

