from PyQt5.QtCore import Qt, QRect, QPoint, QVariantAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QCheckBox

class PyToggle(QCheckBox):
    def __init__(
            self,
            width=60,
            bg_color='#777',
            circle_color='#DDD',
            active_color='#F2662A',
            animation_curve=QEasingCurve.OutBounce
    ):
        super().__init__()

        self.setFixedSize(width, 28)
        self.setCursor(Qt.PointingHandCursor)

        self._bg_color = bg_color
        self._circle_color = circle_color
        self._active_color = active_color

        self._circle_position = 3
        self.animation = QVariantAnimation(self, startValue=3, endValue=self.width() - 26, valueChanged=self.on_animation_value_changed)
        self.animation.setEasingCurve(animation_curve)
        self.animation.setDuration(500)

        # self.stateChanged.connect(self.debug)

        self.stateChanged.connect(self.start_transition)

    # def debug(self):
    #     print(f"Status: {self.isChecked()}")

    def circle_position(self):
        return self._circle_position

    def setCirclePosition(self, value):
        self._circle_position = value
        self.update()

    circlePosition = pyqtProperty(float, circle_position, setCirclePosition)

    def start_transition(self, value):
        self.animation.stop()
        if value:
            self.animation.setDirection(QVariantAnimation.Forward)
        else:
            self.animation.setDirection(QVariantAnimation.Backward)
        self.animation.start()

    def on_animation_value_changed(self, value):
        self.setCirclePosition(value)

    def hitButton(self, pos):
        return QRect(self.contentsRect()).contains(QPoint(pos))

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.setPen(Qt.NoPen)

        rect = QRect(0, 0, self.width(), self.height())

        if not self.isChecked():
            p.setBrush(QColor(self._bg_color))
            p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2)

            p.setBrush(QColor(self._circle_color))
            p.drawEllipse(self._circle_position, 3, 22, 22)
        else:
            p.setBrush(QColor(self._active_color))
            p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2)

            p.setBrush(QColor(self._circle_color))
            p.drawEllipse(self._circle_position, 3, 22, 22)