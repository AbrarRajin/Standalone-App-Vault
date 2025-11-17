#!/usr/bin/env python3
"""
Color Picker with UI (Keyboard-based)
--------------------------------------
Workflow:
1) Click "Pick Color" button
2) Move the crosshair over any color
3) Press SPACE or ENTER to pick → returns to UI with HEX code

Controls in picker mode:
- SPACE or ENTER: pick color & return to UI
- ESC: cancel and return to UI

Requires: PyQt6  (pip install PyQt6)
"""

import sys
from PyQt6.QtCore import Qt, QTimer, QPoint, QRect, pyqtSignal
from PyQt6.QtGui import QCursor, QColor, QGuiApplication, QPainter, QPen, QBrush, QFont
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame

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
    colorPicked = pyqtSignal(str, QColor)
    cancelled = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(None, Qt.WindowType.FramelessWindowHint | 
                        Qt.WindowType.WindowStaysOnTopHint | 
                        Qt.WindowType.BypassWindowManagerHint)
        self.parent_window = parent
        
        # Get full screen geometry across all monitors
        geo = QGuiApplication.primaryScreen().virtualGeometry()
        self.setGeometry(geo)
        
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setCursor(Qt.CursorShape.BlankCursor)

        self.cursor_pos = QCursor.pos()
        self.current_color = QColor(0, 0, 0)
        self.current_hex = "#000000"

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)

    def start_picking(self):
        self.cursor_pos = QCursor.pos()
        self.current_color = color_at(self.cursor_pos)
        self.current_hex = to_hex(self.current_color)
        
        self.showFullScreen()
        self.raise_()
        self.activateWindow()
        self.setFocus()
        self.grabKeyboard()  # Grab keyboard input
        self.grabMouse()     # Grab mouse input
        
        self.timer.start(12)

    def stop_picking(self):
        self.timer.stop()
        self.releaseKeyboard()
        self.releaseMouse()
        self.hide()

    # --- Events ---
    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Escape:
            self.stop_picking()
            self.cancelled.emit()
        elif e.key() in (Qt.Key.Key_Space, Qt.Key.Key_Return, Qt.Key.Key_Enter):
            hex_code = self.current_hex
            color = self.current_color
            self.stop_picking()
            self.colorPicked.emit(hex_code, color)
        e.accept()

    def mouseMoveEvent(self, e):
        # Don't update cursor_pos here, use global cursor in tick()
        e.accept()

    def mousePressEvent(self, e):
        # Prevent clicks from going through
        e.accept()

    def mouseReleaseEvent(self, e):
        # Prevent clicks from going through
        e.accept()

    def tick(self):
        self.cursor_pos = QCursor.pos()
        self.current_color = color_at(self.cursor_pos)
        self.current_hex = to_hex(self.current_color)
        self.update()

    # --- Drawing ---
    def _preview_geometry(self, pos: QPoint) -> QRect:
        radius = 20
        offset = QPoint(35, 35)
        center = pos + offset
        return QRect(center.x() - radius, center.y() - radius, radius * 2, radius * 2)

    def paintEvent(self, _event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        pos = self.cursor_pos
        gap, arm = 6, 16
        ring_outer, ring_thickness = 12, 2

        # Shadow crosshair
        pen_shadow = QPen(QColor(0, 0, 0, 150), 4)
        p.setPen(pen_shadow)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p.drawLine(pos + QPoint(-(gap + arm) + dx, dy), pos + QPoint(-gap + dx, dy))
            p.drawLine(pos + QPoint(gap + dx, dy), pos + QPoint(gap + arm + dx, dy))
            p.drawLine(pos + QPoint(dx, -(gap + arm) + dy), pos + QPoint(dx, -gap + dy))
            p.drawLine(pos + QPoint(dx, gap + dy), pos + QPoint(dx, gap + arm + dy))

        # White crosshair
        p.setPen(QPen(QColor(255, 255, 255, 240), 2))
        p.drawLine(pos + QPoint(-(gap + arm), 0), pos + QPoint(-gap, 0))
        p.drawLine(pos + QPoint(gap, 0), pos + QPoint(gap + arm, 0))
        p.drawLine(pos + QPoint(0, -(gap + arm)), pos + QPoint(0, -gap))
        p.drawLine(pos + QPoint(0, gap), pos + QPoint(0, gap + arm))

        # Target ring
        p.setPen(QPen(QColor(0, 0, 0, 180), ring_thickness + 2))
        p.drawEllipse(pos, ring_outer, ring_outer)
        p.setPen(QPen(QColor(255, 255, 255, 240), ring_thickness))
        p.drawEllipse(pos, ring_outer, ring_outer)

        # Preview circle
        preview = self._preview_geometry(pos)
        p.setPen(QPen(QColor(0, 0, 0, 180), 3))
        p.setBrush(QBrush(self.current_color))
        p.drawEllipse(preview)
        p.setPen(QPen(QColor(255, 255, 255, 240), 1.5))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawEllipse(preview.adjusted(2, 2, -2, -2))

        # Hex label with instructions
        p.setPen(QColor(255, 255, 255))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        p.setFont(font)
        
        text = self.current_hex
        metrics = p.fontMetrics()
        pad = 8
        w = metrics.horizontalAdvance(text) + pad * 2
        h = metrics.height() + pad * 2
        tl = preview.bottomRight() + QPoint(12, 8)
        bg = QRect(tl.x(), tl.y(), w, h)
        
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(0, 0, 0, 200))
        p.drawRoundedRect(bg, 6, 6)
        p.setPen(QColor(255, 255, 255))
        p.drawText(bg.adjusted(pad, pad, -pad, -pad), Qt.AlignmentFlag.AlignVCenter, text)

        # Instructions
        font.setPointSize(11)
        font.setBold(False)
        p.setFont(font)
        instruction_text = "Press SPACE or ENTER to pick • ESC to cancel"
        inst_metrics = p.fontMetrics()
        inst_w = inst_metrics.horizontalAdvance(instruction_text) + 20
        inst_h = inst_metrics.height() + 16
        
        screen_rect = self.rect()
        inst_x = (screen_rect.width() - inst_w) // 2
        inst_y = screen_rect.height() - 80
        inst_rect = QRect(inst_x, inst_y, inst_w, inst_h)
        
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(0, 0, 0, 200))
        p.drawRoundedRect(inst_rect, 8, 8)
        p.setPen(QColor(255, 255, 255, 230))
        p.drawText(inst_rect, Qt.AlignmentFlag.AlignCenter, instruction_text)

        p.end()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Color Picker")
        self.setFixedSize(450, 450)
        
        # Create central widget and layout
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        title = QLabel("Color Picker")
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: #FFFFFF;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Color preview frame
        self.color_frame = QFrame()
        self.color_frame.setFixedSize(100, 100)
        self.color_frame.setStyleSheet("background-color: #F5F5F5; border: 3px solid #ddd; border-radius: 10px;")
        frame_layout = QHBoxLayout()
        frame_layout.addStretch()
        frame_layout.addWidget(self.color_frame)
        frame_layout.addStretch()
        layout.addLayout(frame_layout)
        
        # Hex code label
        self.hex_label = QLabel("No color selected")
        self.hex_label.setStyleSheet("font-size: 18px; font-family: monospace; color: #555;")
        self.hex_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.hex_label)
        
        # Pick color button
        self.pick_btn = QPushButton("Pick Color")
        self.pick_btn.setFixedHeight(55)
        self.pick_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        self.pick_btn.clicked.connect(self.start_picking)
        layout.addWidget(self.pick_btn)
        
        # Instructions
        instructions = QLabel("Press SPACE or ENTER to pick color")
        instructions.setStyleSheet("font-size: 12px; color: #888; font-style: bold;")
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(instructions)
        
        layout.addStretch()
        
        # Create overlay
        self.overlay = Overlay(self)
        self.overlay.colorPicked.connect(self.on_color_picked)
        self.overlay.cancelled.connect(self.on_picker_cancelled)
        
    def start_picking(self):
        self.hide()  # Hide main window while picking
        QTimer.singleShot(100, self.overlay.start_picking)  # Small delay for smooth transition
        
    def on_color_picked(self, hex_code, color):
        # Update UI
        self.hex_label.setText(hex_code)
        self.color_frame.setStyleSheet(
            f"background-color: {hex_code}; border: 3px solid #999; border-radius: 10px;"
        )
        
        # Copy to clipboard
        QGuiApplication.clipboard().setText(hex_code)
        
        # Show main window again
        self.show()
        self.activateWindow()
        self.raise_()
        
    def on_picker_cancelled(self):
        # Just restore the main window
        self.show()
        self.activateWindow()
        self.raise_()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Color Picker")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()