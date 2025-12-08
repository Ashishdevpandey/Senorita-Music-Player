SENORITA_THEME = """
/* Global Styles */
QWidget {
    background-color: #F9F1D8; /* Parchment/Old Paper background */
    color: #2C1B0E; /* Dark Coffee/Ink text */
    font-family: 'Georgia', 'Times New Roman', serif; /* Serif font for book look */
    font-size: 15px;
}

/* Sidebar */
QWidget#widget_sidebar {
    background-color: #F0E6C2; /* Slightly darker/aged paper */
    border-right: 1px solid #D7CEA5;
}

QFrame#frame_music_section {
    background-color: transparent;
    border: none;
}

QLabel#label_logo {
    color: #8B4513; /* SaddleBrown for "Title" ink */
    font-size: 28px;
    font-weight: bold;
    font-style: italic;
    padding: 24px 20px;
    letter-spacing: 1px;
    font-family: 'Garamond', 'Georgia', serif;
}

QPushButton.sidebar_btn {
    text-align: left;
    padding: 8px 16px;
    border: none;
    background-color: transparent;
    color: #5D4037; /* Brownish grey */
    font-size: 15px;
    font-weight: normal;
    border-radius: 4px;
    margin: 1px 8px;
}

QPushButton.sidebar_btn:hover {
    background-color: #E6D8AD; /* Darker parchment hover */
    color: #2C1B0E;
    font-weight: bold;
}

QPushButton.sidebar_btn:checked {
    background-color: #E6D8AD;
    color: #8B4513;
    font-weight: bold;
    border-left: 3px solid #8B4513; /* Bookmark style indicator */
}

QLabel#label_section_header {
    color: #8D6E63;
    font-size: 13px;
    font-weight: bold;
    padding: 16px 24px 8px;
    text-transform: uppercase;
    letter-spacing: 1px;
    border-bottom: 1px solid #D7CEA5; /* Section divider */
    margin-bottom: 5px;
}

/* Main Content Area */
QWidget#widget_main {
    background-color: #F9F1D8;
    background-image: none; /* Could add a paper texture image here if available */
}

/* Search Bar */
QLineEdit#lineEdit_search {
    background-color: #FFFDF0; /* Lighter paper */
    border: 1px solid #D7CEA5;
    border-radius: 4px; /* Less rounded, more like a box/input field */
    padding: 12px 24px;
    font-size: 16px;
    color: #2C1B0E;
    selection-background-color: #D7CEA5;
    margin: 20px;
    font-family: 'Georgia', serif;
}

QLineEdit#lineEdit_search:focus {
    border: 1px solid #8B4513;
    background-color: #FFFFFF;
}

/* List Widget (Results) */
QListWidget {
    background-color: transparent;
    border: none;
    outline: none;
    padding: 0 20px;
    icon-size: 64px; /* Larger icons for album art */
}

QListWidget::item {
    background-color: transparent;
    padding: 16px;
    border-bottom: 1px solid #E6D8AD; /* Line between items like a ledger */
    color: #2C1B0E;
    margin-bottom: 0px;
    border-radius: 0px;
}

QListWidget::item:hover {
    background-color: #F0E6C2;
}

QListWidget::item:selected {
    background-color: #E6D8AD;
    color: #8B4513;
    font-weight: bold;
}

/* Player Bar */
QFrame#player_bar {
    background-color: #F0E6C2; /* Match sidebar or slightly different */
    border-top: 2px solid #D7CEA5;
    border-radius: 0px;
}

QLabel#label_title {
    font-size: 16px;
    font-weight: bold;
    color: #2C1B0E;
    font-family: 'Georgia', serif;
}

QLabel#label_artist {
    font-size: 14px;
    color: #5D4037;
    font-style: italic;
}

/* Sliders */
QSlider::groove:horizontal {
    border: none;
    height: 3px;
    background: #D7CEA5;
    margin: 2px 0;
    border-radius: 1.5px;
}

QSlider::handle:horizontal {
    background: #F9F1D8; /* Paper color handle */
    border: 2px solid #8B4513; /* Brown border */
    width: 14px;
    height: 14px;
    margin: -6px 0;
    border-radius: 7px;
}

QSlider::handle:horizontal:hover {
    background: #8B4513;
    border: 2px solid #8B4513;
}

QSlider::sub-page:horizontal {
    background: #8B4513; /* Ink color fill */
    border-radius: 2px;
}

/* Player Controls */
QPushButton.control_btn {
    background-color: transparent;
    border: none;
    border-radius: 16px;
    padding: 0px;
    min-width: 32px;
    max-width: 32px;
    min-height: 32px;
    max-height: 32px;
    color: #2C1B0E;
    font-size: 20px;
}

QPushButton.control_btn_small {
    background-color: transparent;
    border: none;
    border-radius: 12px;
    padding: 0px;
    min-width: 24px;
    max-width: 24px;
    min-height: 24px;
    max-height: 24px;
    color: #8D6E63;
    font-size: 14px;
}

QPushButton.control_btn_small:hover {
    color: #2C1B0E;
}

QPushButton.control_btn:hover {
    background-color: #E6D8AD;
    color: #2C1B0E;
    border-radius: 16px;
}

QPushButton#btn_play_pause {
    background-color: #8B4513; /* SaddleBrown Circle */
    border-radius: 24px;
    min-width: 48px;
    max-width: 48px;
    min-height: 48px;
    max-height: 48px;
    color: #F9F1D8; /* Paper color icon */
    font-size: 22px;
    padding-bottom: 2px;
    border: 2px solid #5D4037; /* Darker border */
}

QPushButton#btn_play_pause:hover {
    background-color: #A0522D; /* Sienna */
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: transparent;
    width: 0px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: transparent;
    min-height: 0px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background: transparent;
    height: 0px;
    margin: 0px;
}

QScrollBar::handle:horizontal {
    background: transparent;
    min-width: 0px;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}
"""
