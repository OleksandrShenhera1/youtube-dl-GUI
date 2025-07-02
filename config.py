STYLESHEET = """
QWidget {
        background-color: #2E3440;
        color: #D8DEE9;
        font-size: 14px;
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    QMainWindow {
        background-color: #2E3440;
    }
    QGroupBox {
        border: 1px solid #4C566A;
        border-radius: 8px;
        margin-top: 1em;
        font-weight: bold;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px 0 5px;
    }
    QPushButton {
        background-color: #5E81AC;
        color: #ECEFF4;
        border: none;
        padding: 5px 10px;
        border-radius: 8px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #81A1C1;
    }
    QPushButton:pressed {
        background-color: #4C566A;
    }
    QComboBox {
        background-color: #3B4252;
        border: 1px solid #4C566A;
        border-radius: 5px;
        padding: 5px;
    }
    QComboBox::drop-down {
        border: none;
    }
    QComboBox:hover {
        border: 1px solid #81A1C1;
    }
    QLineEdit {
        background-color: #3B4252;
        border: 1px solid #4C566A;
        border-radius: 5px;
        padding: 5px;
    }
    QProgressBar {
        border: 1px solid #4C566A;
        border-radius: 8px;
        text-align: center;
        background-color: #3B4252;
        color: #D8DEE9;
    }
    QProgressBar::chunk {
        background-color: #A3BE8C;
        border-radius: 7px;
    }
    QTextEdit {
        background-color: #3B4252;
        border: 1px solid #4C566A;
        border-radius: 8px;
    }
    QLabel {
        font-weight: bold;
    }
    QLabel#thumbnail {
        margin-top: 25px;
        border: 2px solid #888;
        border-radius: 10px;
        
    }
"""