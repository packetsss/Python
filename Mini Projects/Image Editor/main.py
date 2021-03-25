from widgets import *


class Start(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/startup.ui", self)
        self.setWindowIcon(QIcon("icon/icon.png"))

        self.button = self.findChild(QPushButton, "browse")
        self.button.clicked.connect(self.on_click)
        self.files, self.main_window = None, None

    def on_click(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Choose Image File", "",
                                                "Image Files (*.jpg *.png *.jpeg *.ico);;All Files (*)")
        if files:
            self.files = files
            self.close()
            self.main_window = Main(self.files) 
            self.main_window.show()


class Main(QWidget):
    def __init__(self, files):
        # initialize
        super().__init__()
        uic.loadUi("ui\\main.ui", self)
        self.setWindowIcon(QIcon("icon/icon.png"))
        self.move(120, 100)
        self.img_list, self.rb = [], None
        for f in files:
            self.img_list.append(Images(f))
        self.img_id = 0
        self.img_class = self.img_list[self.img_id]
        self.img = QPixmap(qimage2ndarray.array2qimage(cv2.cvtColor(self.img_class.img, cv2.COLOR_BGR2RGB)))

        # find widgets and connect them
        self.vbox = self.findChild(QVBoxLayout, "vbox")
        self.vbox1 = self.findChild(QVBoxLayout, "vbox1")
        self.base_frame = self.findChild(QFrame, "base_frame")
        self.filter_btn = self.findChild(QPushButton, "filter_btn")
        self.filter_btn.clicked.connect(self.filter_frame)
        self.adjust_btn = self.findChild(QPushButton, "adjust_btn")
        self.adjust_btn.clicked.connect(self.adjust_frame)
        self.ai_btn = self.findChild(QPushButton, "ai_btn")
        self.ai_btn.clicked.connect(self.ai_frame)
        self.save_btn = self.findChild(QPushButton, "save_btn")
        self.save_btn.clicked.connect(self.click_save)
        self.slider = self.findChild(QSlider, "slider")
        self.slider.setParent(None)

        # display img
        self.gv = self.findChild(QGraphicsView, "gv")
        self.scene = QGraphicsScene()
        self.scene_img = self.scene.addPixmap(self.img)
        self.gv.setScene(self.scene)

        # zoom in
        self.zoom_moment = False
        self._zoom = 0

        # misc
        self.rotate_value, self.brightness_value, self.contrast_value, self.saturation_value = 0, 0, 1, 0
        self.flip = [False, False]
        self.factorr = 1

    def update_img(self, movable=False):
        self.img = QPixmap(qimage2ndarray.array2qimage(cv2.cvtColor(self.img_class.img, cv2.COLOR_BGR2RGB)))
        self.scene.removeItem(self.scene_img)
        self.scene_img = self.scene.addPixmap(self.img)
        if movable:
            self.scene_img.setFlag(QGraphicsItem.ItemIsMovable)
        else:
            self.fitInView()

    def filter_frame(self):
        def click_contrast():
            self.img_class.auto_contrast()
            self.update_img()
            filter_frame.contrast_btn.clicked.disconnect()

        def click_sharpen():
            self.img_class.auto_sharpen()
            self.update_img()
            filter_frame.sharpen_btn.clicked.disconnect()

        def click_cartoon():
            self.img_class.auto_cartoon()
            self.update_img()
            filter_frame.cartoon_btn.clicked.disconnect()

        def click_cartoon1():
            self.img_class.auto_cartoon(1)
            self.update_img()
            filter_frame.cartoon_btn1.clicked.disconnect()

        def click_invert():
            self.img_class.auto_invert()
            self.update_img()
            filter_frame.invert_btn.clicked.disconnect()

        def click_bypass():
            self.img_class.bypass_censorship()
            self.update_img()
            filter_frame.bypass_btn.clicked.disconnect()

        def click_y():
            filter_frame.frame.setParent(None)
            self.img_class.img_copy = deepcopy(self.img_class.img)
            self.img_class.grand_img_copy = deepcopy(self.img_class.img)
            self.vbox.addWidget(self.base_frame)

        def click_n():
            if not np.array_equal(self.img_class.grand_img_copy, self.img_class.img):
                msg = QMessageBox.question(self, "Cancel edits", "Confirm to discard all the changes?   ",
                                           QMessageBox.Yes | QMessageBox.No)
                if msg != QMessageBox.Yes:
                    return False

            filter_frame.frame.setParent(None)
            self.img_class.grand_reset()
            self.update_img()
            self.vbox.addWidget(self.base_frame)

        filter_frame = Filter()
        filter_frame.y_btn.clicked.connect(click_y)
        filter_frame.n_btn.clicked.connect(click_n)
        filter_frame.contrast_btn.clicked.connect(click_contrast)
        filter_frame.sharpen_btn.clicked.connect(click_sharpen)
        filter_frame.cartoon_btn.clicked.connect(click_cartoon)
        filter_frame.cartoon_btn1.clicked.connect(click_cartoon1)
        filter_frame.invert_btn.clicked.connect(click_invert)
        filter_frame.bypass_btn.clicked.connect(click_bypass)

        self.base_frame.setParent(None)
        self.vbox.addWidget(filter_frame.frame)

    def adjust_frame(self):
        def click_crop(rotate=False):
            def click_y1():
                self.rb.update_dim()
                if rotate:
                    self.img_class.rotate_img(self.rotate_value, crop=True, flip=self.flip)
                    self.img_class.crop_img(int(self.rb.top * 2 / self.factorr),
                                            int(self.rb.bottom * 2 / self.factorr),
                                            int(self.rb.left * 2 / self.factorr),
                                            int(self.rb.right * 2 / self.factorr))
                else:
                    self.img_class.reset(self.flip)
                    self.img_class.crop_img(int(self.rb.top / self.factorr), int(self.rb.bottom / self.factorr),
                                            int(self.rb.left // self.factorr), int(self.rb.right // self.factorr))

                self.update_img()
                self.zoom_moment = False

                self.img_class.img_copy = deepcopy(self.img_class.img)
                self.slider.setParent(None)
                self.slider.valueChanged.disconnect()
                crop_frame.frame.setParent(None)
                self.vbox.addWidget(adjust_frame.frame)
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
                self.vbox.addWidget(adjust_frame.frame)
                self.rb.close()

            def change_slide():
                self.rotate_value = self.slider.value()
                self.slider.setValue(self.rotate_value)

                self.img_class.rotate_img(self.rotate_value)

                self.rb.setGeometry(int(self.img_class.left * self.factorr), int(self.img_class.top * self.factorr),
                                    int((self.img_class.right - self.img_class.left) * self.factorr),
                                    int((self.img_class.bottom - self.img_class.top) * self.factorr))
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

            adjust_frame.frame.setParent(None)
            self.vbox.addWidget(crop_frame.frame)

            self.rb = ResizableRubberBand(self)
            self.rb.setGeometry(0, 0, self.img_class.img.shape[1], self.img_class.img.shape[0])
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
                self.rb.setGeometry(0, 0, self.img_class.img.shape[1], self.img_class.img.shape[0])
                self.update_img(True)

            img_copy = deepcopy(self.img_class.img)

        def click_brightness(mode=0):
            def click_y1():
                self.img_class.img_copy = deepcopy(self.img_class.img)
                if mode != 3:
                    self.slider.setParent(None)
                    self.slider.valueChanged.disconnect()
                brightness_frame.frame.setParent(None)
                self.vbox.addWidget(adjust_frame.frame)

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
                self.vbox.addWidget(adjust_frame.frame)

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

            adjust_frame.frame.setParent(None)
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

        def click_y():
            self.start_detect = False
            adjust_frame.frame.setParent(None)
            self.img_class.img_copy = deepcopy(self.img_class.img)
            self.img_class.grand_img_copy = deepcopy(self.img_class.img)
            self.vbox.addWidget(self.base_frame)

        def click_n():
            if not np.array_equal(self.img_class.grand_img_copy, self.img_class.img):
                msg = QMessageBox.question(self, "Cancel edits", "Confirm to discard all the changes?   ",
                                           QMessageBox.Yes | QMessageBox.No)
                if msg != QMessageBox.Yes:
                    return False

            self.start_detect = False
            adjust_frame.frame.setParent(None)
            self.img_class.grand_reset()
            self.update_img()
            self.vbox.addWidget(self.base_frame)

        adjust_frame = Adjust()
        adjust_frame.y_btn.clicked.connect(click_y)
        adjust_frame.n_btn.clicked.connect(click_n)
        adjust_frame.crop_btn.clicked.connect(click_crop)
        adjust_frame.rotate_btn.clicked.connect(lambda _: click_crop(rotate=True))
        adjust_frame.brightness_btn.clicked.connect(click_brightness)
        adjust_frame.contrast_btn.clicked.connect(lambda _: click_brightness(mode=1))
        adjust_frame.saturation_btn.clicked.connect(lambda _: click_brightness(mode=2))
        adjust_frame.mask_btn.clicked.connect(lambda _: click_brightness(mode=3))

        self.base_frame.setParent(None)
        self.vbox.addWidget(adjust_frame.frame)

    def ai_frame(self):
        self.rb = ResizableRubberBand(self)
        ai_frame = Ai(self)
        self.base_frame.setParent(None)
        self.vbox.addWidget(ai_frame.frame)

    def click_save(self):
        try:
            file, _ = QFileDialog.getSaveFileName(self, 'Save File', f"{self.img_class.img_name}."
                                                                     f"{self.img_class.img_format}",
                                                  "Image Files (*.jpg *.png *.jpeg *.ico);;All Files (*)")
            self.img_class.save_img(file)
        except Exception:
            pass

    def wheelEvent(self, event):
        if self.zoom_moment:
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.gv.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    def fitInView(self):
        rect = QRectF(self.img.rect())
        if not rect.isNull():
            self.gv.setSceneRect(rect)

            unity = self.gv.transform().mapRect(QRectF(0, 0, 1, 1))
            self.gv.scale(1 / unity.width(), 1 / unity.height())
            view_rect = self.gv.viewport().rect()
            scene_rect = self.gv.transform().mapRect(rect)
            factor = min(view_rect.width() / scene_rect.width(),
                         view_rect.height() / scene_rect.height())
            self.gv.scale(factor, factor)
            self._zoom = 0
            self.factorr = factor


def main():
    app = QApplication(sys.argv)
    window = Start()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
