import sys
import json
import os
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QScrollArea,
                             QDialog, QLineEdit, QFrame, QSizePolicy, QMessageBox)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QFont, QIcon

class SkillDialog(QDialog):
    def __init__(self, parent=None, skill_data=None):
        super().__init__(parent)
        self.skill_data = skill_data
        self.setWindowTitle("New Skill" if not skill_data else "Edit Skill")
        self.setModal(True)
        self.setFixedSize(500, 400)
        self.setup_ui()
        #self.resize(True)
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(35, 35, 35, 35)
        
        # Title
        title = QLabel("New Skill" if not self.skill_data else "Edit Skill")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #333; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Skill Name
        name_label = QLabel("Skill Name:")
        name_label.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        name_label.setStyleSheet("color: #555; margin-top: 5px;")
        layout.addWidget(name_label)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter skill name")
        self.name_input.setFont(QFont("Arial", 13))
        self.name_input.setMinimumHeight(40)
        if self.skill_data:
            self.name_input.setText(self.skill_data['name'])
        layout.addWidget(self.name_input)
        
        # Icon
        icon_label = QLabel("Icon (Emoji):")
        icon_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        icon_label.setStyleSheet("color: #555; margin-top: 5px;")
        layout.addWidget(icon_label)
        
        self.icon_input = QLineEdit()
        self.icon_input.setPlaceholderText(" ")
        self.icon_input.setFont(QFont("Arial", 13))
        self.icon_input.setMaxLength(2)
        self.icon_input.setMinimumHeight(45)
        if self.skill_data:
            self.icon_input.setText(self.skill_data['icon'])
        layout.addWidget(self.icon_input)
        
        layout.addSpacing(10)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        cancel_btn.setMinimumHeight(45)
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save")
        save_btn.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        save_btn.setMinimumHeight(45)
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self.accept)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        # Styling
        self.setStyleSheet("""
            QDialog {
                background: white;
            }
            QLabel {
                color: #333;
            }
            QLineEdit {
                padding: 10px 12px;
                border: 2px solid #ddd;
                border-radius: 8px;
                font-size: 14px;
                background: white;
                color: #333;
            }
            QLineEdit:focus {
                border: 2px solid #6b5b95;
            }
            QPushButton {
                padding: 12px 30px;
                border: none;
                border-radius: 8px;
                font-size: 14px;
            }
        """)
        
        # Set button colors
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: #e0e0e0;
                color: #555;
                border: none;
                border-radius: 8px;
                padding: 12px 30px;
            }
            QPushButton:hover {
                background: #d0d0d0;
            }
        """)
        
        save_btn.setStyleSheet("""
            QPushButton {
                background: #6b5b95;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 30px;
            }
            QPushButton:hover {
                background: #5a4a85;
            }
        """)
        
    def get_data(self):
        return {
            'name': self.name_input.text().strip(),
            'icon': self.icon_input.text().strip()
        }


class SkillRow(QFrame):
    def __init__(self, skill_id, name, icon, total_seconds, is_active, parent=None):
        super().__init__(parent)
        self.skill_id = skill_id
        self.name = name
        self.icon = icon
        self.total_seconds = total_seconds
        self.is_active = is_active
        self.is_selected = False
        self.parent_window = parent
        
        self.setFixedHeight(130) 
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setup_ui()
        self.update_style()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Don't select if clicking the action button
            if not self.action_btn.geometry().contains(event.pos()):
                if self.parent_window:
                    self.parent_window.select_skill(self.skill_id)
        super().mousePressEvent(event)
        
    def set_selected(self, selected):
        self.is_selected = selected
        self.update_style()
        
    def setup_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(25)
        
        # Icon
        icon_label = QLabel(self.icon)
        icon_label.setFont(QFont("Arial", 40))
        icon_label.setFixedSize(80, 80)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("""
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        """)
        layout.addWidget(icon_label)
        
        # Name
        name_label = QLabel(self.name)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        name_label.setStyleSheet("color: white;")
        name_label.setMinimumWidth(600) #spacing from counters
        layout.addWidget(name_label)
        
        # Spacer
        layout.addSpacing(10)
        
        # Time Display
        time_layout = QHBoxLayout()
        time_layout.setSpacing(5)
        time_layout.setSizeConstraint(QHBoxLayout.SizeConstraint.SetFixedSize)
        
        
        hours, minutes, seconds = self.format_time(self.total_seconds)
        
        self.hours_widget = self.create_time_unit("Hours", hours)
        self.minutes_widget = self.create_time_unit("Minutes", minutes)
        self.seconds_widget = self.create_time_unit("Seconds", seconds)
        
        time_layout.addWidget(self.hours_widget)
        time_layout.addWidget(self.minutes_widget)
        time_layout.addWidget(self.seconds_widget)
        
        layout.addLayout(time_layout)
        layout.addStretch()
        
        # Action Button
        self.action_btn = QPushButton(" Stop " if self.is_active else " Log ")
        self.action_btn.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        #Log/Stop width,height
        self.action_btn.setMinimumSize(130, 80)
        self.action_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.action_btn.clicked.connect(self.toggle_timer)
        # Prevent event propagation to parent
        self.action_btn.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.update_button_style()
        layout.addWidget(self.action_btn)
        
        self.setLayout(layout)
        
    def create_time_unit(self, label, value):
        container = QWidget()
        container.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(0, 0, 0, 0)
        
        label_widget = QLabel(label)
        label_widget.setFont(QFont("Roboto", 10, QFont.Weight.Bold))
        label_widget.setStyleSheet("color: #e3e3e3;")
        label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        value_widget = QLabel(value)
        value_widget.setFont(QFont("Roboto", 30, QFont.Weight.Bold))

        value_widget.setFixedSize(140, 50)

        value_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_widget.setStyleSheet("""
            background: rgba(255, 255, 255, 0.95);
            color: #2a2a2a;
            border-radius: 25px;
            padding: 5px 5px;
        """)
        #time style
        value_widget.setObjectName("timeValue")
        
        layout.addWidget(label_widget)
        layout.addWidget(value_widget)
        
        container.setLayout(layout)
        return container
        
    def format_time(self, total_seconds):
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:04d}", f"{minutes:02d}", f"{seconds:02d}"
        
    def update_display(self):
        hours, minutes, seconds = self.format_time(self.total_seconds)
        self.hours_widget.findChild(QLabel, "timeValue").setText(hours)
        self.minutes_widget.findChild(QLabel, "timeValue").setText(minutes)
        self.seconds_widget.findChild(QLabel, "timeValue").setText(seconds)
        
    def toggle_timer(self):
        if self.parent_window:
            if self.is_active:
                self.parent_window.stop_timer(self.skill_id)
            else:
                self.parent_window.start_timer(self.skill_id)
                
    def set_active(self, active):
        self.is_active = active
        self.action_btn.setText(" Stop " if active else " Log ")
        self.update_button_style()
        self.update_style()
        
    def update_button_style(self):
        if self.is_active:
            #showing stop
            self.action_btn.setStyleSheet("""
                QPushButton {
                    background: #3a3a3a;
                    color: white;
                    border: 3px solid #f6a3ff;
                    border-radius: 20px;
                }
                QPushButton:hover {
                    color: #ffffff;                  
                    background: #733b3b;
                    border: 3px solid #d13d3d;
                }
            """)
        else:
            #when button is showing LOG
            self.action_btn.setStyleSheet("""
                QPushButton {
                    background: #b8b3d4;
                    color: #333;
                    border: 3px solid #f6a3ff;
                    border-radius: 20px;
                }
                QPushButton:hover {
                    color: white;                      
                    background: #462c4d;
                }
            """)
            
    def update_style(self):
        if self.is_selected and self.is_active:
            self.setStyleSheet("""
                SkillRow {
                    background: #4a7c59;     
                    border: 3px solid #f6a3ff;
                    border-radius: 12px;
                }
            """)

        elif self.is_selected:
            # Selected state - pink/purple border
            self.setStyleSheet("""
                SkillRow {
                    background: #666666;
                    border: 3px solid #f6a3ff;
                    border-radius: 12px;
                }
            """)

        elif self.is_active:
            # Active state - green
            self.setStyleSheet("""
                SkillRow {
                    background: #4a7c59;
                    border: 3px solid #5a9c69;
                    border-radius: 12px;
                }
            """)

        else:
            # Default state
            self.setStyleSheet("""
                SkillRow {
                    background: #2a2a2a;
                    border: 3px solid transparent;
                    border-radius: 12px;
                }
            """)


class SkillTimeKeeper(QMainWindow):
    def __init__(self):
        super().__init__()
        self.skills = []
        self.active_skill_id = None
        self.selected_skill_id = None
        self.skill_widgets = {}
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_active_timer)
        self.timer.start(1000)  # Update every second
        
        self.data_file = "skills_data.json"
        self.load_data()
        #ekhane
        self.setWindowTitle("Time Keeper")
        self.setGeometry(100, 100, 1450, 900)
        self.setMinimumSize(1200, 500)
        self.setWindowFlags(Qt.WindowType.CustomizeWindowHint)
        
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main widget
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Title Bar
        title_bar = self.create_title_bar()
        main_layout.addWidget(title_bar)
        
        # Skills Area with Scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        self.skills_container = QWidget()
        self.skills_layout = QVBoxLayout()
        self.skills_layout.setSpacing(18)
        self.skills_layout.setContentsMargins(20, 20, 25, 20)  # Extra right margin for scrollbar
        self.skills_layout.addStretch()
        self.skills_container.setLayout(self.skills_layout)
        
        scroll_area.setWidget(self.skills_container)
        main_layout.addWidget(scroll_area, 1)  # Give it stretch factor to fill space
        
        # Settings Section - Fixed at bottom
        settings_section = self.create_settings_section()
        main_layout.addWidget(settings_section, 0)  # No stretch, stays at bottom
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # Styling
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #c9c4e3, stop:1 #b8b3d4);
            }
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: rgba(0, 0, 0, 0.1);
                width: 15px;
                margin: 0px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: rgba(107, 91, 149, 0.6);
                min-height: 30px;
                border-radius: 6px;
                margin: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(107, 91, 149, 0.8);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            QWidget#skillsContainer {
                background: transparent;
            }
        """)
        
        self.skills_container.setObjectName("skillsContainer")
        
        # Load skills
        self.render_skills()
        
    def create_title_bar(self):
        title_bar = QFrame()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("""
            background: rgba(255, 255, 255, 0.15);
            border-bottom: 1px solid rgba(0, 0, 0, 0.1);
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 0, 15, 0)
        
        # Title
        title = QLabel("Time Keeper")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title.setStyleSheet("color: #381b42;")
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Window controls
        btn_style = """
            QPushButton {
                border: none;
                border-radius: 6px;
                font-size: 16px;
                font-weight: bold;
            }
        """
        
        minimize_btn = QPushButton("−")
        minimize_btn.setFixedSize(35, 28)
        minimize_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        minimize_btn.setStyleSheet(btn_style + """
            QPushButton {
                background: #e8e8e8;
                color: #555;
            }
            QPushButton:hover {
                background: #5e365e;
            }
        """)
        minimize_btn.clicked.connect(self.showMinimized)
        
        maximize_btn = QPushButton("🔲")
        maximize_btn.setFixedSize(35, 28)
        maximize_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        maximize_btn.setStyleSheet(btn_style + """
            QPushButton {
                background: #e8e8e8;
                color: #555;
            }
            QPushButton:hover {
                background: #5e365e;
            }
        """)
        maximize_btn.clicked.connect(self.toggle_maximize)
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(35, 28)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet(btn_style + """
            QPushButton {
                background: #ff5f57;
                color: white;
            }
            QPushButton:hover {
                background: #801e18;
            }
        """)
        close_btn.clicked.connect(self.close)
        
        layout.addWidget(minimize_btn)
        layout.addWidget(maximize_btn)
        layout.addWidget(close_btn)
        
        title_bar.setLayout(layout)
        
        # Make title bar draggable
        title_bar.mousePressEvent = self.mouse_press_event
        title_bar.mouseMoveEvent = self.mouse_move_event
        
        return title_bar
        
    def create_settings_section(self):
        settings = QFrame()
        settings.setFixedHeight(100)
        settings.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        settings.setStyleSheet("""
            QFrame {
                background: #2f2f2f;
                border-top: 2px solid rgba(0, 0, 0, 0.1);
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
        label = QLabel("⚙️ Settings ")
        label.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        label.setStyleSheet("color: white;")
        layout.addWidget(label)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        btn_style = """
            QPushButton {
                padding: 18px 30px;
                border: none;
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
                min-height: 50px;
            }
        """
        
        new_btn = QPushButton("New")
        new_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        new_btn.setStyleSheet("""
            QPushButton {
                background: #a8f0a8;
                color: #2a5a2a;
                padding: 10px 30px;
                border: none;
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
                min-height: 10px;
            }
            QPushButton:hover {
                background: #95e095;
            }
        """)
        new_btn.clicked.connect(self.add_skill)
        
        edit_btn = QPushButton("Edit")
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_btn.setStyleSheet("""
            QPushButton {
                background: #c9c4e3;
                color: #333;
                padding: 10px 30px;
                border: none;
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
                min-height: 10px;
            }
            QPushButton:hover {
                background: #b9b4d3;
            }
        """)
        edit_btn.clicked.connect(self.edit_skill)
        
        remove_btn = QPushButton("Remove")
        remove_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        remove_btn.setStyleSheet("""
            QPushButton {
                background: #f0b0b0;
                color: #5a2a2a;
                padding: 10px 30px;
                border: none;
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
                min-height: 10px;
            }
            QPushButton:hover {
                background: #e09090;
            }
        """)
        remove_btn.clicked.connect(self.remove_skill)
        
        button_layout.addWidget(new_btn)
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(remove_btn)
        
        layout.addLayout(button_layout)
        settings.setLayout(layout)
        
        return settings
        
    def render_skills(self):
        # Clear existing widgets
        for widget in self.skill_widgets.values():
            widget.deleteLater()
        self.skill_widgets.clear()
        
        # Remove all items except the stretch
        while self.skills_layout.count() > 1:
            item = self.skills_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Add skill rows
        for skill in self.skills:
            skill_row = SkillRow(
                skill['id'],
                skill['name'],
                skill['icon'],
                skill['total_seconds'],
                skill['is_active'],
                self
            )
            # Restore selection state
            if skill['id'] == self.selected_skill_id:
                skill_row.set_selected(True)
                
            self.skill_widgets[skill['id']] = skill_row
            self.skills_layout.insertWidget(self.skills_layout.count() - 1, skill_row)
            
    def select_skill(self, skill_id):
        """Select a skill for editing or removal"""
        # Deselect previous skill
        if self.selected_skill_id and self.selected_skill_id in self.skill_widgets:
            self.skill_widgets[self.selected_skill_id].set_selected(False)
        
        # Select new skill
        self.selected_skill_id = skill_id
        if skill_id in self.skill_widgets:
            self.skill_widgets[skill_id].set_selected(True)
            
    def add_skill(self):
        dialog = SkillDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data['name'] and data['icon']:
                skill = {
                    'id': str(len(self.skills)) + str(datetime.now().timestamp()),
                    'name': data['name'],
                    'icon': data['icon'],
                    'total_seconds': 0,
                    'is_active': False
                }
                self.skills.append(skill)
                self.save_data()
                self.render_skills()
                
    def edit_skill(self):
        if not self.selected_skill_id:
            QMessageBox.information(self, "No Selection", "Please select a skill to edit by clicking on it.")
            return
            
        skill = None
        for s in self.skills:
            if s['id'] == self.selected_skill_id:
                skill = s
                break
                
        if not skill:
            return
            
        dialog = SkillDialog(self, skill)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data['name'] and data['icon']:
                skill['name'] = data['name']
                skill['icon'] = data['icon']
                self.save_data()
                self.render_skills()
                
    def remove_skill(self):
        if not self.selected_skill_id:
            QMessageBox.information(self, "No Selection", "Please select a skill to remove by clicking on it.")
            return
            
        # Find the skill
        skill_to_remove = None
        skill_index = -1
        for i, skill in enumerate(self.skills):
            if skill['id'] == self.selected_skill_id:
                skill_to_remove = skill
                skill_index = i
                break
                
        if skill_to_remove:
            reply = QMessageBox.question(
                self, 
                'Confirm Removal', 
                f'Are you sure you want to remove "{skill_to_remove["name"]}"?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                # Stop timer if active
                if skill_to_remove['is_active']:
                    self.stop_timer(self.selected_skill_id)
                    
                # Remove the skill
                self.skills.pop(skill_index)
                self.selected_skill_id = None
                self.save_data()
                self.render_skills()
        
    def start_timer(self, skill_id):
        # Stop any active timer
        if self.active_skill_id:
            self.stop_timer(self.active_skill_id)
        
        # Find and activate skill
        for skill in self.skills:
            if skill['id'] == skill_id:
                skill['is_active'] = True
                self.active_skill_id = skill_id
                if skill_id in self.skill_widgets:
                    self.skill_widgets[skill_id].set_active(True)
                break
        
        self.save_data()
        
    def stop_timer(self, skill_id):
        for skill in self.skills:
            if skill['id'] == skill_id:
                skill['is_active'] = False
                if self.active_skill_id == skill_id:
                    self.active_skill_id = None
                if skill_id in self.skill_widgets:
                    self.skill_widgets[skill_id].set_active(False)
                break
        
        self.save_data()
        
    def update_active_timer(self):
        if self.active_skill_id:
            for skill in self.skills:
                if skill['id'] == self.active_skill_id and skill['is_active']:
                    skill['total_seconds'] += 1
                    if self.active_skill_id in self.skill_widgets:
                        widget = self.skill_widgets[self.active_skill_id]
                        widget.total_seconds = skill['total_seconds']
                        widget.update_display()
                    break
                    
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.skills = data.get('skills', [])
                    self.active_skill_id = data.get('active_skill_id')
            except:
                self.skills = self.get_default_skills()
        else:
            self.skills = self.get_default_skills()
            
    def get_default_skills(self):
        return [
            {'id': 'skill1', 'name': 'Guitar', 'icon': ' ', 'total_seconds': 0, 'is_active': False},
            {'id': 'skill2', 'name': 'Painting', 'icon': ' ', 'total_seconds': 0, 'is_active': False},
            {'id': 'skill3', 'name': 'Sports', 'icon': ' ', 'total_seconds': 0, 'is_active': False}
        ]
            
    def save_data(self):
        data = {
            'skills': self.skills,
            'active_skill_id': self.active_skill_id
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
            
    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
            
    def mouse_press_event(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            
    def mouse_move_event(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            
    def closeEvent(self, event):
        self.save_data()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SkillTimeKeeper()
    window.show()
    sys.exit(app.exec())