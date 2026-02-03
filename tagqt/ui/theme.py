class Theme:
    _is_light = False
    
    # Dark Theme (default)
    BASE = "#050505"
    MANTLE = "#121212"
    CRUST = "#000000"
    
    TEXT = "#ffffff"
    SUBTEXT0 = "#b3b3b3"
    SUBTEXT1 = "#d4d4d4"
    
    OVERLAY0 = "#404040"
    OVERLAY1 = "#525252"
    OVERLAY2 = "#737373"
    
    SURFACE0 = "#1e1e1e"
    SURFACE1 = "#2d2d2d"
    SURFACE2 = "#3d3d3d"
    
    ACCENT = "#ff2e63"
    ACCENT_HOVER = "#ff477e"
    ACCENT_DIM = "#991b3b"
    
    RED = "#ff5555"
    
    TOAST_TEXT = "#ffffff"  # Always white on colored toast backgrounds
    
    WINDOW_BG = BASE
    SIDEBAR_BG = MANTLE
    BUTTON_TEXT = TEXT
    
    FONT_FAMILY = "Segoe UI"
    CORNER_RADIUS = "8px"
    
    @classmethod
    def set_light_mode(cls, enabled):
        cls._is_light = enabled
        if enabled:
            cls.BASE = "#f5f5f5"
            cls.MANTLE = "#e8e8e8"
            cls.CRUST = "#ffffff"
            cls.TEXT = "#1a1a1a"
            cls.SUBTEXT0 = "#666666"
            cls.SUBTEXT1 = "#333333"
            cls.OVERLAY0 = "#cccccc"
            cls.OVERLAY1 = "#b3b3b3"
            cls.OVERLAY2 = "#999999"
            cls.SURFACE0 = "#ffffff"
            cls.SURFACE1 = "#f0f0f0"
            cls.SURFACE2 = "#e0e0e0"
            cls.ACCENT = "#e01e4f"
            cls.ACCENT_HOVER = "#c91847"
            cls.ACCENT_DIM = "#a8153b"
            cls.WINDOW_BG = cls.BASE
            cls.SIDEBAR_BG = cls.MANTLE
            cls.BUTTON_TEXT = "#ffffff"
        else:
            cls.BASE = "#050505"
            cls.MANTLE = "#121212"
            cls.CRUST = "#000000"
            cls.TEXT = "#ffffff"
            cls.SUBTEXT0 = "#b3b3b3"
            cls.SUBTEXT1 = "#d4d4d4"
            cls.OVERLAY0 = "#404040"
            cls.OVERLAY1 = "#525252"
            cls.OVERLAY2 = "#737373"
            cls.SURFACE0 = "#1e1e1e"
            cls.SURFACE1 = "#2d2d2d"
            cls.SURFACE2 = "#3d3d3d"
            cls.WINDOW_BG = cls.BASE
            cls.SIDEBAR_BG = cls.MANTLE
            cls.BUTTON_TEXT = cls.TEXT

    @staticmethod
    def get_stylesheet():
        return f"""
            QMainWindow {{
                background-color: {Theme.WINDOW_BG};
                color: {Theme.TEXT};
            }}
            QWidget {{
                font-family: '{Theme.FONT_FAMILY}', sans-serif;
                color: {Theme.TEXT};
                font-size: 14px;
            }}
            QLabel {{
                color: {Theme.TEXT};
                font-weight: 500;
            }}
            QLineEdit {{
                background-color: {Theme.SURFACE0};
                color: {Theme.TEXT};
                border: 1px solid {Theme.SURFACE1};
                border-radius: {Theme.CORNER_RADIUS};
                padding: 10px;
                selection-background-color: {Theme.ACCENT};
                selection-color: {Theme.TEXT};
                font-size: 13px;
            }}
            QLineEdit:focus {{
                border: 1px solid {Theme.ACCENT};
                background-color: {Theme.SURFACE0};
            }}
            QPushButton {{
                background-color: {Theme.SURFACE1};
                color: {Theme.TEXT};
                border: none;
                border-radius: {Theme.CORNER_RADIUS};
                padding: 10px 20px;
                font-weight: 600;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {Theme.SURFACE2};
            }}
            QPushButton:pressed {{
                background-color: {Theme.SURFACE0};
            }}
            /* Primary Action Button Style */
            QPushButton[class="primary"] {{
                background-color: {Theme.ACCENT};
                color: {Theme.TEXT};
            }}
            QPushButton[class="primary"]:hover {{
                background-color: {Theme.ACCENT_HOVER};
            }}

            /* Secondary/Outlined Button Style */
            QPushButton[class="secondary"] {{
                background-color: {Theme.SURFACE0};
                border: 1px solid {Theme.SURFACE2};
                color: {Theme.TEXT};
            }}
            QPushButton[class="secondary"]:hover {{
                background-color: {Theme.SURFACE1};
                border: 1px solid {Theme.OVERLAY0};
            }}
            
            /* Combo Box */
            QComboBox {{
                background-color: {Theme.SURFACE0};
                color: {Theme.TEXT};
                border: 1px solid {Theme.SURFACE1};
                border-radius: {Theme.CORNER_RADIUS};
                padding: 8px;
                min-width: 100px;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {Theme.SURFACE0};
                color: {Theme.TEXT};
                selection-background-color: {Theme.ACCENT};
                selection-color: {Theme.TEXT};
                border: 1px solid {Theme.SURFACE1};
            }}

            /* Tree Widget (File List) */
            QTreeWidget {{
                background-color: {Theme.MANTLE};
                alternate-background-color: {Theme.SURFACE0};
                border: 1px solid {Theme.SURFACE0};
                border-radius: {Theme.CORNER_RADIUS};
                padding: 5px;
                outline: none;
            }}
            QTreeWidget::item {{
                padding: 10px 8px;
                border-radius: 4px;
                color: {Theme.SUBTEXT1};
            }}
            QTreeWidget::item:alternate {{
                background-color: {Theme.SURFACE0};
            }}
            QTreeWidget::item:selected {{
                background-color: {Theme.SURFACE1};
                color: {Theme.ACCENT};
            }}
            QTreeWidget::item:hover {{
                background-color: {Theme.SURFACE0};
            }}
            QHeaderView::section {{
                background-color: {Theme.MANTLE};
                color: {Theme.SUBTEXT0};
                padding: 8px;
                border: none;
                border-bottom: 1px solid {Theme.SURFACE0};
                font-weight: bold;
                font-size: 12px;
                text-transform: uppercase;
            }}
            
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            
            /* Scrollbar Styling */
            QScrollBar:vertical {{
                border: none;
                background: {Theme.MANTLE};
                width: 8px;
                margin: 0;
            }}
            QScrollBar::handle:vertical {{
                background: {Theme.SURFACE2};
                min-height: 20px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {Theme.OVERLAY0};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            
            /* GroupBox / Frames */
            QFrame {{
                border: none;
            }}

            /* File Dialog & Generic Views */
            QFileDialog {{
                background-color: {Theme.MANTLE};
                color: {Theme.TEXT};
            }}
            QListView, QTreeView {{
                background-color: {Theme.MANTLE};
                alternate-background-color: {Theme.SURFACE0};
                color: {Theme.TEXT};
                border: 1px solid {Theme.SURFACE0};
                border-radius: {Theme.CORNER_RADIUS};
                outline: none;
            }}
            QListView::item:selected, QTreeView::item:selected {{
                background-color: {Theme.SURFACE1};
                color: {Theme.ACCENT};
            }}
            QListView::item:hover, QTreeView::item:hover {{
                background-color: {Theme.SURFACE0};
            }}
            /* Fix for standard headers in dialogs */
            QHeaderView::section {{
                background-color: {Theme.MANTLE};
                color: {Theme.SUBTEXT0};
                padding: 5px;
                border: none;
                border-bottom: 1px solid {Theme.SURFACE0};
            }}

            /* Message Box */
            QMessageBox {{
                background-color: {Theme.MANTLE};
                color: {Theme.TEXT};
            }}
            QMessageBox QLabel {{
                color: {Theme.TEXT};
            }}
            
            /* Dialogs */
            QDialog {{
                background-color: {Theme.MANTLE};
                color: {Theme.TEXT};
            }}
            
            /* Menus */
            QMenuBar {{
                background-color: {Theme.MANTLE};
                color: {Theme.TEXT};
                border-bottom: 1px solid {Theme.SURFACE0};
            }}
            QMenuBar::item {{
                background-color: transparent;
                padding: 8px 12px;
                color: {Theme.TEXT};
            }}
            QMenuBar::item:selected {{
                background-color: {Theme.SURFACE1};
                color: {Theme.ACCENT};
            }}
            QMenuBar::item:pressed {{
                background-color: {Theme.SURFACE0};
            }}
            
            QMenu {{
                background-color: {Theme.SURFACE0};
                color: {Theme.TEXT};
                border: 1px solid {Theme.SURFACE1};
                border-radius: {Theme.CORNER_RADIUS};
                padding: 8px;
            }}
            QMenu::item {{
                padding: 12px 24px;
                border-radius: 4px;
            }}
            QMenu::item:selected {{
                background-color: {Theme.ACCENT};
                color: {Theme.CRUST};
            }}
            QMenu::separator {{
                height: 1px;
                background: {Theme.SURFACE1};
                margin: 8px 10px;
            }}
            
            /* Horizontal Scrollbar */
            QScrollBar:horizontal {{
                border: none;
                background: {Theme.MANTLE};
                height: 8px;
                margin: 0;
            }}
            QScrollBar::handle:horizontal {{
                background: {Theme.SURFACE2};
                min-width: 20px;
                border-radius: 4px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background: {Theme.OVERLAY0};
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical,
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
                background: none;
            }}
            
            /* Progress Bar */
            QProgressBar {{
                background-color: {Theme.SURFACE0};
                border: none;
                border-radius: 4px;
                text-align: center;
                color: {Theme.TEXT};
                height: 20px;
            }}
            QProgressBar::chunk {{
                background-color: {Theme.ACCENT};
                border-radius: 4px;
            }}
            
            /* Progress Dialog */
            QProgressDialog {{
                background-color: {Theme.MANTLE};
                color: {Theme.TEXT};
            }}
            
            /* Text Edit & Plain Text Edit */
            QTextEdit, QPlainTextEdit {{
                background-color: {Theme.SURFACE0};
                color: {Theme.TEXT};
                border: 1px solid {Theme.SURFACE1};
                border-radius: {Theme.CORNER_RADIUS};
                padding: 10px;
                selection-background-color: {Theme.ACCENT};
                selection-color: {Theme.TEXT};
            }}
            QTextEdit:focus, QPlainTextEdit:focus {{
                border: 1px solid {Theme.ACCENT};
            }}
            
            /* Spin Box */
            QSpinBox, QDoubleSpinBox {{
                background-color: {Theme.SURFACE0};
                color: {Theme.TEXT};
                border: 1px solid {Theme.SURFACE1};
                border-radius: {Theme.CORNER_RADIUS};
                padding: 6px;
            }}
            QSpinBox:focus, QDoubleSpinBox:focus {{
                border: 1px solid {Theme.ACCENT};
            }}
            QSpinBox::up-button, QDoubleSpinBox::up-button,
            QSpinBox::down-button, QDoubleSpinBox::down-button {{
                background-color: {Theme.SURFACE1};
                border: none;
                width: 16px;
            }}
            QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
            QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{
                background-color: {Theme.SURFACE2};
            }}
            
            /* Slider */
            QSlider::groove:horizontal {{
                border: none;
                height: 4px;
                background: {Theme.SURFACE1};
                border-radius: 2px;
            }}
            QSlider::handle:horizontal {{
                background: {Theme.ACCENT};
                width: 14px;
                margin: -5px 0;
                border-radius: 7px;
            }}
            QSlider::handle:horizontal:hover {{
                background: {Theme.ACCENT_HOVER};
            }}
            
            /* Tab Widget */
            QTabWidget::pane {{
                border: 1px solid {Theme.SURFACE1};
                background-color: {Theme.MANTLE};
                border-radius: {Theme.CORNER_RADIUS};
            }}
            QTabBar::tab {{
                background-color: {Theme.SURFACE0};
                color: {Theme.SUBTEXT0};
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }}
            QTabBar::tab:selected {{
                background-color: {Theme.MANTLE};
                color: {Theme.ACCENT};
            }}
            QTabBar::tab:hover:!selected {{
                background-color: {Theme.SURFACE1};
            }}
            
            /* Checkbox & Radio */
            QCheckBox, QRadioButton {{
                color: {Theme.TEXT};
                spacing: 8px;
            }}
            QCheckBox::indicator, QRadioButton::indicator {{
                width: 18px;
                height: 18px;
                background-color: {Theme.SURFACE0};
                border: 2px solid {Theme.SURFACE2};
            }}
            QCheckBox::indicator {{
                border-radius: 4px;
            }}
            QRadioButton::indicator {{
                border-radius: 9px;
            }}
            QCheckBox::indicator:checked, QRadioButton::indicator:checked {{
                background-color: {Theme.ACCENT};
                border-color: {Theme.ACCENT};
            }}
            QCheckBox::indicator:hover, QRadioButton::indicator:hover {{
                border-color: {Theme.OVERLAY0};
            }}
            
            /* Group Box */
            QGroupBox {{
                color: {Theme.TEXT};
                border: 1px solid {Theme.SURFACE1};
                border-radius: {Theme.CORNER_RADIUS};
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                color: {Theme.SUBTEXT1};
            }}
            
            /* Tool Tip */
            QToolTip {{
                background-color: {Theme.SURFACE1};
                color: {Theme.TEXT};
                border: 1px solid {Theme.SURFACE2};
                border-radius: 4px;
                padding: 5px;
            }}
            
            /* Status Bar */
            QStatusBar {{
                background-color: {Theme.MANTLE};
                color: {Theme.SUBTEXT0};
            }}
            
            /* Input Dialog */
            QInputDialog {{
                background-color: {Theme.MANTLE};
            }}
            
            /* List Widget */
            QListWidget {{
                background-color: {Theme.MANTLE};
                alternate-background-color: {Theme.SURFACE0};
                color: {Theme.TEXT};
                border: 1px solid {Theme.SURFACE0};
                border-radius: {Theme.CORNER_RADIUS};
                outline: none;
            }}
            QListWidget::item {{
                padding: 8px;
                border-radius: 4px;
            }}
            QListWidget::item:selected {{
                background-color: {Theme.SURFACE1};
                color: {Theme.ACCENT};
            }}
            QListWidget::item:hover {{
                background-color: {Theme.SURFACE0};
            }}
            
            /* Dialog Button Box */
            QDialogButtonBox {{
                button-layout: 3;
            }}
        """
