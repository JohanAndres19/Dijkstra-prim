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
        
    def DibujarAyacente(self,nodos):
        self.nodos=nodos
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
        self.canvas2 = MplCanvas(self.ui.frame_2)
        self.canvas2.setGeometry(0, 0, self.ui.frame_2.width(),self.ui.frame_2.height())
        
    def Get_modelo(self):
        return self.modelo

class MplCanvas(FigureCanvas):
    
    def __init__(self, parent=None):
        self.figure = plt.figure()
        FigureCanvas.__init__(self,self.figure)
        FigureCanvas.updateGeometry(self)
        self.setParent(parent)
        """
        self.axes = fig.add_subplot(111)
        FigureCanvas .__init__(self, fig) # Inicializa la clase padre
        """
        """
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        """

    def dibujar(self,gr,pos):
        self.figure.clf()
        nx.draw(gr, pos, with_labels=True, arrows=True)
        self.draw_idle()

class PlotCanvas(
    FigureCanvas): # Al heredar la clase FigureCanvas, esta clase es un QQidget PyQt5 y un FigureCanvas matplotlib. Esta es la clave para conectar pyqt5 con matplotlib.
 
    def __init__(self, parent=None, width=500, height=500, dpi=100):
        self.fig = plt.figure() # Crear una figura, nota: la figura es una figura debajo de matplotlib, no una figura debajo de matplotlib.pyplot
         # Llame al método add_subplot en la figura, similar al método subplot en matplotlib.pyplot
 
        FigureCanvas .__init__(self, self.fig) # Inicializa la clase padre
        self.setParent(parent)
        """
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        """
        FigureCanvas.updateGeometry(self)
    
    def dibujar(self,gr,pos):
        self.fig.clf()
        nx.draw(gr, pos, with_labels=True, arrows=True)
        self.draw_idle()

class Grafica:
    def __init__(self):
        self.G = nx.DiGraph()

    def Graficar(self,nodo):
        self.Grafica_arbol(nodo)        
        self.pos =graphviz_layout(self.G, prog='dot')
        return self.pos

            
    def Grafica_arbol(self,nodo):                
        if not self.G.has_node(nodo.valor):
            self.G.add_node(nodo.valor) 
        for i in nodo.Get__Partes():
            if not self.G.has_node(i.valor):
                self.G.add_node(i.valor)
                self.G.add_edge(nodo.valor,i.valor)
                self.Grafica_arbol(i)
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
    
    def BorrarPuntos(self):
       self.ventana.Get_Lienzo().Limpiar()

    def Dibujar(self):
        if self.grafo != None:
            items=[" "]
            for i in self.grafo.nodos:
                 items.append("nodo "+str(i.valor))
            self.VentanaG.ui.comboBox.addItems(items)
            self.VentanaG.ui.comboBox_2.addItems([" ","RECORRIDO EN ANCHURA","RECORRIDO EN PROFUNDIDAD"])
            self.VentanaG.show()

    def DibujarArbol(self):
        if self.VentanaG.ui.comboBox.currentIndex()!=0:
            g1=Grafica()
            if self.VentanaG.ui.comboBox_2.currentIndex()==1 :
                print("esta entrando")          
                pos1=g1.Graficar(self.grafo.RecorridoA(self.nodos[self.VentanaG.ui.comboBox.currentIndex()-1]))
                self.VentanaG.canvas2.dibujar(g1.G, pos1)
            elif self.VentanaG.ui.comboBox_2.currentIndex()==2: 
                pos1=g1.Graficar(self.grafo.RecorridoP(self.nodos[self.VentanaG.ui.comboBox.currentIndex()-1],[]))
                self.VentanaG.canvas2.dibujar(g1.G, pos1)
            
    
    def Lista(self):
        if len(self.ventana.Get_Lienzo().posicion)>0:
            self.ventana.Get_Lienzo().Set_NoDibujar(True)
            self.dialogo.ui.tableWidget.setColumnCount(len(self.ventana.Get_Lienzo().posicion))
            self.dialogo.show()
            label_en_y=["nodos"]
            for i in range(len(self.ventana.Get_Lienzo().posicion)):
                label_en_y.append(("nodo "+ str(i+1)))
            print(label_en_y)
            self.dialogo.ui.tableWidget.setHorizontalHeaderLabels(label_en_y)
            if self.dialogo.ui.tableWidget.rowCount()!=0:
                self.dialogo.ui.tableWidget.clearContents()
                self.dialogo.ui.tableWidget.setRowCount(0)
            for i in range(len(self.ventana.Get_Lienzo().posicion)):
                self.dialogo.ui.tableWidget.insertRow(i)
                celda= QTableWidgetItem(str(i+1))
                self.dialogo.ui.tableWidget.setItem(i, 0, celda)
                aux=QLineEdit()
                self.dialogo.ui.tableWidget.setColumnWidth(1,30)
                self.dialogo.ui.tableWidget.setCellWidget(i,1,aux)
        else:
            QMessageBox.warning(self.dialogo, " ADVERTENCIA ", " POR FAVOR UBIQUE LOS NODOS PRIMERO ")

    def Agregar(self):
        matriz=[]
        valido=True
        for i in range(self.dialogo.ui.tableWidget.rowCount()):
            fila=self.dialogo.ui.tableWidget.cellWidget(i, 1).text()
            if len(fila)==0:
                QMessageBox.warning(self.dialogo, "  ADVERTENCIA  ", "Verifique los valores")
                valido=False
                break
            matriz.append(fila.split(","))
        if valido :
            self.dialogo.close()    
            for i in range(self.dialogo.ui.tableWidget.rowCount()):
                self.nodos.append(nodo(self.ventana.Get_Lienzo().posicion[i][0],self.ventana.Get_Lienzo().posicion[i][1],i+1))
            self.grafo=Grafo()
            self.grafo.Set_nodos(self.nodos)
            self.grafo.Set_listaAd(matriz)
            self.grafo.Crear_grafo()
            self.ventana.Get_Lienzo().DibujarAyacente(self.grafo.Get_nodosD())    

        
    def Get_ventana(self):
        return self.ventana

#--------------------------------------
#---------------Main------------------- 

if __name__ =="__main__":
    app =QApplication(sys.argv)
    gui = Modelo().Get_ventana()
    gui.show()
    sys.exit(app.exec_())
