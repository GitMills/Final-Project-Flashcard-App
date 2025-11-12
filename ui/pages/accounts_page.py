from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt
from ui.visual.styles.styles import get_accounts_page_styles  # Import centralized styles


class AccountsPage(QWidget):
    """
    Page for managing user accounts — allows switching between saved users
    or returning to the login page to add a new one.
    """

    def __init__(self, data, login_page, profile_page, fade_to_page):
        super().__init__()
        self.styles = get_accounts_page_styles()
        self.setStyleSheet(self.styles["page"])
        
        self.data = data
        self.login_page = login_page
        self.profile_page = profile_page
        self.fade_to_page = fade_to_page

        self.setObjectName("AccountsPage")
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title
        self.title = QLabel("Manage Accounts")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet(self.styles["title"])  # use style from styles.py
        self.layout.addWidget(self.title)

        # Accounts list
        self.account_list = QListWidget()
        self.account_list.setStyleSheet(self.styles["list"])  # centralized list style
        self.layout.addWidget(self.account_list)

        # Buttons
        self.switch_button = QPushButton("Switch to Selected Account")
        self.add_button = QPushButton("Add New Account")
        self.delete_button = QPushButton("Delete Selected Account")
        self.back_button = QPushButton("Back to Profile")

        for btn in (self.switch_button, self.add_button, self.delete_button, self.back_button):
            btn.setMinimumHeight(36)
            btn.setStyleSheet(self.styles["button"])  # apply button style
            self.layout.addWidget(btn)

        # Connect signals
        self.switch_button.clicked.connect(self.switch_account)
        self.add_button.clicked.connect(self.add_account)
        self.delete_button.clicked.connect(self.delete_account)
        self.back_button.clicked.connect(lambda: self.fade_to_page(self.profile_page))

        # Load saved accounts
        self.refresh_list()

    def refresh_list(self):
        """Refresh the account list from shared data."""
        self.account_list.clear()
        accounts = getattr(self.data, "accounts", [])
        for username in accounts:
            item = QListWidgetItem(username)
            if username == self.data.username:
                item.setText(f"{username} (current)")
            self.account_list.addItem(item)

    def switch_account(self):
        """Switch to the selected account and fade to ProfilePage."""
        item = self.account_list.currentItem()
        if not item:
            QMessageBox.warning(self, "No Selection", "Please select an account first.")
            return

        username = item.text().replace(" (current)", "")
        self.data.username = username

        profile = self.data.get_profile(username)
        full_name = profile.get("full_name", username)

        if hasattr(self.profile_page, "load_profile"):
            self.profile_page.load_profile(username, full_name)
        else:
            print("⚠️ Warning: ProfilePage has no 'load_profile' method")

        self.refresh_list()
        print(f"✅ Switched to account: {username}")

        # Go back to WelcomePage
        parent_stack = self.parent()
        while parent_stack is not None and not hasattr(parent_stack, "setCurrentIndex"):
            parent_stack = parent_stack.parent()

        if parent_stack is not None:
            print(f"👋 Returning to WelcomePage for selected account: {username}")
            parent_stack.selected_username = username
            parent_stack.setCurrentIndex(0)
        else:
            print("⚠️ Could not find AppStack — staying in current window.")

    def add_account(self):
        """Fade back to the login page to add a new account."""
        print("➕ Adding new account — returning to login page.")
        self.data.username = None
        self.fade_to_page(self.login_page)

    def delete_account(self):
        item = self.account_list.currentItem()
        if not item:
            QMessageBox.warning(self, "No Selection", "Please select an account to delete.")
            return

        username = item.text().replace(" (current)", "")
        confirm = QMessageBox.question(
            self,
            "Delete Account",
            f"Are you sure you want to delete '{username}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            self.data.delete_account(username)
            if username == self.data.username:
                self.data.username = None
            self.refresh_list()

        self.fade_to_page(self.profile_page)
