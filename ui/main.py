import os
import re
import sys

import fitz
import pyscreenshot
from PIL import Image
from PyQt5 import QtWebEngineWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QPoint, QRect, QAbstractNativeEventFilter, QAbstractEventDispatcher
from PyQt5.QtGui import QPixmap, QPainter, QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QWidget, QVBoxLayout, QDesktopWidget, \
    QSystemTrayIcon, QMenu, QAction, qApp
from pyqtkeybind import keybinder

from qt import Ui_MainWindow
from settings import Ui_Form


class SettingsWindow(QWidget, Ui_Form):
    def __init__(self):
        self.toTray = True
        super(SettingsWindow, self).__init__()
        self.setupUi(self)
        self.ToTrayCheck.setChecked(self.toTray)
        self.ToTrayCheck.toggled.connect(self.check_changed)

    def check_changed(self):
        self.toTray = not self.toTray


class ScreenShotWindow(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.move(0, 0)
        QApplication.setOverrideCursor(Qt.CrossCursor)


        self.setFixedHeight(QDesktopWidget().screenGeometry().height())
        self.setFixedWidth(QDesktopWidget().screenGeometry().width())
        self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
        self.setLayout(layout)
        self.pix = QPixmap(QtGui.QPixmap("screenshot_temp.png"))

        self.RectBegin, self.RectDest = QPoint(), QPoint

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.yellow)
        painter.drawPixmap(QPoint(), self.pix)
        if not self.RectBegin.isNull() and not self.RectDest.isNull():
            rect = QRect(self.RectBegin, self.RectDest)
            painter.drawRect(rect.normalized())

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        if e.buttons() & Qt.LeftButton:
            self.RectBegin = e.pos()
            self.RectDest = self.RectBegin
            self.update()

    def mouseMoveEvent(self, e: QtGui.QMouseEvent):
        if e.buttons() & Qt.LeftButton:
            self.RectDest = e.pos()
            self.update()

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent):

        if e.button() & Qt.LeftButton:
            rect = QRect(self.RectBegin, self.RectDest)
            painter = QPainter(self.pix)
            painter.drawRect(rect.normalized())
            im = Image.open("screenshot_temp.png")
            if abs(self.RectBegin.x() - self.RectDest.x()) < 10 or abs(self.RectBegin.y() - self.RectDest.y()) < 10:
                QMessageBox.warning(self, "Ошибка",
                                    "Слишком маленький скриншот!",
                                    QMessageBox.Ok)
                self.destroy(destroyWindow=True)
                self.close()
                QApplication.restoreOverrideCursor()
                return
            if self.RectBegin.x() < self.RectDest.x():
                if self.RectBegin.y() < self.RectDest.y():
                    x, y, xd, yd = self.RectBegin.x(), self.RectBegin.y(), self.RectDest.x(), self.RectDest.y()
                elif self.RectBegin.y() > self.RectDest.y():
                    x, y, xd, yd = self.RectBegin.x(), self.RectDest.y(), self.RectDest.x(), self.RectBegin.y()
            elif self.RectBegin.x() > self.RectDest.x():
                if self.RectBegin.y() < self.RectDest.y():
                    x, y, xd, yd = self.RectDest.x(), self.RectBegin.y(), self.RectBegin.x(), self.RectDest.y()
                elif self.RectBegin.y() > self.RectDest.y():
                    x, y, xd, yd = self.RectDest.x(), self.RectDest.y(), self.RectBegin.x(), self.RectBegin.y()

            im.crop((x, y, xd, yd)).save("result/screenshot.png", quality=100)
            self.RectBegin, self.RectDest = QPoint(), QPoint
            os.remove("screenshot_temp.png")
            QApplication.restoreOverrideCursor()
            self.destroy(destroyWindow=True)
            self.close()

    def keyPressEvent(self, e: QtGui.QKeyEvent):
        if e.key() & Qt.Key_Escape:
            os.remove("screenshot_temp.png")
            self.close()


class App(QMainWindow, Ui_MainWindow):
    pageCount = 0
    imgs = []
    chosenPages = []
    textBoxChosenPages = []
    checkBoxes = []
    model = QtGui.QStandardItemModel()

    def __init__(self):
        super().__init__()

        self.settings_window = SettingsWindow()
        self.keybinder = keybinder
        self.screen_shot_window = None
        self.tray_icon = QSystemTrayIcon(self)
        self.pdfview = QtWebEngineWidgets.QWebEngineView()
        self.all_dates = {}
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):

        self.action.triggered.connect(self.screen_shot_part)
        self.action_2.triggered.connect(self.screen_shot)
        self.OpenFile.triggered.connect(self.add_file)
        self.Exit.triggered.connect(qApp.quit)
        self.Settings.triggered.connect(self.show_settings)

        self.openFileButton.clicked.connect(self.add_file)
        self.verticalLayout.addWidget(self.verticalLayoutWidget)
        self.verticalLayout.addWidget(self.pdfview)
        self.setAcceptDrops(True)
        self.listView.setModel(self.model)
        self.listView.clicked[QtCore.QModelIndex].connect(self.open_file_list)
        self.Delete.clicked.connect(self.delete_item)
        tray_menu = QMenu()

        show_action = QAction("Развернуть", self)
        show_action.triggered.connect(self.show)
        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(qApp.quit)
        screenshot_action = QAction("Скриншот", self)
        screenshot_action.triggered.connect(self.screen_shot_part)

        tray_menu.addAction(show_action)
        tray_menu.addAction(screenshot_action)
        tray_menu.addSeparator()
        tray_menu.addAction(exit_action)
        self.tray_icon.setIcon(QIcon("icon.jpg"))
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def show_settings(self):
        self.settings_window.show()

    def closeEvent(self, e: QtGui.QCloseEvent):
        if self.settings_window.toTray:
            e.ignore()
            self.hide()
            self.tray_icon.showMessage("LanUI", "Программа свёрнута в трей", QSystemTrayIcon.Information, 500)

    def dragEnterEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.accept()
        else:
            event.ignore()

    def screen_shot(self):
        self.hide()
        im = pyscreenshot.grab()

        im.save("screenshot.png")
        self.show()

    def screen_shot_part(self):
        self.hide()
        im = pyscreenshot.grab()
        im.save("screenshot_temp.png")
        self.show()
        self.screen_shot_window = ScreenShotWindow()
        self.screen_shot_window.show()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            if f[-4:] == ".pdf":
                iteam = QtGui.QStandardItem(f)
                self.model.appendRow(iteam)

    def delete_item(self):
        for index in self.listView.selectedIndexes():
            self.model.removeRow(index.row())
        if len(self.listView.selectedIndexes()) > 0:
            i = self.model.index(0, 0)
            self.listView.setCurrentIndex(i)
            self.open_file_list()
        else:
            self.verticalLayout.removeWidget(self.pdfview)
            self.pdfview = QtWebEngineWidgets.QWebEngineView()
            self.verticalLayout.addWidget(self.pdfview)

    def open_file_list(self, index):
        self.fname = self.model.itemFromIndex(index).text()
        if len(self.fname) > 0:
            pdf = "file:///" + self.fname
            self.pdfview.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
            self.pdfview.load(QtCore.QUrl(pdf))
            self.lineEdit.textChanged[str].connect(self.on_line_edit)
            self.pageCount = len(fitz.open(self.fname))
            self.ConvertButton.clicked.connect(self.convert)

    def add_file(self):
        fname = QFileDialog.getOpenFileNames(self, 'Open file',
                                             'c:\\', "PDF (*.pdf)")

        if len(fname[0]) > 0:
            for name in fname[0]:
                item = QtGui.QStandardItem(name)
                self.model.appendRow(item)

    def on_line_edit(self):
        text = self.lineEdit.text()
        text = re.sub("\s", "", text)
        text = re.sub("--", "-", text)
        text = re.sub(",,", ",", text)
        text = re.sub(",-", "-", text)
        text = re.sub("-,", ",", text)

        if len(text) > 0 and not text[len(text) - 1].isdigit() and text[len(text) - 1] != ',' and text[
            len(text) - 1] != '-':
            text = text.replace(text[len(text) - 1], "")

        arr = re.split("[,-]", text)
        sep = re.split("[0-9]", text)
        while arr.__contains__(""):
            arr.remove("")
        while sep.__contains__(""):
            sep.remove("")
        while sep.__contains__("-"):
            sep.remove("-")

        i = 0

        self.chosenPages = []

        arr = re.split(",", text)
        while arr.__contains__(""):
            arr.remove("")
        for a in arr:
            a1 = re.split("-", a)
            while a1.__contains__(""):
                a1.remove("")
            if len(a1) == 1 and (int(a1[0]) > self.pageCount):
                arr.remove(a)
            elif len(a1) > 1 and (int(a1[0]) > self.pageCount or int(a1[1]) > self.pageCount):
                arr.remove(a)
            elif len(a1) > 1 and len(a1[1]) > 0 and int(a1[0]) < int(a1[1]):
                for j in range(int(a1[0]), int(a1[1]) + 1):
                    if not self.chosenPages.__contains__(j):
                        self.chosenPages.append(j)
            elif len(a1) > 1 and len(a1[1]) > 0 and int(a1[0]) >= int(a1[1]):
                for j in range(int(a1[1]), int(a1[0]) + 1):
                    if not self.chosenPages.__contains__(j):
                        self.chosenPages.append(j)
            else:
                if not self.chosenPages.__contains__(int(a1[0])):
                    self.chosenPages.append(int(a1[0]))
        text = ""
        for s in arr:
            if len(s) > 0:
                text += s
            if len(sep) >= i + 1:
                text += sep[i]
            i += 1

        self.lineEdit.setText(text)
        self.textBrowser.setText("")
        for choise in self.chosenPages:
            self.textBrowser.append(str(choise))

    def convert(self):
        folder = "result"
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

        if len(self.fname) > 2:
            pdf_document = fitz.open(self.fname)
            for current_page in self.chosenPages:
                for image in pdf_document.getPageImageList(current_page - 1):
                    xref = image[0]
                    try:
                        pix = fitz.Pixmap(pdf_document, xref)
                        if pix.n < 5:  # this is GRAY or RGB
                            pix.writePNG("result/%s.png" % (current_page - 1))
                        else:  # CMYK: convert to RGB first
                            pix1 = fitz.Pixmap(fitz.csRGB, pix)
                            pix1.writePNG("result/%s.png" % (current_page - 1))
                            pix1 = None
                        pix = None
                    except Exception as e:
                        QMessageBox.warning(self, "Ошибка",
                                            "Невозможно преобразовать страницу в картинку!\n" + e.args[0],
                                            QMessageBox.Ok)
                        return


class WinEventFilter(QAbstractNativeEventFilter):
    def __init__(self, keybinder):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, event_type, message):
        ret = self.keybinder.handler(event_type, message)
        return ret, 0


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    keybinder.init()
    keybinder.register_hotkey(window.winId(), "Ctrl+F1", window.screen_shot_part)
    keybinder.register_hotkey(window.winId(), "Ctrl+o", window.add_file)
    win_event_filter = WinEventFilter(keybinder)
    event_dispatcher = QAbstractEventDispatcher.instance()
    event_dispatcher.installNativeEventFilter(win_event_filter)
    window.show()
    app.exec_()
    keybinder.unregister_hotkey(window.winId(), "Ctrl+F1")
    keybinder.unregister_hotkey(window.winId(), "Ctrl+o")
