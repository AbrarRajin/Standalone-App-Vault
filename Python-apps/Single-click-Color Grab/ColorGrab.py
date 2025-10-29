#!/usr/bin/env python3
"""
Minimal One-Click Color Picker
------------------------------
Workflow:
1) Run the app.
2) Move the crosshair over any app/window.
3) Left-click once → copies HEX to clipboard and exits.

Controls:
- Left-click: copy HEX & quit
- Esc: quit (no copy)

Requires: PyQt6  (pip install PyQt6)
"""

import sys
from typing import Tuple
from dataclasses import dataclass

from PyQt6.QtCore import Qt, QTimer, QPoint, QRect
from PyQt6.QtGui import QCursor, QColor, QGuiApplication, QPainter, QPen, QBrush, QFont
from PyQt6.QtWidgets import QApplication, QWidget

@dataclass
class ColorInfo:
    hex: str

def color_at(pos: QPoint) -> QColor:
    screen = QGuiApplication.primaryScreen()
    for s in QGuiApplication.screens():
        if s.geometry().contains(pos):
            screen = s
            break
    img = screen.grabWindow(0, pos.x(), pos.y(), 1, 1).toImage()
    if img.isNull():
        return QColor(0, 0, 0)
    return img.pixelColor(0, 0)

def to_hex(c: QColor) -> str:
    return c.name(QColor.NameFormat.HexRgb).upper()

class Overlay(QWidget):
    def __init__(self):
        super().__init__(None, Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        geo = QGuiApplication.primaryScreen().virtualGeometry()
        self.setGeometry(geo)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)

        self.cursor_pos = QCursor.pos()
        self.current_color = color_at(self.cursor_pos)
        self.current_hex = to_hex(self.current_color)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(12)

        self.showFullScreen()

    # --- Events ---
    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Escape:
            QApplication.instance().quit()

    def mouseMoveEvent(self, e):
        self.cursor_pos = e.globalPosition().toPoint()
        e.accept()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            QGuiApplication.clipboard().setText(self.current_hex)
            QTimer.singleShot(60, QApplication.instance().quit)
        e.accept()

    def tick(self):
        self.cursor_pos = QCursor.pos()
        self.current_color = color_at(self.cursor_pos)
        self.current_hex = to_hex(self.current_color)
        self.update()

    # --- Drawing ---
    def _preview_geometry(self, pos: QPoint) -> QRect:
        radius = 16
        offset = QPoint(26, 26)
        center = pos + offset
        return QRect(center.x() - radius, center.y() - radius, radius * 2, radius * 2)

    def paintEvent(self, _event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        pos = self.cursor_pos
        gap, arm = 4, 14
        ring_outer, ring_thickness = 10, 2

        # subtle dim for focus
        p.fillRect(self.rect(), QColor(0, 0, 0, 30))

        # shadow crosshair
        pen_shadow = QPen(QColor(0, 0, 0, 130), 3.5)
        p.setPen(pen_shadow)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p.drawLine(pos + QPoint(-(gap + arm) + dx, dy), pos + QPoint(-gap + dx, dy))
            p.drawLine(pos + QPoint(gap + dx, dy), pos + QPoint(gap + arm + dx, dy))
            p.drawLine(pos + QPoint(dx, -(gap + arm) + dy), pos + QPoint(dx, -gap + dy))
            p.drawLine(pos + QPoint(dx, gap + dy), pos + QPoint(dx, gap + arm + dy))

        # white crosshair
        p.setPen(QPen(QColor(255, 255, 255, 220), 1.5))
        p.drawLine(pos + QPoint(-(gap + arm), 0), pos + QPoint(-gap, 0))
        p.drawLine(pos + QPoint(gap, 0), pos + QPoint(gap + arm, 0))
        p.drawLine(pos + QPoint(0, -(gap + arm)), pos + QPoint(0, -gap))
        p.drawLine(pos + QPoint(0, gap), pos + QPoint(0, gap + arm))

        # target ring (transparent center = "hole")
        p.setPen(QPen(QColor(0, 0, 0, 160), ring_thickness + 2))
        p.drawEllipse(pos, ring_outer, ring_outer)
        p.setPen(QPen(QColor(255, 255, 255, 230), ring_thickness))
        p.drawEllipse(pos, ring_outer, ring_outer)

        # preview circle filled with current color
        preview = self._preview_geometry(pos)
        p.setPen(QPen(QColor(0, 0, 0, 160), 3))
        p.setBrush(QBrush(self.current_color))
        p.drawEllipse(preview)
        p.setPen(QPen(QColor(255, 255, 255, 230), 1.2))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawEllipse(preview.adjusted(2, 2, -2, -2))

        # small hex label
        p.setPen(QColor(255, 255, 255))
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        p.setFont(font)
        text = self.current_hex
        metrics = p.fontMetrics()
        pad = 6
        w = metrics.horizontalAdvance(text) + pad * 2
        h = metrics.height() + pad * 2
        tl = preview.bottomRight() + QPoint(10, 6)
        bg = QRect(tl.x(), tl.y(), w, h)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(0, 0, 0, 180))
        p.drawRoundedRect(bg, 6, 6)
        p.setPen(QColor(255, 255, 255))
        p.drawText(bg.adjusted(pad, pad, -pad, -pad), Qt.AlignmentFlag.AlignVCenter, text)

        p.end()

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("One-Click Color Picker")
    app.setQuitOnLastWindowClosed(True)
    _ = Overlay()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
