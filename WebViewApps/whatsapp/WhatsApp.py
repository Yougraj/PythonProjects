import sys

from PyQt6.QtCore import QCoreApplication, QEvent, QUrl
from PyQt6.QtGui import QIcon
from PyQt6.QtWebEngineCore import QWebEngineProfile
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox


class WhatsApp(QMainWindow):
    def __init__(self, url):
        super().__init__()
        self.setWindowTitle("WhatsApp Web")
        self.setGeometry(100, 100, 1200, 800)

        # Set up the QWebEngineView
        self.browser = QWebEngineView()

        # Set custom User-Agent for compatibility
        user_agent = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        )
        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpUserAgent(user_agent)

        self.browser.setUrl(QUrl(url))
        self.setCentralWidget(self.browser)

        # Enable Local Storage
        self.browser.settings().setAttribute(
            self.browser.settings().WebAttribute.LocalStorageEnabled, True
        )

        # Enable notifications
        self.browser.page().featurePermissionRequested.connect(self.handle_permission_request)

    def handle_permission_request(self, security_origin, feature):
        if feature == self.browser.page().Notification:
            self.browser.page().setFeaturePermission(security_origin, feature, self.browser.page().PermissionGranted)

def main():
    QCoreApplication.setApplicationName("WhatsApp Desktop")
    app = QApplication(sys.argv)
    
    # Set an application icon if you have one
    app.setWindowIcon(QIcon("./WhatsApp.png"))  # Update the icon path

    url = "https://web.whatsapp.com/"
    window = WhatsApp(url)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
