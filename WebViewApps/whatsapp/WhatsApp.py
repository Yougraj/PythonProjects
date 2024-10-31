import sys

from PyQt6.QtCore import QCoreApplication, QUrl
from PyQt6.QtWebEngineCore import QWebEngineProfile
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication, QMainWindow


class WhatsApp(QMainWindow):
    def __init__(self, url):
        super().__init__()
        self.setWindowTitle("WhatsApp Web")
        self.setGeometry(100, 100, 1200, 800)

        # Set up the QWebEngineView
        self.browser = QWebEngineView()
        
        # Set custom User-Agent for compatibility
        user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
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

def main():
    QCoreApplication.setApplicationName("WhatsApp Desktop")
    app = QApplication(sys.argv)
    url = "https://web.whatsapp.com/"
    window = WhatsApp(url)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
