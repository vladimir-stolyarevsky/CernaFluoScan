from PyQt5.QtWidgets import (QWidget, QTabBar, QSizePolicy)
from PyQt5.QtCore import Qt, QRectF, QLineF, QPointF, QSize

import pyqtgraph as pg


class VTabBar(QTabBar):
    def __init__(self, parent=None):
        QTabBar.__init__(self, parent)

    def tabSizeHint(self, index):
        size = QTabBar.tabSizeHint(self, index)
        h = int(self.height()/2)
        return QSize(size.width(), h)


class PgGraphicsView(pg.GraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent, useOpenGL=False, background=pg.mkColor('#29353D'))

        pg.setConfigOptions(imageAxisOrder='row-major')

        self.vb = pg.ViewBox()
        self.setCentralItem(self.vb)

        self.image = pg.ImageItem()
        self.vb.addItem(self.image)

        self.init_ui()

    def init_ui(self):
        self.vb.setMenuEnabled(False)
        self.vb.setAspectLocked()
        self.vb.enableAutoRange()

        size_policy = QSizePolicy()
        size_policy.setHorizontalPolicy(QSizePolicy.Expanding)
        size_policy.setVerticalPolicy(QSizePolicy.Expanding)
        self.setSizePolicy(size_policy)
        self.setMinimumSize(512, 512)


class CrossCursor(pg.InfiniteLine):
    def __init__(self, size=30, pos=None, pen=None, bounds=None, label=None, labelOpts=None, name=None):
        pg.InfiniteLine.__init__(self, pos, 0, pen, False, bounds, None, label, labelOpts, name)

        # self.vb = vb
        self.cursorSize = size

    def boundingRect(self):
        if self._boundingRect is None:
            # br = UIGraphicsItem.boundingRect(self)
            br = self.viewRect()
            if br is None:
                return QRectF()

            # get vertical pixel length
            self.pxv = self.pixelLength(direction=pg.Point(0, 1), ortho=False)
            if self.pxv is None:
                self.pxv = 0
            # get horizontal pixel length
            self.pxh = self.pixelLength(direction=pg.Point(1, 0), ortho=False)
            if self.pxh is None:
                self.pxh = 0

            br = br.normalized()
            self._boundingRect = br

        return self._boundingRect

    def paint(self, p, *args):
        p.setPen(self.currentPen)

        x = self.getXPos()
        y = self.getYPos()
        # print((x, y))

        h = self.cursorSize * self.pxv
        w = self.cursorSize * self.pxh

        p.drawLine(QPointF(x, y - h), QPointF(x, y + h))
        p.drawLine(QPointF(x - w, y), QPointF(x + w, y))