import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
import requests
from bs4 import BeautifulSoup

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'HTML Bulucu Özgür Baba'
        self.left = 50
        self.top = 50
        self.width = 600
        self.height = 400
        self.font_size = 14
        self.font = QFont("Arial", self.font_size)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFont(self.font)
        self.setStyleSheet("background-color: grey;")  # Arayüzün arka plan rengi

        # Aranacak değer için metin kutusu
        self.search_label = QLabel(self)
        self.search_label.setText("Aranacak değer:")
        self.search_label.move(5, 20)
        self.search_label.setStyleSheet("color: #283747; font-size: 18px;")  # Metin rengi ve boyutu

        self.search_box = QLineEdit(self)
        self.search_box.resize(200, 25)
        self.search_box.move(150, 20)
        self.search_box.setStyleSheet("background-color: #ECF0F1; color: #283747; font-size: 14px;")  # Arama kutusunun arka planı, metin rengi ve boyutu
        self.url_label = QLabel(self)
        self.url_label.setText("Aranacak URL:")
        self.url_label.move(5, 50)
        self.url_label.setStyleSheet("color: #283747; font-size: 18px;")  # Metin rengi ve boyutu

        self.url_box = QLineEdit(self)
        self.url_box.resize(200, 25)
        self.url_box.move(150, 50)
        self.url_box.setStyleSheet(
            "background-color: #ECF0F1; color: #283747; font-size: 14px;")  # Arama kutusunun arka planı, metin rengi ve boyutu
        # "Ara" düğmesi
        self.search_button = QPushButton(self)
        self.search_button.setText("Ara")
        self.search_button.resize(150, 25)

        self.search_button.move(350, 20)
        self.search_button.setStyleSheet("background-color: #2980B9; color: white; font-size: 26px; border-radius: 5px;")  # Düğmenin arka plan rengi, metin rengi, boyutu ve köşe yuvarlama özelliği
        self.search_button.clicked.connect(self.search)

        # Sonuçlar için etiket
        self.result_label = QLabel(self)
        self.result_label.setText("")
        self.result_label.move(20, 70)
        self.result_label.setAlignment(Qt.AlignTop)
        self.result_label.setWordWrap(True)
        self.result_label.resize(550, 200)
        self.result_label.setStyleSheet(
            "background-color: #ECF0F1; color: #283747; font-size: 14px; padding: 10px; border: 1px solid #BDC3C7;")
        self.result_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.result_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)

    # Etiketin arka plan rengi, metin rengi, boyutu ve dolgu özelliği

    def search(self):
        # Get the URL and search value
        url = self.url_box.text()
        search_value = self.search_box.text()

        # Get the HTML content from the URL
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all tags in the HTML content
        tags = soup.find_all()

        # Keep track of the two closest tags
        closest_tags = []

        # Iterate over the tags to find the two closest tags that contain the search value
        for tag in tags:
            if search_value in str(tag):
                if len(closest_tags) < 5:
                    closest_tags.append(tag)
                elif tag.get_text().find(search_value) < closest_tags[1].get_text().find(search_value):
                    closest_tags[1] = tag
                closest_tags = sorted(closest_tags, key=lambda t: t.get_text().find(search_value))

        # Prepare the result string
        result = ""
        for tag in closest_tags:
            if search_value in tag.get_text():
                result += f"Etiket: {tag.name}\n"
                if tag.has_attr('class'):
                    result += f"Class: {tag['class']}\n"
                if tag.has_attr('style'):
                    result += f"Style: {tag['style']}\n"
                result += "\n"

        # Set the result label in the GUI
        if result:
            self.result_label.setText(result)
        else:
            self.result_label.setText("Aradığınız değer bulunamadı.")
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
