import sys
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QTableWidgetItem, QAbstractItemView, QDesktopWidget
from PyQt5.QtGui import QColor
from template import Ui_main_window
import get_data
from subprocess import call

class game_viewer(QMainWindow):
    def __init__(self, parent=None):
        super(game_viewer, self).__init__(parent=parent)

        # Set up the user interface from Designer.
        self.ui = Ui_main_window()
        self.ui.setupUi(self)

        self.ui.todos_jogos.clicked.connect(self.jogos)
        self.ui.procurar_jogo.clicked.connect(self.procura_jogo)

        self.data_json = get_data.get_data()

        self.ui.table_jogos.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.table_jogos.cellDoubleClicked.connect(self.ligar_jogo)

        #self.screen_size = QDesktopWidget().screenGeometry(-1)

        #HALPPPPPPP
        #self.ui.resize(self.screen_size.width(),self.screen_size.height())

        self.link_to_ace = "" # link for the ace streamer

        for i in range(len(self.data_json["days_to_Select"])):
            self.ui.select_days.addItem(self.data_json["days_to_Select"][i])
        
        self.ui.select_days.currentTextChanged.connect(self.jogos)

        self.jogos()

    def jogos(self):
        self.ui.table_jogos.setRowCount(0);
        for i in self.data_json["games"]:
            if self.data_json["games"][i]["date"] == self.data_json["days_to_Select"][self.ui.select_days.currentIndex()]:
                rowPos = self.ui.table_jogos.rowCount()
                self.ui.table_jogos.insertRow(rowPos)
                #self.ui.table_jogos.setItem(rowPos, 0, QTableWidgetItem(self.data_json["games"][i]["date"]))
                self.ui.table_jogos.setItem(rowPos, 0, QTableWidgetItem(self.data_json["games"][i]["time"]))
                self.ui.table_jogos.setItem(rowPos, 1, QTableWidgetItem(self.data_json["games"][i]["type"]))
                self.ui.table_jogos.setItem(rowPos, 2, QTableWidgetItem(self.data_json["games"][i]["league"]))
                self.ui.table_jogos.setItem(rowPos, 3, QTableWidgetItem(self.data_json["games"][i]["players"]))
                if "language" in self.data_json["games"][i]:
                    if self.data_json["games"][i]["language"] == "[POR]":
                        ling = QTableWidgetItem(self.data_json["games"][i]["language"])
                        ling.setBackground(QColor(255,255,0))
                        self.ui.table_jogos.setItem(rowPos, 4, ling)
                    else:
                        self.ui.table_jogos.setItem(rowPos, 4, QTableWidgetItem(self.data_json["games"][i]["language"]))
                else:
                    self.ui.table_jogos.setItem(rowPos, 4, QTableWidgetItem("UnKnown"))
                
                if "Channels" in self.data_json["games"][i]:
                    if len(self.data_json["games"][i]["Channels"]) is 2:
                        canal1 = QTableWidgetItem("CANAL " + str(self.data_json["games"][i]["Channels"][0][1]))
                        canal2 = QTableWidgetItem("CANAL " + str(self.data_json["games"][i]["Channels"][1][1]))
                        
                        #MUDAR A COR DA FONT E AUMENTAR LA
                        canal1.setBackground(QColor(0,255,0))
                        canal2.setBackground(QColor(0,255,0))
                        
                        self.ui.table_jogos.setItem(rowPos, 5, canal1)
                        self.ui.table_jogos.setItem(rowPos, 6, canal2)
                    else:
                        canal1 = QTableWidgetItem("CANAL " + str(self.data_json["games"][i]["Channels"][0][1]))
                        canal1.setBackground(QColor(0,255,0))
                        canal2 = QTableWidgetItem("None")
                        canal2.setBackground(QColor(255,0,0))
                        self.ui.table_jogos.setItem(rowPos, 5, QTableWidgetItem(canal1))
                        
                        self.ui.table_jogos.setItem(rowPos, 6, QTableWidgetItem(canal2))
                else:
                    canal = QTableWidgetItem("None")
                    canal.setBackground(QColor(255,0,0))
                    self.ui.table_jogos.setItem(rowPos, 5, QTableWidgetItem(canal))
                    self.ui.table_jogos.setItem(rowPos, 6, QTableWidgetItem(canal))
        self.ui.table_jogos.resizeColumnsToContents()

    def procura_jogo(self):
        if self.ui.procurar_jogo_texto.text() is not "":
            self.ui.table_jogos.setRowCount(0);
            for i in self.data_json["games"]:
                if self.data_json["games"][i]["date"] == self.data_json["days_to_Select"][self.ui.select_days.currentIndex()]:
                    if self.ui.procurar_jogo_texto.text().upper() in self.data_json["games"][i]["players"]: #VERIFICA ISTO AQUI FICOU AQUI
                        rowPos = self.ui.table_jogos.rowCount()
                        self.ui.table_jogos.insertRow(rowPos)
                        #self.ui.table_jogos.setItem(rowPos, 0, QTableWidgetItem(self.data_json["games"][i]["date"]))
                        self.ui.table_jogos.setItem(rowPos, 0, QTableWidgetItem(self.data_json["games"][i]["time"]))
                        self.ui.table_jogos.setItem(rowPos, 1, QTableWidgetItem(self.data_json["games"][i]["type"]))
                        self.ui.table_jogos.setItem(rowPos, 2, QTableWidgetItem(self.data_json["games"][i]["league"]))
                        self.ui.table_jogos.setItem(rowPos, 3, QTableWidgetItem(self.data_json["games"][i]["players"]))
                        if "language" in self.data_json["games"][i]:
                            if self.data_json["games"][i]["language"] == "[POR]":
                                ling = QTableWidgetItem(self.data_json["games"][i]["language"])
                                ling.setBackground(QColor(255,255,0))
                                self.ui.table_jogos.setItem(rowPos, 4, ling)
                            else:
                                self.ui.table_jogos.setItem(rowPos, 4, QTableWidgetItem(self.data_json["games"][i]["language"]))
                        else:
                            self.ui.table_jogos.setItem(rowPos, 4, QTableWidgetItem("UnKnown"))
                        
                        if "Channels" in self.data_json["games"][i]:
                            if len(self.data_json["games"][i]["Channels"]) is 2:
                                canal1 = QTableWidgetItem("CANAL " + str(self.data_json["games"][i]["Channels"][0][1]))
                                canal2 = QTableWidgetItem("CANAL " + str(self.data_json["games"][i]["Channels"][1][1]))
                                
                                #MUDAR A COR DA FONT E AUMENTAR LA
                                canal1.setBackground(QColor(0,255,0))
                                canal2.setBackground(QColor(0,255,0))
                                
                                self.ui.table_jogos.setItem(rowPos, 5, canal1)
                                self.ui.table_jogos.setItem(rowPos, 6, canal2)
                            else:
                                canal1 = QTableWidgetItem("CANAL " + str(self.data_json["games"][i]["Channels"][0][1]))
                                canal1.setBackground(QColor(0,255,0))
                                canal2 = QTableWidgetItem("None")
                                canal2.setBackground(QColor(255,0,0))
                                self.ui.table_jogos.setItem(rowPos, 5, QTableWidgetItem(canal1))
                                
                                self.ui.table_jogos.setItem(rowPos, 6, QTableWidgetItem(canal2))
                        else:
                            canal = QTableWidgetItem("None")
                            canal.setBackground(QColor(255,0,0))
                            self.ui.table_jogos.setItem(rowPos, 5, QTableWidgetItem(canal))
                            self.ui.table_jogos.setItem(rowPos, 6, QTableWidgetItem(canal))
        self.ui.table_jogos.resizeColumnsToContents()

    def ligar_jogo(self):       
        col = self.ui.table_jogos.currentItem().column()
        if col is 5 or col is 6: 
            row = self.ui.table_jogos.currentItem().row()
            text = self.ui.table_jogos.item(row,col).text()
            if not (text == "None"):
                if col is 5:
                    url = self.data_json["games"]["game" + str(row + 1)]["Channels"][0][0]
                elif col is 6:
                    url = self.data_json["games"]["game" + str(row + 1)]["Channels"][1][0]
                self.link_to_ace = get_data.get_link_to_ace_streamer(self.data_json["session"], url)
                call(["ace_player",self.link_to_ace])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = game_viewer()
    window.show()
    sys.exit(app.exec_())
