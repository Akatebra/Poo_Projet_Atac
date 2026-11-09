import sys
# from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFormLayout, QLineEdit, QMessageBox
from Point import Point

class FenetrePlugin(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Plugin QGIS-Isochrone")
        self.resize(600,400)
        self.move(30,200)

        layout = QVBoxLayout()
        form = QFormLayout() 
        self.lonEdit = QLineEdit()
        self.latEdit = QLineEdit()
        form.addRow("Longitude :", self.lonEdit)
        form.addRow("Latitude :", self.latEdit)
        layout.addLayout(form)

        self.selectButton = QPushButton("Sélectionner un point")
        self.calculateButton = QPushButton("Lancer le calcul")
        layout.addWidget(self.selectButton)
        layout.addWidget(self.calculateButton)
        self.setLayout(layout)

        self.selectButton.clicked.connect(self.select_point)
        self.calculateButton.clicked.connect(self.lancer_calcul)

        

    def select_point(self):
        print("Point sélectionné")

    def lancer_calcul(self):
        lon = float(self.lonEdit.text())
        lat = float(self.latEdit.text())
        point: Point[float, float] = Point(lon, lat)
        print(point.toStr())

if __name__ == "__main__":
    app = QApplication.instance() 
    if not app: # sinon on crée une instance de QApplication
        app = QApplication(sys.argv)
    fen = FenetrePlugin()
    fen.show()
    app.exec_()

    p = Point(2.337306, 48.849319)
    print(p.toStr())