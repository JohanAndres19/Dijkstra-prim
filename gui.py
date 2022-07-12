import sys
from PyQt5.QtGui import QTextOption ,QPalette,QPainter, QColor, QPen, QBrush, QImage
from  PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt
from qt_for_python.uic.ventanaR import *
from qt_for_python.uic.ventanaE import *
from qt_for_python.uic.ventanG import *
from Logica import *;
import networkx as nx

from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


#-------------------------------------
#------------- Interfaz---------------

class Ventana_principal(QMainWindow):
    
    def __init__(self,modelo):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.modelo=modelo
        self.controlador=Controlador(self)
        self.canvas =Lienzo(self.ui.Contenedor)
        self.canvas.setStyleSheet("background: white;\n  border: 3px solid; \n border-radius:15px")
        #-------------------------------------------
        self.ui.boton_Borrarpuntos
        self.ui.boton_Dibujar
        self.ui.boton_Lista

    def Get_modelo(self):
        return self.modelo
    
    def Get_Lienzo(self):
        return self.canvas

class Lienzo(QFrame):
    def __init__(self,parent):
        super().__init__(parent=parent)      
        self.resize(parent.width(),parent.height())
        self.posicion =[]
        self.presionado=False
        self.No_dibujar=False
        self.dibujar_lineas=False
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

    def mousePressEvent(self,event):
        if ( event.buttons() & Qt.LeftButton) and not self.No_dibujar:
            self.posicion.append((event.pos().x(),event.pos().y()))
            self.presionado=True
        self.update()    
            
    def paintEvent(self, event):
        painter = QPainter()
        painter.drawImage(self.rect(),self.image, self.image.rect())
        if self.presionado and not self.dibujar_lineas:
            painter.begin(self)
            painter.setBrush(QBrush(Qt.blue, Qt.SolidPattern))
            pincel =QPen(Qt.blue,8)
            pincel2=QPen(Qt.white)
            painter.setPen(pincel)
            cantidad=0
            for i in self.posicion:
                painter.drawEllipse(i[0],i[1], 20, 20)
            painter.setPen(pincel2)            
            for i in self.posicion:
                cantidad+=1
                painter.drawText(i[0]+3,i[1]+3,11,14,Qt.AlignHCenter,str(cantidad))
            painter.end()
        elif self.dibujar_lineas:
            painter.begin(self)
            painter.setBrush(QBrush(Qt.blue, Qt.SolidPattern))
            pincel =QPen(Qt.blue,8)
            pincel2=QPen(Qt.white)
            painter.setPen(pincel)
            cantidad=0
            for i in self.posicion:
                painter.drawEllipse(i[0],i[1], 20, 20)
            painter.setPen(pincel2)            
            for i in self.posicion:
                cantidad+=1
                painter.drawText(i[0]+4,i[1]+3,10,12,Qt.AlignHCenter,str(cantidad))
            pincel3=QPen(Qt.blue,2)
            painter.setPen(pincel3)
            for i in self.nodos:
                aux= list(i)
                painter.drawLine(aux[0].posx+3, aux[0].posy+5, aux[1].posx+3,aux[1].posy+5)
            painter.end()        
        
    def DibujarAyacente(self,nodos,arista):
        self.nodos=nodos
        self.aristas=arista
        self.dibujar_lineas=True
        self.update()
        
    def Limpiar(self):
        self.image.fill(Qt.white)
        self.presionado=False
        self.No_dibujar=False
        self.dibujar_lineas=False
        self.posicion.clear()
        self.update()

    def Set_presionado(self,valor):
        self.presionado=valor

    def Set_NoDibujar(self,valor):
        self.No_dibujar=valor

    def Get_NoDibujar(self):
        return self.No_dibujar

class Dialogo(QDialog):
    def __init__(self,modelo):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.controlador = ContoladorD(self)
        self.modelo=modelo
       # self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.tableWidget.verticalHeader().setVisible(False)
    def Get_modelo(self):
        return self.modelo    

class GraficaArbol(QMainWindow):
    
    def __init__(self,modelo):
        super().__init__()
        self.ui = Ui_ventanG()
        self.ui.setupUi(self)
        self.modelo=modelo
        self.controlador=ControladorA(self)
        self.canvas = CanvasGrafo(self.ui.frame_2)
        self.canvas.setStyleSheet("background: white;\n  border: 3px solid; \n border-radius:15px")
        
        
    def Get_modelo(self):
        return self.modelo

class CanvasGrafo(QFrame):
    def __init__(self,parent):
        super().__init__(parent=parent)      
        self.resize(parent.width(),parent.height())
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.dibujarD=False
    
    def paintEvent(self, event):
        painter = QPainter()
        painter.drawImage(self.rect(),self.image, self.image.rect())
        if self.dibujarD:
            painter.begin(self)
            painter.setBrush(QBrush(Qt.blue, Qt.SolidPattern))
            pincel =QPen(Qt.blue,8)
            pincel2=QPen(Qt.white)
            painter.setPen(pincel)
            for i in self.nodo:
                painter.drawEllipse(i.posx,i.posy, 20, 20)
            painter.setPen(pincel2)            
            for i in self.nodo:
                painter.drawText(i.posx+4,i.posy+3,10,12,Qt.AlignHCenter,str(i.valor))
            pincel3=QPen(Qt.blue,2)
            painter.setPen(pincel3)
            for i in self.camino:
                painter.drawLine(self.nodo[i[0]-1].posx+3, self.nodo[i[0]-1].posy+5, self.nodo[i[1]-1].posx+3,self.nodo[i[1]-1].posy+5)
            pincel4 =QPen(Qt.black,5)
            painter.setPen(pincel4)
            for i in self.camino:
                x=int((self.nodo[i[0]-1].posx+self.nodo[i[1]-1].posx)//2)
                y=int((self.nodo[i[0]-1].posy+self.nodo[i[1]-1].posy)//2)
                painter.drawText(x+6,y+8,10,12,Qt.AlignHCenter,str(i[2]))
            painter.setPen(pincel4)            
            painter.end()            
    
    def DibujarDi(self,camino,nodos):
        self.dibujarD=True
        self.nodo=nodos
        self.camino=camino
        self.update()

    
#--------------------------------------
#------------controlador---------------

class Controlador():
    def __init__(self,ventana):
        self.ventana =ventana
        self.Eventos()

    def Eventos(self):
        self.ventana.ui.boton_Borrarpuntos.clicked.connect(lambda: self.ventana.Get_modelo().BorrarPuntos())
        self.ventana.ui.boton_Dibujar.clicked.connect(lambda :self.ventana.Get_modelo().Dibujar())
        self.ventana.ui.boton_Lista.clicked.connect(lambda : self.ventana.Get_modelo().Lista())
 
class ContoladorD:
    def __init__(self,ventana):
        self.ventana=ventana
        self.Eventos()

    def Eventos(self):
        self.ventana.ui.boton_Agregar.clicked.connect(lambda:self.ventana.Get_modelo().Agregar())

class ControladorA:

    def __init__(self,ventana):
        self.ventana=ventana
        self.Eventos()

    def Eventos(self):
        self.ventana.ui.boton_dibujar.clicked.connect(lambda:self.ventana.Get_modelo().DibujarArbol())

#---------------------------------------
#---------------Modelo-----------------

class Modelo ():
    def __init__(self) :
        self.ventana = Ventana_principal(self)
        self.dialogo =Dialogo(self)
        self.VentanaG = GraficaArbol(self)
        self.nodos=[]
        self.grafo=None 
        self.contarclicks=0
        self.Arboldikjstra=None
        self.ArbolPrim=None
    
    def setArbolDikjstra(self,valor):
        self.Arboldikjstra=valor
    def setArbolPrim(self,valor):
        self.ArbolPrim=valor
    
    def getArbolDikjstra(self):
       return self.Arboldikjstra
    
    def getArbolPrim(self):
       return self.ArbolPrim

    def BorrarPuntos(self):
       self.ventana.Get_Lienzo().Limpiar()

    def Dibujar(self):
        if self.grafo != None:
            self.VentanaG.ui.comboBox.clear()
            self.VentanaG.ui.comboBox.addItems([" ","DIJKSTRA","PRIM"])
            self.VentanaG.show()

    def DibujarArbol(self):
        if  self.contarclicks==0:
            if self.VentanaG.ui.comboBox.currentIndex()==1 :
                visitados=[]
                recorrido=[]
                aux=0
                ca_d=self.grafo.AlgDijkstra()
                visitados.append(((ca_d[0])[0])[0])
                ca_d.pop(0)
                print(ca_d)
                for i in ca_d:
                    for j in i[0]:
                        if j in visitados:
                            aux=j       
                        else:
                            visitados.append(j)
                            recorrido.append((aux,j,i[1]))    
                self.setArbolDikjstra(recorrido)
                self.VentanaG.canvas.DibujarDi(recorrido,self.nodos)
            elif self.VentanaG.ui.comboBox.currentIndex()==2:
                self.setArbolPrim(self.grafo.AlgPrim(self.nodos[0].valor, [], [], [])) 
                self.VentanaG.canvas.DibujarDi(self.getArbolPrim(), self.nodos)
        else:
            if self.VentanaG.ui.comboBox.currentIndex()==1 :
                 self.VentanaG.canvas.DibujarDi(self.getArbolDikjstra(),self.nodos)
            elif self.VentanaG.ui.comboBox.currentIndex()==2:
                 self.VentanaG.canvas.DibujarDi(self.getArbolPrim(), self.nodos)
        self.contarclicks+=1         
    
    def Lista(self):
        if len(self.ventana.Get_Lienzo().posicion)>0:
            self.ventana.Get_Lienzo().Set_NoDibujar(True)
            if self.dialogo.ui.tableWidget.rowCount()!=0:
                self.dialogo.ui.tableWidget.clearContents()
                self.dialogo.ui.tableWidget.setRowCount(0)
            self.dialogo.ui.tableWidget.setColumnCount(len(self.ventana.Get_Lienzo().posicion)+1)
            self.dialogo.show()
            label_en_y=["nodos"]
            for i in range(len(self.ventana.Get_Lienzo().posicion)):
                label_en_y.append(("nodo "+ str(i+1)))
            self.dialogo.ui.tableWidget.setHorizontalHeaderLabels(label_en_y)
            self.dialogo.ui.tableWidget.setColumnWidth(0,50)
            for i in range(len(self.ventana.Get_Lienzo().posicion)):
                self.dialogo.ui.tableWidget.insertRow(i)
                celda= QTableWidgetItem(str(i+1))
                celda.setTextAlignment(Qt.AlignHCenter)
                self.dialogo.ui.tableWidget.setItem(i, 0, celda)
            for i in range(len(self.ventana.Get_Lienzo().posicion)):
                self.dialogo.ui.tableWidget.setColumnWidth(i+1,60)
                for j in range(len(self.ventana.Get_Lienzo().posicion)):
                    aux=QLineEdit()
                    aux.setAlignment((Qt.AlignHCenter))
                    if (i-j)>=0:
                        aux.setText("X")
                        aux.setEnabled(False)
                    else:
                        aux.setValidator(QtGui.QIntValidator())
                    self.dialogo.ui.tableWidget.setCellWidget(i,j+1,aux)
        else:
            QMessageBox.warning(self.dialogo, " ADVERTENCIA ", " POR FAVOR UBIQUE LOS NODOS PRIMERO ")

    def Agregar(self):
        matriz=[]
        valido=True
        for i in range(self.dialogo.ui.tableWidget.rowCount()):
            aux=[]
            for j in range(1,self.dialogo.ui.tableWidget.columnCount()):
                fila=self.dialogo.ui.tableWidget.cellWidget(i, j).text()
                if len(fila)==0:
                    QMessageBox.warning(self.dialogo, "  ADVERTENCIA  ", "Verifique los valores")
                    valido=False
                    break
                if fila!="X":
                    aux.append(int(fila))    
            if not valido :
                break
            matriz.append(aux)
        if valido :
            self.dialogo.close()
            for i in range(self.dialogo.ui.tableWidget.rowCount()):
                self.nodos.append(nodo(self.ventana.Get_Lienzo().posicion[i][0],self.ventana.Get_Lienzo().posicion[i][1],i+1))
            self.grafo=Grafo()
            self.grafo.Set_nodos(self.nodos)
            self.grafo.Set_listaAd(matriz)
            self.grafo.Crear_grafo()
            self.ventana.Get_Lienzo().DibujarAyacente(self.grafo.Get_nodosD(),self.grafo.Get_Arista())    
               
    def Get_ventana(self):
        return self.ventana

#--------------------------------------
#---------------Main------------------- 

if __name__ =="__main__":
    app =QApplication(sys.argv)
    gui = Modelo().Get_ventana()
    gui.show()
    sys.exit(app.exec_())
