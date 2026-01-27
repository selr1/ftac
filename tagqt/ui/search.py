from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, 
    QPushButton, QLabel, QTreeWidget, QTreeWidgetItem, QHeaderView, 
    QDialogButtonBox, QWidget
)
from PySide6.QtCore import Qt
from tagqt.ui.theme import Theme
from tagqt.ui import dialogs

class UnifiedSearchDialog(QDialog):
    def __init__(self, parent=None, mode="lyrics", initial_artist="", initial_title="", initial_album="", fetcher_callback=None):
        super().__init__(parent)
        self.setWindowTitle(f"Get {mode.capitalize()}{'s' if mode == 'cover' else ''}")
        self.resize(800, 600)
        self.setStyleSheet(Theme.get_stylesheet())
        
        self.mode = mode
        self.fetcher_callback = fetcher_callback
        self.selected_result = None
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # --- Search Inputs ---
        input_group = QWidget()
        input_layout = QFormLayout(input_group)
        input_layout.setContentsMargins(0, 0, 0, 0)
        
        self.artist_edit = QLineEdit(initial_artist)
        self.album_edit = QLineEdit(initial_album)
        self.title_edit = QLineEdit(initial_title)
        
        input_layout.addRow("Artist:", self.artist_edit)
        if mode == "lyrics":
            input_layout.addRow("Title:", self.title_edit)
        input_layout.addRow("Album:", self.album_edit)
        
        layout.addWidget(input_group)
        
        # Search Button
        self.search_btn = QPushButton("Search")
        self.search_btn.setProperty("class", "primary")
        self.search_btn.setCursor(Qt.PointingHandCursor)
        self.search_btn.clicked.connect(self.perform_search)
        layout.addWidget(self.search_btn)
        
        # --- Results Tree ---
        self.tree = QTreeWidget()
        if mode == "lyrics":
            self.tree.setHeaderLabels(["Title", "Artist", "Album", "Duration", "Type"])
        else:
            self.tree.setHeaderLabels(["Album", "Artist", "Source", "Size"])
            
        self.tree.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tree.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tree.setRootIsDecorated(False)
        self.tree.itemDoubleClicked.connect(self.accept_selection)
        layout.addWidget(self.tree)
        
        # --- Footer Buttons ---
        buttons = QDialogButtonBox(QDialogButtonBox.Cancel)
        buttons.rejected.connect(self.reject)
        
        self.select_btn = QPushButton("Select")
        self.select_btn.setProperty("class", "primary")
        self.select_btn.setCursor(Qt.PointingHandCursor)
        self.select_btn.clicked.connect(self.accept_selection)
        self.select_btn.setEnabled(False) # Disabled until selection
        
        buttons.addButton(self.select_btn, QDialogButtonBox.AcceptRole)
        
        layout.addWidget(buttons)
        
        self.tree.itemSelectionChanged.connect(self.on_selection_changed)
        
        # Auto-search if we have enough info? Maybe not, let user confirm.
        # But user expects "Search" to just work if they clicked "Fetch".
        # Let's auto-search if fields are populated.
        if initial_artist and (initial_title or mode == "cover"):
            # Use a timer or just call it? Call it directly might block UI show.
            # Let's just let user click search, or maybe trigger it.
            # User said: "currently when i search for lyrics and search temr window appear and when i confirm it dissappear and another windows appear... i dont want it like that"
            # So they probably want to see the dialog, maybe adjust, then search.
            pass

    def perform_search(self):
        artist = self.artist_edit.text()
        title = self.title_edit.text()
        album = self.album_edit.text()
        
        if not artist:
            dialogs.show_warning(self, "Missing Info", "Artist is required.")
            return
            
        if self.mode == "lyrics" and not title:
            dialogs.show_warning(self, "Missing Info", "Title is required for lyrics.")
            return
             
        self.tree.clear()
        self.select_btn.setEnabled(False)
        
        # Show loading?
        self.search_btn.setText("Searching...")
        self.search_btn.setEnabled(False)
        self.repaint() # Force update
        
        try:
            results = []
            if self.fetcher_callback:
                if self.mode == "lyrics":
                    results = self.fetcher_callback(artist, title, album)
                else:
                    results = self.fetcher_callback(artist, album)
            
            if not results:
                dialogs.show_info(self, "No Results", "No matches found.")
            else:
                self.populate_results(results)
                
        except Exception as e:
            dialogs.show_error(self, "Error", f"Search failed: {e}")
        finally:
            self.search_btn.setText("Search")
            self.search_btn.setEnabled(True)

    def populate_results(self, results):
        for res in results:
            if self.mode == "lyrics":
                duration_str = self.format_duration(res.get("duration", 0))
                type_str = "Synced" if res.get("isSynced") else "Plain"
                
                item = QTreeWidgetItem([
                    res.get("trackName", ""),
                    res.get("artistName", ""),
                    res.get("albumName", ""),
                    duration_str,
                    type_str
                ])
            else: # cover
                item = QTreeWidgetItem([
                    res.get("album", ""),
                    res.get("artist", ""),
                    res.get("source", ""),
                    res.get("size", "")
                ])
            
            item.setData(0, Qt.UserRole, res)
            self.tree.addTopLevelItem(item)

    def format_duration(self, seconds):
        if not seconds: return ""
        m, s = divmod(int(seconds), 60)
        return f"{m:02d}:{s:02d}"

    def on_selection_changed(self):
        self.select_btn.setEnabled(len(self.tree.selectedItems()) > 0)

    def accept_selection(self):
        item = self.tree.currentItem()
        if item:
            self.selected_result = item.data(0, Qt.UserRole)
            self.accept()
