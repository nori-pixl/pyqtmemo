import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QListWidgetItem, QTextEdit, 
    QLabel, QToolBar, QSlider
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QAction

class AdvancedNotepad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('多機能メモ帳')
        self.setGeometry(100, 100, 800, 500)
        
        # --- メインレイアウトのベース ---
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # ==========================================
        # 1. 左側：サイドバーエリア（フォルダ・メモ一覧）
        # ==========================================
        sidebar = QWidget()
        sidebar.setStyleSheet("background-color: #f0f4f8; border-right: 1px solid #dcdcdc;")
        sidebar.setFixedWidth(250)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)
        
        # 新規フォルダボタン
        btn_new_folder = QPushButton("＋ 新規フォルダ")
        btn_new_folder.setStyleSheet("padding: 8px; font-weight: bold; background-color: #ffffff; border: 1px solid #ccc;")
        sidebar_layout.addWidget(btn_new_folder)
        
        # セクションヘッダー（メモ ＋ ボタン）
        header_layout = QHBoxLayout()
        lbl_memo_title = QLabel("📂 メモ")
        lbl_memo_title.setStyleSheet("font-weight: bold; color: #333;")
        btn_add_memo = QPushButton("＋")
        btn_add_memo.setFixedSize(24, 24)
        header_layout.addWidget(lbl_memo_title)
        header_layout.addStretch()
        header_layout.addWidget(btn_add_memo)
        sidebar_layout.addLayout(header_layout)
        
        # メモ一覧リスト
        self.memo_list = QListWidget()
        self.memo_list.setStyleSheet("""
            QListWidget { border: none; background: transparent; }
            QListWidget::item { padding: 10px; border-radius: 4px; }
            QListWidget::item:selected { background-color: #0078d4; color: white; }
        """)
        
        # サンプルアイテムの追加
        item = QListWidgetItem("📄 ああああ")
        self.memo_list.addItem(item)
        self.memo_list.setCurrentItem(item) # 初期選択
        sidebar_layout.addWidget(self.memo_list)
        
        # ==========================================
        # 2. 右側：メインコンテンツエリア（ツールバー ＋ エディタ）
        # ==========================================
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        
        # 上部ツールバー（青い背景のバー）
        toolbar = QToolBar()
        toolbar.setStyleSheet("background-color: #0078d4; color: white; padding: 5px; spacing: 10px; border: none;")
        toolbar.setMovable(False)
        
        # ツールバーの各種操作用ボタン・スライダー
        btn_menu = QPushButton("☰")
        btn_bold = QPushButton("B")
        btn_italic = QPushButton("I")
        btn_color = QPushButton("■")
        
        # スタイル適用
        for btn in [btn_menu, btn_bold, btn_italic, btn_color]:
            btn.setFixedSize(30, 30)
            btn.setStyleSheet("background-color: rgba(255,255,255,0.2); color: white; border: none; font-weight: bold; border-radius: 3px;")
        
        # 文字サイズ用スライダー
        slider_layout = QHBoxLayout()
        lbl_small_a = QLabel("A")
        lbl_small_a.setStyleSheet("color: white; font-size: 10px;")
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setFixedWidth(100)
        slider.setRange(10, 30)
        slider.setValue(14)
        lbl_large_a = QLabel("A")
        lbl_large_a.setStyleSheet("color: white; font-size: 18px;")
        
        # 保存ボタン（右端）
        btn_save = QPushButton("💾")
        btn_save.setFixedSize(35, 30)
        btn_save.setStyleSheet("background-color: rgba(255,255,255,0.3); border: none; font-size: 16px; border-radius: 3px;")
        
        # ツールバーへの配置
        toolbar.addWidget(btn_menu)
        toolbar.addSeparator()
        toolbar.addWidget(btn_bold)
        toolbar.addWidget(btn_italic)
        toolbar.addWidget(btn_color)
        toolbar.addSeparator()
        toolbar.addWidget(lbl_small_a)
        toolbar.addWidget(slider)
        toolbar.addWidget(lbl_large_a)
        
        # 右端に保存ボタンを追いやるためのスペース
        spacer = QWidget()
        spacer.setSizePolicy(spacer.sizePolicy().Policy.Expanding, spacer.sizePolicy().Policy.Preferred)
        toolbar.addWidget(spacer)
        toolbar.addWidget(btn_save)
        
        right_layout.addWidget(toolbar)
        
        # テキストエディタ領域
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText("追加してください")
        self.text_edit.setStyleSheet("border: none; padding: 15px; font-size: 14px;")
        right_layout.addWidget(self.text_edit)
        
        # 下部ステータスバー（文字数カウント）
        status_bar = QWidget()
        status_bar.setStyleSheet("background-color: #f3f3f3; border-top: 1px solid #dcdcdc; padding: 5px 15px;")
        status_layout = QHBoxLayout(status_bar)
        status_layout.setContentsMargins(0, 0, 0, 0)
        
        self.lbl_char_count = QLabel("152 文字")
        self.lbl_char_count.setStyleSheet("color: #666; font-size: 12px;")
        status_layout.addStretch()
        status_layout.addWidget(self.lbl_char_count)
        
        right_layout.addWidget(status_bar)
        
        # メインレイアウトへ結合
        main_layout.addWidget(sidebar)
        main_layout.addWidget(right_container)
        
        # スライダーによるフォントサイズ変更の連動
        slider.valueChanged.connect(self.change_font_size)
        # 文字数カウンターの連動
        self.text_edit.textChanged.connect(self.update_char_count)
        self.update_char_count()

    def change_font_size(self, value):
        font = self.text_edit.font()
        font.setPointSize(value)
        self.text_edit.setFont(font)
        
    def update_char_count(self):
        count = len(self.text_edit.toPlainText())
        self.lbl_char_count.setText(f"{count} 文字")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AdvancedNotepad()
    ex.show()
    sys.exit(app.exec())
