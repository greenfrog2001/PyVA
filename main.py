import sys
import platform
from PySide2 import QtCore, QtGui, QtWidgets, QtMultimedia
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

# LANGUAGE CODE FILE
from lang_code import LANGUAGES_LIST, LANGCODES

# GUI FILE
from app_modules import *

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ## PRINT ==> SYSTEM
        print('System: ' + platform.system())
        print('Version: ' +platform.release())

        ########################################################################
        ## START - WINDOW ATTRIBUTES
        ########################################################################

        ## REMOVE ==> STANDARD TITLE BAR
        UIFunctions.removeTitleBar(True)
        ## ==> END ##

        ## WINDOW SIZE ==> DEFAULT SIZE
        startSize = QSize(1000, 720)
        self.resize(startSize)
        self.setMinimumSize(startSize)
        # UIFunctions.enableMaximumSize(self, 500, 720)
        ## ==> END ##

        ## ==> CREATE MENUS
        ########################################################################

        ## ==> TOGGLE MENU SIZE
        self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self, 220, True))
        ## ==> END ##

        ## ==> ADD CUSTOM MENUS
        self.ui.stackedWidget.setMinimumWidth(20)
        UIFunctions.addNewMenu(self, "HOME", "btn_home", "url(:/16x16/icons/16x16/cil-home.png)", True)
        UIFunctions.addNewMenu(self, "YOUTUBE PLAYER", "btn_youtube_player", "url(:/16x16/icons/16x16/cil-featured-playlist.png)", True)
        UIFunctions.addNewMenu(self, "PYVA TRANSLATE", "btn_translate", "url(:/16x16/icons/16x16/cil-transfer.png)", True)
        ## ==> END ##

        # START MENU => SELECTION
        UIFunctions.selectStandardMenu(self, "btn_home")
        ## ==> END ##

        ## ==> START PAGE
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
        ## ==> END ##

        ## USER ICON ==> SHOW HIDE
        UIFunctions.userIcon(self, "GF", "", True)
        ## ==> END ##


        ## ==> MOVE WINDOW / MAXIMIZE / RESTORE
        ########################################################################
        def moveWindow(event):
            # IF MAXIMIZED CHANGE TO NORMAL
            if UIFunctions.returStatus() == 1:
                UIFunctions.maximize_restore(self)

            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        # WIDGET TO MOVE
        self.ui.frame_label_top_btns.mouseMoveEvent = moveWindow
        ## ==> END ##

        ## ==> LOAD DEFINITIONS
        ########################################################################
        UIFunctions.uiDefinitions(self)
        ## ==> END ##

        ########################################################################
        ## END - WINDOW ATTRIBUTES
        ############################## ---/--/--- ##############################




        ########################################################################
        #                                                                      #
        ## START -------------- WIDGETS FUNCTIONS/PARAMETERS ---------------- ##
        #                                                                      #
        ## ==> USER CODES BELLOW                                              ##
        ########################################################################
        # SET VARIABLE FOR PAUSE/RESUME BUTTON COUNT
        self.pause_count = 0

        # BIND BUTTONS
        self.ui.search_btn.clicked.connect(self.btn_clicked)
        self.ui.sound_btn.clicked.connect(self.btn_clicked)
        self.ui.youtube_search_btn.clicked.connect(self.btn_clicked)
        self.ui.youtube_pause.clicked.connect(self.btn_clicked)
        self.ui.youtube_stop.clicked.connect(self.btn_clicked)
        self.ui.translate_btn.clicked.connect(self.btn_clicked)
        self.ui.src_sound.clicked.connect(self.btn_clicked)
        self.ui.dest_sound.clicked.connect(self.btn_clicked)

        # ADD ITEMS TO TRANSLATE COMBO BOX
        self.ui.src_box.addItem('Auto Detect')
        self.ui.src_box.addItems(LANGUAGES_LIST)
        self.ui.dest_box.addItems(LANGUAGES_LIST)

        ## ==> QTableWidget RARAMETERS
        ########################################################################
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        ## ==> END ##



        ########################################################################
        #                                                                      #
        ## END --------------- WIDGETS FUNCTIONS/PARAMETERS ----------------- ##
        #                                                                      #
        ############################## ---/--/--- ##############################


        ## SHOW ==> MAIN WINDOW
        ########################################################################
        self.show()
        ## ==> END ##

    ########################################################################
    ## MENUS ==> DYNAMIC MENUS FUNCTIONS
    ########################################################################
    def Button(self):
        # GET BT CLICKED
        btnWidget = self.sender()

        # PAGE HOME
        if btnWidget.objectName() == "btn_home":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            UIFunctions.resetStyle(self, "btn_home")
            UIFunctions.labelPage(self, "Home")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        # PAGE YOUTUBE PLAYER
        if btnWidget.objectName() == "btn_youtube_player":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_youtube)
            UIFunctions.resetStyle(self, "btn_youtube_player")
            UIFunctions.labelPage(self, "Youtube Player")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        # PAGE PYVA TRANSLATE
        if btnWidget.objectName() == "btn_translate":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_translate)
            UIFunctions.resetStyle(self, "btn_translate")
            UIFunctions.labelPage(self, "Translate")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        # PAGE WIDGETS
        if btnWidget.objectName() == "btn_widgets":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_widgets)
            UIFunctions.resetStyle(self, "btn_widgets")
            UIFunctions.labelPage(self, "Custom Widgets")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

    ## ==> END ##

    ########################################################################
    ## START ==> APP EVENTS
    ########################################################################

    ## EVENT ==> BUTTON CLICK
    def btn_clicked(self):
        if self.sender().objectName() == "search_btn":
            query = self.ui.user_input.text()
            self.ui.answer_output.setText(Functions.GetAnswer(query))
        if self.sender().objectName() == "sound_btn":
            query = self.ui.user_input.text()
            self.ui.answer_output.setText(Functions.GetAnswer(query))
            url = Functions.GetSound(query)
            self.ui.mediaPlayer = QtMultimedia.QMediaPlayer(self)
            self.ui.mediaPlayer.setMedia(QtMultimedia.QMediaContent(url))
            self.ui.mediaPlayer.play()
        if self.sender().objectName() == "youtube_search_btn":
            print("YT search works!")
            query = self.ui.youtube_search_input.text()
            url = Functions.GetYouTubeLink(query)
            if Functions.MediaCheck():
                Functions.StopVideo()
            Functions.VLCPlay(url)
        if self.sender().objectName() == "youtube_pause":
            Functions.PauseVideo()
            if (self.pause_count % 2 == 0):
                self.ui.youtube_pause.setStyleSheet(u"QPushButton {\n"
            "	background-image: url(:/20x20/icons/20x20/cil-media-play.png);\n"
            "	background-position: center;\n"
            "	background-repeat: no-reperat;\n"
            "	border: none;\n"
            "	background-color: rgb(27, 29, 35);\n"
            "}\n"
            "QPushButton:hover {\n"
            "	background-color: rgb(33, 37, 43);\n"
            "}\n"
            "QPushButton:pressed {	\n"
            "	background-color: rgb(85, 170, 255);\n"
            "}")
            else:
                self.ui.youtube_pause.setStyleSheet(u"QPushButton {\n"
            "	background-image: url(:/20x20/icons/20x20/cil-media-pause.png);\n"
            "	background-position: center;\n"
            "	background-repeat: no-reperat;\n"
            "	border: none;\n"
            "	background-color: rgb(27, 29, 35);\n"
            "}\n"
            "QPushButton:hover {\n"
            "	background-color: rgb(33, 37, 43);\n"
            "}\n"
            "QPushButton:pressed {	\n"
            "	background-color: rgb(85, 170, 255);\n"
            "}")
            self.pause_count += 1
        if self.sender().objectName() == "youtube_stop":
            Functions.StopVideo()
        if self.sender().objectName() == "translate_btn":
            src_text_input = self.ui.src_text.toPlainText()
            src_language = self.ui.src_box.currentText().lower()
            dest_language = self.ui.dest_box.currentText().lower()
            dest = LANGCODES[dest_language]

            if src_language == 'auto detect':
                dest_text_output = Functions.Translate(src_text_input, src_language, dest)
            else:
                src = LANGCODES[src_language]
                dest_text_output = Functions.Translate(src_text_input, src, dest)
            self.ui.dest_text.setText(dest_text_output)
        if self.sender().objectName() == "src_sound":
            src_text_input = self.ui.src_text.toPlainText()
            src_language = self.ui.src_box.currentText().lower()
            dest_language = self.ui.dest_box.currentText().lower()
            dest = LANGCODES[dest_language]

            if src_language == 'auto detect':
                if os.path.exists('gtts_obj.mp3'):
                    os.remove('gtts_obj.mp3')
                gtts_obj = gTTS(src_text_input, lang='en')
                gtts_obj.save('gtts_obj.mp3')
                url = QtCore.QUrl.fromLocalFile('gtts_obj.mp3')
            else:
                src = LANGCODES[src_language]
                if os.path.exists('gtts_obj.mp3'):
                    os.remove('gtts_obj.mp3')
                gtts_obj = gTTS(src_text_input, lang=src)
                gtts_obj.save('gtts_obj.mp3')
                url = QtCore.QUrl.fromLocalFile('gtts_obj.mp3')
            self.ui.mediaPlayer = QtMultimedia.QMediaPlayer(self)
            self.ui.mediaPlayer.setMedia(QtMultimedia.QMediaContent(url))
            self.ui.mediaPlayer.play()
        if self.sender().objectName() == "dest_sound":
            dest_text_input = self.ui.dest_text.toPlainText()
            dest_language = self.ui.dest_box.currentText().lower()
            dest = LANGCODES[dest_language]

            if os.path.exists('gtts_obj.mp3'):
                os.remove('gtts_obj.mp3')
            gtts_obj = gTTS(dest_text_input, lang=dest)
            gtts_obj.save('gtts_obj.mp3')
            url = QtCore.QUrl.fromLocalFile('gtts_obj.mp3')
            self.ui.mediaPlayer = QtMultimedia.QMediaPlayer(self)
            self.ui.mediaPlayer.setMedia(QtMultimedia.QMediaContent(url))
            self.ui.mediaPlayer.play()



    ## EVENT ==> MOUSE DOUBLE CLICK
    ########################################################################
    def eventFilter(self, watched, event):
        if watched == self.le and event.type() == QtCore.QEvent.MouseButtonDblClick:
            print("pos: ", event.pos())
    ## ==> END ##

    ## EVENT ==> MOUSE CLICK
    ########################################################################
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')
        if event.buttons() == Qt.MidButton:
            print('Mouse click: MIDDLE BUTTON')
    ## ==> END ##

    ## EVENT ==> KEY PRESSED
    ########################################################################
    def keyPressEvent(self, event):
        print('Key: ' + str(event.key()) + ' | Text Press: ' + str(event.text()))
    ## ==> END ##

    ## EVENT ==> RESIZE EVENT
    ########################################################################
    def resizeEvent(self, event):
        self.resizeFunction()
        return super(MainWindow, self).resizeEvent(event)

    def resizeFunction(self):
        print('Height: ' + str(self.height()) + ' | Width: ' + str(self.width()))
    ## ==> END ##

    ########################################################################
    ## END ==> APP EVENTS
    ############################## ---/--/--- ##############################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeui.ttf')
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeuib.ttf')
    window = MainWindow()
    sys.exit(app.exec_())
