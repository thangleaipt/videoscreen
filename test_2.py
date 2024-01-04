#!/usr/bin/env python

from PyQt5.QtCore import QDir, Qt, QUrl, pyqtSignal
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QWidget, QGridLayout, QMainWindow)
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QFrame
import sys

class ClickableVideoWidget(QVideoWidget):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super(ClickableVideoWidget, self).__init__(parent)

    def mousePressEvent(self, event):
        self.clicked.emit()

class NonClickableVideoWidget(QFrame):
    def __init__(self, parent=None):
        super(NonClickableVideoWidget, self).__init__(parent)
        self.setFrameShape(QFrame.Box)
        self.setLineWidth(2)
        layout = QVBoxLayout()
        self.label = QLabel("Non-Clickable Video")
        layout.addWidget(self.label)
        self.setLayout(layout)


class VideoWindow(QMainWindow):

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.mediaPlayers = []
        self.videoWidgets = []

        # Create a grid layout
        gridLayout = QGridLayout(self)
        gridLayout.setContentsMargins(0, 0, 0, 0)

        for row in range(2):
            for col in range(2):
                frame = NonClickableVideoWidget()
                gridLayout.addWidget(frame, row, col)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)
        # Set widget to contain window contents
        wid.setLayout(gridLayout)

    def load_and_play_video(self, row, col):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Video Files (*.mp4)")
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]

                # Replace NonClickableVideoWidget with ClickableVideoWidget
                clickable_widget = ClickableVideoWidget()
                self.gridLayout().replaceWidget(self.videoWidgets[row * 2 + col], clickable_widget)
                self.videoWidgets[row * 2 + col] = clickable_widget

                # Set up the new ClickableVideoWidget
                player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
                player.setVideoOutput(clickable_widget)
                self.mediaPlayers[row * 2 + col] = player
                self.mediaPlayers[row * 2 + col].setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
                self.mediaPlayers[row * 2 + col].play()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.showMaximized()
    sys.exit(app.exec_())
