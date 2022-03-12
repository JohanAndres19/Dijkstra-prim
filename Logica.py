class nodo:
    def __init__(self, posx, posy, valor):
        self.posx = posx
        self.posy = posy
        self.valor = valor
        self.adyacente = []

    def Agregar_adyacente(self, valor):
        if len(self.adyacente) == 0:
            self.adyacente.append(valor)
        else:
            if not self.isinlista(valor):
                self.adyacente.append(valor)

    def isinlista(self, nodo):
        for i in self.adyacente:
            if i.valor == nodo.valor:
                return True
        return False

class Grafo:
    def __init__(self):
        self.nodos = []
        self.listaAd=[]
        self.colaparejas=[]

    def Crear_grafo(self):
        for i in range(len(self.nodos)):
            aux=self.nodos[i]
            for j in  self.listaAd[i]:
                pareja={aux,self.nodos[int(j)-1]}
                aux.Agregar_adyacente(self.nodos[int(j)-1])
                if pareja not in self.colaparejas:
                    self.colaparejas.append(pareja)

    def ImprimirGrafo(self):
        palabra=''
        for i in self.nodos:
            palabra+= str(i.valor)+','
        return palabra  

    def RecorridoA(self,nodo):
        visitados=[]
        visitados.append(nodo)
        cola=[]
        colaArbol=[]
        cola.append(nodo)
        arbol=Arbol(nodo.valor)
        colaArbol.append(arbol)
        while len(cola)>0:
            aux=cola.pop(0)
            actual=colaArbol.pop(0)
            for i in aux.adyacente :
                if i not in visitados: 
                    cola.append(i)
                    visitados.append(i)    
                    actual.add_Componente(Arbol(i.valor))
                    colaArbol.append(actual.Get_componente(len(actual.Get__Partes())-1))
        return arbol

    def RecorridoP(self,nodo,visitado):
        visitado.append(nodo)
        arbol=Arbol(nodo.valor)
        for i in nodo.adyacente:
            if i not in visitado:
                arbol.add_Componente(self.RecorridoP(i, visitado))
        return arbol        
    
    def Set_nodos(self,valor):
        self.nodos=valor

    def Set_listaAd(self,valor):
        self.listaAd=valor    

    def Get_nodosD(self):
        return self.colaparejas

class Arbol():
    
    def __init__(self,valor):
       self.partes=[]
       self.valor=valor
       
    def operacion(self):
        cad = str(self.valor)+"("
        for i in self.partes:
            cad+=i.operacion()+","
        cad= cad[0:len(cad)]+")"
        return cad   

    def add_Componente(self,componente):
        self.partes.append(componente)   

    def Get__Partes(self):
        return self.partes

    def Get_componente(self,valor=0):
        if len(self.partes)>0:
            return self.partes[valor]
        else:
            return 0         

    def Get_Padre(self):
        return self.padre




