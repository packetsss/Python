import sys
import cv2
import qimage2ndarray
from copy import deepcopy
from scripts import Images
import numpy as np
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Filter(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui\\filter_frame.ui", self)
        self.frame = self.findChild(QFrame, "frame")
        self.contrast_btn = self.findChild(QPushButton, "contrast_btn")
        self.sharpen_btn = self.findChild(QPushButton, "sharpen_btn")
        self.cartoon_btn = self.findChild(QPushButton, "cartoon_btn")
        self.cartoon_btn1 = self.findChild(QPushButton, "cartoon_btn2")
        self.invert_btn = self.findChild(QPushButton, "invert_btn")

        self.y_btn = self.findChild(QPushButton, "y_btn")
        self.y_btn.setIcon(QIcon("icon/check.png"))
        self.y_btn.setStyleSheet("QPushButton{border: 0px solid;}")
        self.y_btn.setIconSize(QSize(60, 60))
        self.n_btn = self.findChild(QPushButton, "n_btn")
        self.n_btn.setIcon(QIcon("icon/cross.png"))
        self.n_btn.setStyleSheet("QPushButton{border: 0px solid;}")
        self.n_btn.setIconSize(QSize(60, 60))


class Adjust(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui\\adjust_frame.ui", self)
        self.frame = self.findChild(QFrame, "frame")
        self.crop_btn = self.findChild(QPushButton, "crop_btn")
        self.rotate_btn = self.findChild(QPushButton, "rotate_btn")
        self.brightness_btn = self.findChild(QPushButton, "brightness_btn")
        self.contrast_btn = self.findChild(QPushButton, "contrast_btn")
        self.saturation_btn = self.findChild(QPushButton, "saturation_btn")
        self.mask_btn = self.findChild(QPushButton, "mask_btn")

        self.y_btn = self.findChild(QPushButton, "y_btn")
        self.y_btn.setIcon(QIcon("icon/check.png"))
        self.y_btn.setStyleSheet("QPushButton{border: 0px solid;}")
        self.y_btn.setIconSize(QSize(60, 60))
        self.n_btn = self.findChild(QPushButton, "n_btn")
        self.n_btn.setIcon(QIcon("icon/cross.png"))
        self.n_btn.setStyleSheet("QPushButton{border: 0px solid;}")
        self.n_btn.setIconSize(QSize(60, 60))


class Crop(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui\\crop_btn.ui", self)

        self.frame = self.findChild(QFrame, "frame")
        self.y_btn = self.findChild(QPushButton, "y_btn")
        self.y_btn.setIcon(QIcon("icon/check.png"))
        self.y_btn.setStyleSheet("QPushButton{border: 0px solid;}")
        self.y_btn.setIconSize(QSize(70, 70))
        self.n_btn = self.findChild(QPushButton, "n_btn")
        self.n_btn.setIcon(QIcon("icon/cross.png"))
        self.n_btn.setStyleSheet("QPushButton{border: 0px solid;}")
        self.n_btn.setIconSize(QSize(70, 70))

        self.rotate = self.findChild(QPushButton, "rotate")
        self.rotate.setIcon(QIcon("icon/rotate90.png"))
        self.rotate.setStyleSheet("QPushButton{border: 0px solid;}")
        self.rotate.setIconSize(QSize(50, 50))
        self.rotatect = self.findChild(QPushButton, "rotatect")
        self.rotatect.setIcon(QIcon("icon/rotatect90.png"))
        self.rotatect.setStyleSheet("QPushButton{border: 0px solid;}")
        self.rotatect.setIconSize(QSize(50, 50))

        self.vflip = self.findChild(QPushButton, "vflip")
        self.vflip.setIcon(QIcon("icon/vflip.png"))
        self.vflip.setStyleSheet("QPushButton{border: 0px solid;}")
        self.vflip.setIconSize(QSize(50, 50))
        self.hflip = self.findChild(QPushButton, "hflip")
        self.hflip.setIcon(QIcon("icon/hflip.png"))
        self.hflip.setStyleSheet("QPushButton{border: 0px solid;}")
        self.hflip.setIconSize(QSize(50, 50))


class Brightness(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui\\brightness_btn.ui", self)

        self.frame = self.findChild(QFrame, "frame")
        self.vbox2 = self.findChild(QVBoxLayout, "vbox2")
        self.y_btn = self.findChild(QPushButton, "y_btn")
        self.y_btn.setIcon(QIcon("icon/check.png"))
        self.y_btn.setStyleSheet("QPushButton{border: 0px solid;}")
        self.y_btn.setIconSize(QSize(70, 70))
        self.n_btn = self.findChild(QPushButton, "n_btn")
        self.n_btn.setIcon(QIcon("icon/cross.png"))
        self.n_btn.setStyleSheet("QPushButton{border: 0px solid;}")
        self.n_btn.setIconSize(QSize(70, 70))

        self.pten = self.findChild(QPushButton, "pten")
        self.pten.setStyleSheet("QPushButton{border: 0px solid;}")
        self.mten = self.findChild(QPushButton, "mten")
        self.mten.setStyleSheet("QPushButton{border: 0px solid;}")

class Ai(QWidget):
    def __init__(self, img_class, update_img, base_frame, rb, vbox):
        super().__init__()
        uic.loadUi("ui\\ai_frame.ui", self)

        self.img_class, self.update_img, self.base_frame, self.rb, self.vbox = \
            img_class, update_img, base_frame, rb, vbox

        self.frame = self.findChild(QFrame, "frame")

        self.face_btn = self.findChild(QPushButton, "face_btn")
        self.face_btn.clicked.connect(lambda _: self.click_face())
        self.face_counter, self.face_cord = 0, None

        self.y_btn = self.findChild(QPushButton, "y_btn")
        self.y_btn.setIcon(QIcon("icon/check.png"))
        self.y_btn.setStyleSheet("QPushButton{border: 0px solid;}")
        self.y_btn.setIconSize(QSize(60, 60))
        self.n_btn = self.findChild(QPushButton, "n_btn")
        self.n_btn.setIcon(QIcon("icon/cross.png"))
        self.n_btn.setStyleSheet("QPushButton{border: 0px solid;}")
        self.n_btn.setIconSize(QSize(60, 60))

        self.y_btn.clicked.connect(self.click_y)
        self.n_btn.clicked.connect(self.click_n)

    def click_face(self):
        face_frame = Face(self.frame, self.img_class, self.update_img, self.base_frame, self.rb, self.vbox)
        self.frame.setParent(None)
        self.vbox.addWidget(face_frame.frame)

    def click_y(self):
        self.frame.setParent(None)
        self.img_class.img_copy = deepcopy(self.img_class.img)
        self.img_class.grand_img_copy = deepcopy(self.img_class.img)
        self.vbox.addWidget(self.base_frame)
        self.rb.close()

    def click_n(self):
        if not np.array_equal(self.img_class.grand_img_copy, self.img_class.img):
            msg = QMessageBox.question(self, "Cancel edits", "Confirm to discard all the changes?   ",
                                       QMessageBox.Yes | QMessageBox.No)
            if msg != QMessageBox.Yes:
                return False

        self.frame.setParent(None)
        self.img_class.grand_reset()
        self.update_img()
        self.vbox.addWidget(self.base_frame)
        self.rb.close()

class Face(QWidget):
    def __init__(self, ai_frame, img_class, update_img, base_frame, rb, vbox):
        super().__init__()
        uic.loadUi("ui\\face_btn.ui", self)
        self.img_class, self.update_img, self.base_frame, self.rb, self.vbox = \
            img_class, update_img, base_frame, rb, vbox
        self.frame, self.ai_frame = self.findChild(QFrame, "frame"), ai_frame

        self.next_btn = self.findChild(QPushButton, "next_btn")
        self.next_btn.clicked.connect(lambda _: self.click_next())
        self.face_counter, self.face_cord = 0, None

        self.y_btn = self.findChild(QPushButton, "y_btn")
        self.y_btn.setIcon(QIcon("icon/check.png"))
        self.y_btn.setStyleSheet("QPushButton{border: 0px solid;}")
        self.y_btn.setIconSize(QSize(60, 60))
        self.n_btn = self.findChild(QPushButton, "n_btn")
        self.n_btn.setIcon(QIcon("icon/cross.png"))
        self.n_btn.setStyleSheet("QPushButton{border: 0px solid;}")
        self.n_btn.setIconSize(QSize(60, 60))
        self.y_btn.clicked.connect(self.click_y)
        self.n_btn.clicked.connect(self.click_n)

    def click_next(self):
        if self.face_cord is None:
            self.face_cord = np.array(self.img_class.detect_face())

        if self.face_counter == len(self.face_cord):
            self.face_counter = 0

        face = self.face_cord[self.face_counter]
        self.rb.setGeometry(face[0], face[1], face[2], face[3])

        self.update_img()
        self.face_counter += 1

    def click_y(self):
        self.frame.setParent(None)
        self.img_class.img_copy = deepcopy(self.img_class.img)
        self.vbox.addWidget(self.ai_frame)

    def click_n(self):
        if not np.array_equal(self.img_class.grand_img_copy, self.img_class.img):
            msg = QMessageBox.question(self, "Cancel edits", "Confirm to discard all the changes?   ",
                                       QMessageBox.Yes | QMessageBox.No)
            if msg != QMessageBox.Yes:
                return False

        self.frame.setParent(None)
        self.img_class.reset()
        self.update_img()
        self.vbox.addWidget(self.ai_frame)

class ResizableRubberBand(QWidget):
    def __init__(self, parent=None, img_class=None, update=None, factorr=None):
        super(ResizableRubberBand, self).__init__(parent)
        self.img_class, self.update, self.factorr = img_class, update, factorr
        self.draggable, self.mousePressPos, self.mouseMovePos = True, None, None
        self.left, self.right, self.top, self.bottom = None, None, None, None
        self.borderRadius = 0

        self.setWindowFlags(Qt.SubWindow)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QSizeGrip(self), 0, Qt.AlignLeft | Qt.AlignTop)
        layout.addWidget(QSizeGrip(self), 0, Qt.AlignRight | Qt.AlignBottom)

        self._band = QRubberBand(QRubberBand.Rectangle, self)
        self._band.show()
        self.show()

    def update_dim(self):
        self.left, self.top = self.pos().x(), self.pos().y()
        self.right, self.bottom = self._band.width() + self.left, self._band.height() + self.top

    def resizeEvent(self, event):
        try:
            self.left, self.top = self.pos().x(), self.pos().y()
            self.right, self.bottom = self._band.width() + self.left, self._band.height() + self.top
        except:
            pass
        self._band.resize(self.size())

    def paintEvent(self, event):
        # Get current window size
        window_size = self.size()
        qp = QPainter(self)
        qp.drawRoundedRect(0, 0, window_size.width(), window_size.height(), self.borderRadius, self.borderRadius)

    def mousePressEvent(self, event):
        if self.draggable and event.button() == Qt.LeftButton:
            self.mousePressPos = event.globalPos()  # global
            self.mouseMovePos = event.globalPos() - self.pos()  # local

    def mouseMoveEvent(self, event):
        if self.draggable and event.buttons() & Qt.LeftButton:
            if self.right <= int(self.img_class.img.shape[1] * self.factorr) and self.bottom <= \
                    int(self.img_class.img.shape[0] * self.factorr) and self.left >= 0 and self.top >= 0:
                globalPos = event.globalPos()
                diff = globalPos - self.mouseMovePos
                self.move(diff)  # move window
                self.mouseMovePos = globalPos - self.pos()

            self.left, self.top = self.pos().x(), self.pos().y()
            self.right, self.bottom = self._band.width() + self.left, self._band.height() + self.top

    def mouseReleaseEvent(self, event):
        if self.mousePressPos is not None:
            if event.button() == Qt.LeftButton:
                self.mousePressPos = None

        if self.left < 0:
            self.left = 0
            self.move(0, self.top)
        if self.right > int(self.img_class.img.shape[1] * self.factorr):
            self.left = int(self.img_class.img.shape[1] * self.factorr) - self._band.width()
            self.move(self.left, self.top)
        if self.bottom > int(self.img_class.img.shape[0] * self.factorr):
            self.top = int(self.img_class.img.shape[0] * self.factorr) - self._band.height()
            self.move(self.left, self.top)
        if self.top < 0:
            self.top = 0
            self.move(self.left, 0)