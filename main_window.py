#!/usr/bin/env python

from PySide2.QtCore import QDir, QUrl, Signal, Qt, QTime
from PySide2.QtMultimedia import QMediaContent, QMediaPlayer
from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtWidgets import QApplication, QFileDialog, QWidget, QGridLayout, QMainWindow, QSlider, QLabel, QVBoxLayout, QFrame, QToolButton,QStyle, QHBoxLayout
import sys

class ClickableVideoWidget(QVideoWidget):
    clicked = Signal()

    def __init__(self, parent=None):
        super(ClickableVideoWidget, self).__init__(parent)

    def mousePressEvent(self, event):
        self.clicked.emit()

class VideoWindow(QMainWindow):
    def __init__(self, camera_count):
        super(VideoWindow, self).__init__()
        self.mediaPlayers = []
        self.videoWidgets = []
        self.positionSliders = []
        self.stop_buttons = []
        self.list_openButtons = []
        self.list_label_duration = []
        self.list_duration_time = {}
        self.setMinimumSize(640, 480)
        self.setWindowTitle("Video Player")
        self.camera_count = camera_count
        # Create a grid layout
        gridLayout = QGridLayout(self)
        gridLayout.setContentsMargins(0, 0, 0, 0)
        self.num_col = 3 if self.camera_count > 4 else 1 if self.camera_count == 1 else 2

        for i in range(self.camera_count):
            frame = QFrame()
            frame.setObjectName(u"frame_main")
            frame.setStyleSheet(u"QFrame{\n"
                "border:0px;\n"
                "background: rgb(52, 59, 72);\n"
                " border-radius: 10px;\n"
                "}\n"
                "/* LINE EDIT */\n"
                "/* SLIDERS */\n"
                "QSlider::groove:horizontal {\n"
                "    border-radius: 9px;\n"
                "    height: 18px;\n"
                "	margin: 0px;\n"
                "	background-color: rgb(52, 59, 72);\n"
                "}\n"
                "QSlider::groove:horizontal:hover {\n"
                "	background-color: rgb(55, 62, 76);\n"
                "}\n"
                "QSlider::handle:horizontal {\n"
                "    background-color: rgb(85, 170, 255);\n"
                "    border: none;\n"
                "    height: 18px;\n"
                "    width: 18px;\n"
                "    margin: 0px;\n"
                "	border-radius: 9px;\n"
                "}\n"
                "QSlider::handle:horizontal:hover {\n"
                "    background-color: rgb(105, 180, 255);\n"
                "}\n"
                "QSlider::handle:horizontal:pressed {\n"
                "    background-color: rgb(65, 130, 195);\n"
                "}\n"
                "\n"
                "QSlider::groove:vertical {\n"
                "    border-radius: 9px;\n"
                "    width: 18px;\n"
                "    margin: 0px;\n"
                "	background-color: rgb(52, 59, 72);\n"
                "}\n"
                "QSlider::groove:vertical:hover {\n"
                "	background-color: rgb(55, 62, 76);\n"
                "}\n"
                "QSlider::handle:verti"
                                        "cal {\n"
                "    background-color: rgb(85, 170, 255);\n"
                "	border: none;\n"
                "    height: 18px;\n"
                "    width: 18px;\n"
                "    margin: 0px;\n"
                "	border-radius: 9px;\n"
                "}\n"
                "QSlider::handle:vertical:hover {\n"
                "    background-color: rgb(105, 180, 255);\n"
                "}\n"
                "QSlider::handle:vertical:pressed {\n"
                "    background-color: rgb(65, 130, 195);\n"
                "}\n"
                "\n"
                "")
            frame.setFrameShape(QFrame.Box)
            frame.setLineWidth(2)
            layout_video = QVBoxLayout()

            widget_video = ClickableVideoWidget()
            layout_video.addWidget(widget_video)
            # time_layout = QHBoxLayout()
            position_slider = QSlider(Qt.Horizontal)
            position_slider.setRange(0, 0)  # Set the range initially to 0
            position_slider.sliderMoved.connect(self.setPosition)
            layout_video.addWidget(position_slider)
            # labelDuration = QLabel("00:00:00 / 00:00:00")
            # time_layout.addWidget(labelDuration)
            # layout_video.addLayout(time_layout)

            layout_control = QHBoxLayout()
            stopButton = QToolButton(clicked=self.stop)
            stopButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            stopButton.setEnabled(False)
            self.stop_buttons.append(stopButton) 
            layout_control.addWidget(stopButton)

            # openButton = QToolButton(clicked=self.fullScreen)
            # openButton.setIcon(self.style().standardIcon(QStyle.SP_FileIcon))
            # self.list_openButtons.append(openButton)
            # layout_control.addWidget(openButton)

            layout_video.addLayout(layout_control)

            frame.setLayout(layout_video)
            player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
            player.setVideoOutput(widget_video)
            player.positionChanged.connect(self.update_slider_value)
            player.durationChanged.connect(self.durationChanged)
            player.mediaStatusChanged.connect(self.mediaStatusChanged)
            self.mediaPlayers.append(player)
            self.videoWidgets.append(widget_video)
            self.positionSliders.append(position_slider)
            # self.list_label_duration.append(labelDuration)
            gridLayout.addWidget(frame, i // self.num_col, i % self.num_col, 1, 1)
            def on_widget_clicked(row=i // self.num_col, col=i % self.num_col):
                return lambda: self.load_and_play_video(row, col)
            widget_video.clicked.connect(on_widget_clicked())

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)
        # Set widget to contain window contents
        wid.setLayout(gridLayout)
    def update_slider_value(self, position):
        sender = self.sender()
        index = self.mediaPlayers.index(sender)
        self.positionSliders[index].setValue(position)

    def mediaStatusChanged(self, status):
        if status == QMediaPlayer.EndOfMedia:
            # Restart the video when it reaches the end
            sender = self.sender()
            index = self.mediaPlayers.index(sender)
            self.mediaPlayers[index].setPosition(0)
            self.mediaPlayers[index].play()
            self.stop_buttons[index].setEnabled(True)
            duration = self.mediaPlayers[index].duration()
            self.positionSliders[index].setRange(0, duration)
            self.mediaPlayers[index].play()

    def setPosition(self, position):
        position /= 1000
        sender = self.sender()
        index = self.positionSliders.index(sender)
        self.mediaPlayers[index].setPosition(position)
        self.updateDurationInfo(position)
    def updateDurationInfo(self, currentInfo):
        index = self.sender().index
        duration = self.list_duration_time[index]
        if currentInfo or duration:
            currentTime = QTime((currentInfo/3600)%60, (currentInfo/60)%60,
                    currentInfo%60, (currentInfo*1000)%1000)
            totalTime = QTime((duration/3600)%60, (duration/60)%60,
                    duration%60, (duration*1000)%1000);

            format = 'hh:mm:ss' if duration > 3600 else 'mm:ss'
            tStr = currentTime.toString(format) + " / " + totalTime.toString(format)
        else:
            tStr = ""

        self.list_label_duration[index].setText(tStr)
    
    def stop(self):
        sender = self.sender()
        index = self.stop_buttons.index(sender)
        player = self.mediaPlayers[index]
        if player.state() == QMediaPlayer.PlayingState:
            player.pause()
            sender.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        else:
            player.play()
            sender.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

    def fullScreen(self):
        sender = self.sender()
        index = self.list_openButtons.index(sender)
        video_widget = self.videoWidgets[index]
        video_widget.setFullScreen(not video_widget.isFullScreen())


    def durationChanged(self, duration):
        sender = self.sender()
        index = self.mediaPlayers.index(sender)
        self.positionSliders[index].setRange(0, duration)
        self.list_duration_time[index] = duration

    def load_and_play_video(self, row, col):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Video Files (*.mp4 *.mkv *.mov *.avi *.flv *.webm *.wmv)")
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                player_index = row * self.num_col + col
                self.mediaPlayers[player_index].setMedia(QMediaContent(QUrl("file:///" + file_path)))
                self.mediaPlayers[player_index].play()
                self.stop_buttons[player_index].setEnabled(True)
                duration = self.mediaPlayers[player_index].duration()
                self.positionSliders[player_index].setRange(0, duration)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow(4)
    player.showMaximized()
    sys.exit(app.exec_())
