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
        self.logout_button = QPushButton("Log Out")
        self.delete_button = QPushButton("Delete Selected Account")
        self.back_button = QPushButton("Back to Profile")

        for btn in (self.switch_button, self.logout_button, self.delete_button, self.back_button):
            btn.setMinimumHeight(36)
            btn.setStyleSheet(self.styles["button"])  # apply button style
            self.layout.addWidget(btn)

        # Connect signals
        self.switch_button.clicked.connect(self.switch_account)
        self.logout_button.clicked.connect(self.logout)
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
        """Switch to the selected account after password verification."""
        item = self.account_list.currentItem()
        if not item:
            QMessageBox.warning(self, "No Selection", "Please select an account first.")
            return

        username = item.text().replace(" (current)", "")
        
        # Don't require password if switching to current account
        if username == self.data.username:
            QMessageBox.information(self, "Already Logged In", "You are already logged into this account.")
            return
        
        # Show password dialog
        password_dialog = self.create_password_dialog(username)
        if password_dialog.exec():
            entered_password = password_dialog.password_input.text().strip()
            
            # Verify password
            if self.verify_password(username, entered_password):
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
            else:
                QMessageBox.critical(self, "Authentication Failed", "Incorrect password. Please try again.")
    
    def create_password_dialog(self, username):
        """Create a password input dialog for account switching."""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Enter Password")
        dialog.setModal(True)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel(f"Enter password for '{username}'")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #434190; padding: 10px;")
        layout.addWidget(title)
        
        # Password input
        dialog.password_input = QLineEdit()
        dialog.password_input.setPlaceholderText("Password")
        dialog.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        dialog.password_input.setFixedWidth(250)
        dialog.password_input.setStyleSheet("padding: 10px; font-size: 14px; border-radius: 5px; border: 2px solid #CBD5E0;")
        dialog.password_input.returnPressed.connect(dialog.accept)  # Allow Enter key
        layout.addWidget(dialog.password_input)
        
        # Buttons
        button_layout = QVBoxLayout()
        
        confirm_btn = QPushButton("Confirm")
        confirm_btn.setStyleSheet("padding: 10px; font-weight: bold; background-color: #FC483D; color: white; border-radius: 8px;")
        confirm_btn.clicked.connect(dialog.accept)
        button_layout.addWidget(confirm_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("padding: 10px; background-color: #888; color: white; border-radius: 8px;")
        cancel_btn.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        dialog.setLayout(layout)
        
        return dialog
    
    def verify_password(self, username, password):
        """Verify the password for the given username."""
        import os
        import json
        import hashlib
        
        profile_path = "user_profiles.json"
        if not os.path.exists(profile_path):
            return False
        
        try:
            with open(profile_path, "r") as f:
                data = json.load(f)
            
            if username not in data:
                return False
            
            # Hash the entered password and compare
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            return data[username].get("password") == hashed_password
        except Exception as e:
            print(f"Error verifying password: {e}")
            return False

    def logout(self):
        """Log out and return to login page."""
        print("🚪 Logging out...")
        
        # Confirm action
        reply = QMessageBox.question(
            self,
            "Log Out",
            "Are you sure you want to log out?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Clear current user
            self.data.username = None
            
            # Find AppStack and return to WelcomePage
            from PyQt6.QtWidgets import QApplication
            app = QApplication.instance()
            
            for widget in app.topLevelWidgets():
                if widget.__class__.__name__ == 'AppStack':
                    print("Found AppStack")
                    # Get the welcome page
                    welcome_page = widget.welcome_page
                    
                    # Reset login page fields (login_page is a FadeWidget, so access .widget)
                    if hasattr(welcome_page, 'login_page'):
                        print("Found login_page")
                        login_widget = welcome_page.login_page.widget if hasattr(welcome_page.login_page, 'widget') else welcome_page.login_page
                        if hasattr(login_widget, 'reset_fields'):
                            login_widget.reset_fields()
                            print("Reset login fields")
                        
                        # Show the login page in the stacked widget
                        if hasattr(welcome_page, 'stacked'):
                            welcome_page.stacked.setCurrentWidget(welcome_page.login_page)
                            print(f"Set current widget to login_page, index: {welcome_page.stacked.currentIndex()}")
                            # Make sure login page is visible
                            welcome_page.login_page.show()
                    
                    # Switch to welcome page (index 0 in AppStack)
                    widget.setCurrentIndex(0)
                    widget.show()
                    print("✅ Logged out successfully - switched to WelcomePage")
                    break

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
