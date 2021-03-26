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
    def __init__(self, main):
        super().__init__()
        uic.loadUi("ui\\filter_frame.ui", self)
        self.img_class, self.update_img, self.base_frame, self.vbox = \
            main.img_class, main.update_img, main.base_frame, main.vbox

        self.frame = self.findChild(QFrame, "frame")
        self.contrast_btn = self.findChild(QPushButton, "contrast_btn")
        self.sharpen_btn = self.findChild(QPushButton, "sharpen_btn")
        self.cartoon_btn = self.findChild(QPushButton, "cartoon_btn")
        self.cartoon_btn1 = self.findChild(QPushButton, "cartoon_btn2")
        self.invert_btn = self.findChild(QPushButton, "invert_btn")
        self.bypass_btn = self.findChild(QPushButton, "bypass_btn")

        self.y_btn = self.findChild(QPushButton, "y_btn")
        self.y_btn.setIcon(QIcon("icon/check.png"))
        self.y_btn.setStyleSheet("QPushButton{border: 0px solid;}")
        self.y_btn.setIconSize(QSize(60, 60))
        self.n_btn = self.findChild(QPushButton, "n_btn")
        self.n_btn.setIcon(QIcon("icon/cross.png"))
        self.n_btn.setStyleSheet("QPushButton{border: 0px solid;}")
        self.n_btn.setIconSize(QSize(60, 60))

        self.y_btn.clicked.connect(lambda _: self.click_y())
        self.n_btn.clicked.connect(lambda _: self.click_n())
        self.contrast_btn.clicked.connect(lambda _: self.click_contrast())
        self.sharpen_btn.clicked.connect(lambda _: self.click_sharpen())
        self.cartoon_btn.clicked.connect(lambda _: self.click_cartoon())
        self.cartoon_btn1.clicked.connect(lambda _: self.click_cartoon1())
        self.invert_btn.clicked.connect(lambda _: self.click_invert())
        self.bypass_btn.clicked.connect(lambda _: self.click_bypass())

    def click_contrast(self):
        self.img_class.auto_contrast()
        self.update_img()
        self.contrast_btn.clicked.disconnect()

    def click_sharpen(self):
        self.img_class.auto_sharpen()
        self.update_img()
        self.sharpen_btn.clicked.disconnect()

    def click_cartoon(self):
        self.img_class.auto_cartoon()
        self.update_img()
        self.cartoon_btn.clicked.disconnect()

    def click_cartoon1(self):
        self.img_class.auto_cartoon(1)
        self.update_img()
        self.cartoon_btn1.clicked.disconnect()

    def click_invert(self):
        self.img_class.auto_invert()
        self.update_img()
        self.invert_btn.clicked.disconnect()

    def click_bypass(self):
        self.img_class.bypass_censorship()
        self.update_img()
        self.bypass_btn.clicked.disconnect()

    def click_y(self):
        self.frame.setParent(None)
        self.img_class.img_copy = deepcopy(self.img_class.img)
        self.img_class.grand_img_copy = deepcopy(self.img_class.img)
        self.vbox.addWidget(self.base_frame)

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


class Adjust(QWidget):
    def __init__(self, main):
        super().__init__()
        uic.loadUi("ui\\adjust_frame.ui", self)
        self.get_zoom_factor = main.get_zoom_factor

        self.img_class, self.update_img, self.base_frame = main.img_class, main.update_img, main.base_frame
        self.rb, self.vbox, self.flip, self.zoom_factor = main.rb, main.vbox, main.flip, main.zoom_factor
        self.zoom_moment, self.slider, self.gv, self.vbox1 = main.zoom_moment, main.slider, main.gv, main.vbox1
        self.start_detect = False

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

        self.y_btn.clicked.connect(lambda _: self.click_y())
        self.n_btn.clicked.connect(lambda _: self.click_n())
        self.crop_btn.clicked.connect(lambda _: self.click_crop())
        self.rotate_btn.clicked.connect(lambda _: self.click_crop(rotate=True))
        self.brightness_btn.clicked.connect(lambda _: self.click_brightness())
        self.contrast_btn.clicked.connect(lambda _: self.click_brightness(mode=1))
        self.saturation_btn.clicked.connect(lambda _: self.click_brightness(mode=2))
        self.mask_btn.clicked.connect(lambda _: self.click_brightness(mode=3))

    def click_crop(self, rotate=False):
        def click_y1():
            self.rb.update_dim()
            if rotate:
                self.img_class.rotate_img(self.rotate_value, crop=True, flip=self.flip)
                self.img_class.crop_img(int(self.rb.top * 2 / self.zoom_factor),
                                        int(self.rb.bottom * 2 / self.zoom_factor),
                                        int(self.rb.left * 2 / self.zoom_factor),
                                        int(self.rb.right * 2 / self.zoom_factor))
            else:
                self.img_class.reset(self.flip)
                self.img_class.crop_img(int(self.rb.top / self.zoom_factor), int(self.rb.bottom / self.zoom_factor),
                                        int(self.rb.left // self.zoom_factor), int(self.rb.right // self.zoom_factor))

            self.update_img()
            self.zoom_moment = False

            self.img_class.img_copy = deepcopy(self.img_class.img)
            self.slider.setParent(None)
            self.slider.valueChanged.disconnect()
            crop_frame.frame.setParent(None)
            self.vbox.addWidget(self.frame)
            self.rb.close()

        def click_n1():
            if not np.array_equal(img_copy, self.img_class.img):
                msg = QMessageBox.question(self, "Cancel edits", "Confirm to discard all the changes?   ",
                                           QMessageBox.Yes | QMessageBox.No)
                if msg != QMessageBox.Yes:
                    return False

            self.img_class.reset()
            self.update_img()
            self.zoom_moment = False

            self.slider.setParent(None)
            self.slider.valueChanged.disconnect()
            crop_frame.frame.setParent(None)
            self.vbox.addWidget(self.frame)
            self.rb.close()

        def change_slide():
            self.rotate_value = self.slider.value()
            self.slider.setValue(self.rotate_value)

            self.img_class.rotate_img(self.rotate_value)

            self.rb.setGeometry(int(self.img_class.left * self.zoom_factor), int(self.img_class.top * self.zoom_factor),
                                int((self.img_class.right - self.img_class.left) * self.zoom_factor),
                                int((self.img_class.bottom - self.img_class.top) * self.zoom_factor))

            self.rb.update_dim()
            self.update_img(True)

        def add_90():
            if self.rotate_value <= 270:
                self.rotate_value += 90
            else:
                self.rotate_value = 360
            self.slider.setValue(self.rotate_value)
            change_slide()

        def subtract_90():
            if self.rotate_value >= 90:
                self.rotate_value -= 90
            else:
                self.rotate_value = 0
            self.slider.setValue(self.rotate_value)
            change_slide()

        def vertical_flip():
            nonlocal vflip_ct
            self.img_class.img = cv2.flip(self.img_class.img, 0)
            if rotate:
                self.update_img(True)
            else:
                self.update_img()
            vflip_ct += 1
            self.flip[0] = vflip_ct % 2 == 1

        def horizontal_flip():
            nonlocal hflip_ct
            self.img_class.img = cv2.flip(self.img_class.img, 1)
            if rotate:
                self.update_img(True)
            else:
                self.update_img()
            hflip_ct += 1
            self.flip[1] = hflip_ct % 2 == 1

        crop_frame = Crop()
        crop_frame.n_btn.clicked.connect(click_n1)
        crop_frame.y_btn.clicked.connect(click_y1)
        crop_frame.rotate.clicked.connect(add_90)
        crop_frame.rotatect.clicked.connect(subtract_90)
        crop_frame.vflip.clicked.connect(vertical_flip)
        crop_frame.hflip.clicked.connect(horizontal_flip)
        self.flip = [False, False]
        vflip_ct = 2
        hflip_ct = 2

        self.frame.setParent(None)
        self.vbox.addWidget(crop_frame.frame)
        self.zoom_factor = self.get_zoom_factor()

        self.rb = ResizableRubberBand(self)
        self.rb.setGeometry(0, 0, self.img_class.img.shape[1] * self.zoom_factor,
                            self.img_class.img.shape[0] * self.zoom_factor)
        self.img_class.change_b_c(beta=-40)
        self.slider.valueChanged.connect(change_slide)


        if not rotate:
            self.update_img()
            crop_frame.rotate.setParent(None)
            crop_frame.rotatect.setParent(None)
        else:
            self.vbox1.insertWidget(1, self.slider)
            self.slider.setRange(0, 360)
            self.slider.setValue(0)
            self.zoom_moment = True
            self.img_class.rotate_img(0)
            self.rb.setGeometry(0, 0, int(self.img_class.img.shape[1] * self.zoom_factor),
                                int(self.img_class.img.shape[0] * self.zoom_factor))
            self.update_img(True)

        img_copy = deepcopy(self.img_class.img)

    def click_brightness(self, mode=0):
        def click_y1():
            self.img_class.img_copy = deepcopy(self.img_class.img)
            if mode != 3:
                self.slider.setParent(None)
                self.slider.valueChanged.disconnect()
            brightness_frame.frame.setParent(None)
            self.vbox.addWidget(self.frame)

        def click_n1():
            if not np.array_equal(self.img_class.img_copy, self.img_class.img):
                msg = QMessageBox.question(self, "Cancel edits", "Confirm to discard all the changes?   ",
                                           QMessageBox.Yes | QMessageBox.No)
                if msg != QMessageBox.Yes:
                    return False
            self.img_class.reset()
            self.update_img()

            if mode != 3:
                self.slider.setParent(None)
                self.slider.valueChanged.disconnect()
            brightness_frame.frame.setParent(None)
            self.vbox.addWidget(self.frame)

        def change_slide():
            self.brightness_value = self.slider.value()
            self.img_class.reset()
            self.img_class.change_b_c(beta=self.brightness_value)
            self.update_img()

        def change_slide_contr():
            self.contrast_value = self.slider.value() / 100
            self.img_class.reset()
            self.img_class.change_b_c(alpha=self.contrast_value)
            self.update_img()

        def change_slide_sat():
            self.saturation_value = self.slider.value() / 250
            self.img_class.reset()
            self.img_class.change_b_c(alpha=self.saturation_value)
            self.update_img()

        def color_dialog():
            color = QColorDialog.getColor()
            self.img_class.remove_color(color.name())
            self.update_img()

        brightness_frame = Brightness()
        brightness_frame.y_btn.clicked.connect(click_y1)
        brightness_frame.n_btn.clicked.connect(click_n1)

        self.frame.setParent(None)
        self.vbox.addWidget(brightness_frame.frame)

        if mode == 1:
            self.vbox1.insertWidget(1, self.slider)
            self.slider.setRange(0, 300)
            self.slider.setValue(100)
            self.slider.valueChanged.connect(change_slide_contr)
        elif mode == 2:
            self.vbox1.insertWidget(1, self.slider)
            self.slider.setRange(0, 1000)
            self.slider.setValue(250)
            self.slider.valueChanged.connect(change_slide_sat)
        elif mode == 3:
            btnn = QPushButton("Select color", brightness_frame)
            btnn.setFont(QFont("Neue Haas Grotesk Text Pro Medi", 14))
            btnn.setStyleSheet("QPushButton{border: 0px solid;}")
            btnn.setMaximumHeight(50)
            btnn.clicked.connect(color_dialog)
            brightness_frame.vbox2.insertWidget(0, btnn)
        else:
            self.vbox1.insertWidget(1, self.slider)
            self.slider.setRange(-120, 160)
            self.slider.setValue(0)
            self.slider.valueChanged.connect(change_slide)

    def click_y(self):
        self.start_detect = False
        self.frame.setParent(None)
        self.img_class.img_copy = deepcopy(self.img_class.img)
        self.img_class.grand_img_copy = deepcopy(self.img_class.img)
        self.vbox.addWidget(self.base_frame)

    def click_n(self):
        if not np.array_equal(self.img_class.grand_img_copy, self.img_class.img):
            msg = QMessageBox.question(self, "Cancel edits", "Confirm to discard all the changes?   ",
                                       QMessageBox.Yes | QMessageBox.No)
            if msg != QMessageBox.Yes:
                return False

        self.start_detect = False
        self.frame.setParent(None)
        self.img_class.grand_reset()
        self.update_img()
        self.vbox.addWidget(self.base_frame)


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
    def __init__(self, main):
        super().__init__()
        uic.loadUi("ui\\ai_frame.ui", self)

        self.get_zoom_factor = main.get_zoom_factor
        self.img_class, self.update_img, self.base_frame, self.rb, self.vbox, self.zoom_factor = \
            main.img_class, main.update_img, main.base_frame, main.rb, main.vbox, main.zoom_factor

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
        face_frame = Face(self)
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
    def __init__(self, ai_class):
        super().__init__()
        uic.loadUi("ui\\face_btn.ui", self)
        self.img_class, self.update_img, self.base_frame, self.rb, self.vbox = \
            ai_class.img_class, ai_class.update_img, ai_class.base_frame, ai_class.rb, ai_class.vbox
        self.frame, self.ai_frame = self.findChild(QFrame, "frame"), ai_class.frame

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
    def __init__(self, main):
        super(ResizableRubberBand, self).__init__(main.gv)
        self.get_zoom_factor = main.get_zoom_factor

        self.img_class, self.update, self.zoom_factor = main.img_class, main.update, main.zoom_factor
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
        self.zoom_factor = self.get_zoom_factor()
        if self.draggable and event.button() == Qt.LeftButton:
            self.mousePressPos = event.globalPos()  # global
            self.mouseMovePos = event.globalPos() - self.pos()  # local

    def mouseMoveEvent(self, event):
        if self.draggable and event.buttons() & Qt.LeftButton:
            if self.right <= int(self.img_class.img.shape[1] * self.zoom_factor) and self.bottom <= \
                    int(self.img_class.img.shape[0] * self.zoom_factor) and self.left >= 0 and self.top >= 0:
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
        if self.right > int(self.img_class.img.shape[1] * self.zoom_factor):
            self.left = int(self.img_class.img.shape[1] * self.zoom_factor) - self._band.width()
            self.move(self.left, self.top)
        if self.bottom > int(self.img_class.img.shape[0] * self.zoom_factor):
            self.top = int(self.img_class.img.shape[0] * self.zoom_factor) - self._band.height()
            self.move(self.left, self.top)
        if self.top < 0:
            self.top = 0
            self.move(self.left, 0)

