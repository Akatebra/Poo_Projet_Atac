import sys
# from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

# class Fenetre(QWidget):
#     def __init__(self):
#         QWidget.__init__(self)
#         self.setWindowTitle("Ma fenetre")

#         self.setMouseTracking(True)


#     def mouseMoveEvent(self,event):
#         print("position = " + str(event.x()) + " " + str(event.y()))
    # def mousePressEvent(self,event):
    #     if event.button() == Qt.LeftButton:
    #         print("appui bouton gauche")
    #         print("position = " + str(event.x()) + " " + str(event.y()))

app = QApplication.instance() 
if not app: # sinon on crée une instance de QApplication
    app = QApplication(sys.argv)

fen = QWidget()
# creation du premier bouton
bouton1 = QPushButton("Choisir Point")
# creation du deuxieme bouton
bouton2 = QPushButton("Lancer Calcul Isochrone")

# creation du gestionnaire de mise en forme de type QVBoxLayout
layout = QVBoxLayout()
# ajout du premier bouton au gestionnaire de mise en forme
layout.addWidget(bouton1)
# ajout du deuxieme bouton au gestionnaire de mise en forme
layout.addWidget(bouton2)
# on fixe le QVBoxLayout comme gestionnaire de mise en forme de la fenetre
fen.setLayout(layout)
# bouton = QPushButton("Choisir Point")
# bouton.show()

                              #Création d'une instance de QWidget
# # fen.setWindowTitle("Plugin QGIS")              #Titre de la fenêtre
fen.resize(800,500)                            #Taille de la fenêtre
# fen.move(10,500)


fen.show()
app.exec_()




