from dijkstra import *
class nodo:
    def __init__(self, posx, posy, valor):
        self.posx = posx
        self.posy = posy
        self.valor = valor
        self.adyacente = []

    def Agregar_adyacente(self, valor,peso):
            self.adyacente.append([valor,peso])

    def Get_Adyacente(self):
        return self.adyacente

    def BuscarP(self,valor):
        for i in self.adyacente:
            if valor==i[0]:
                return i[1]
    

class Grafo:
    
    def __init__(self):
        self.nodos = []
        self.listaAd=[]
        self.colaparejas=[]
        self.arista=[]

    def Crear_grafo(self):
        corrido=1
        for i in range(len(self.listaAd)):
            aux=self.nodos[i]
            for j in range(len(self.listaAd[i])):
                if self.listaAd[i][j]!=99:
                    pareja={aux,self.nodos[corrido+j]}
                    pareja2=(aux.valor,self.nodos[corrido+j].valor,self.listaAd[i][j])
                    aux.Agregar_adyacente(self.nodos[corrido+j],self.listaAd[i][j])
                    if pareja not in self.colaparejas:
                        self.colaparejas.append(pareja)
                        self.arista.append(pareja2)
            corrido+=1        
            

    def ImprimirGrafo(self):
        palabra=''
        for i in self.nodos:
            palabra+= str(i.valor)+','
        return palabra  

    def AlgDijkstra(self):
        gr=Grafica()
        caminos=[]
        for i in self.nodos:
            gr.agregarVertice(i.valor)
        for i in self.arista:
            gr.agregarArista(i[0], i[1], i[2])
        gr.dijkstra(1)
        for i in range(1,len(self.nodos)+1):
            caminos.append(gr.camino(1, i))
        return caminos

    def AlgPrim(self,nodo,cola,visitados,listaordenada):
        if len(visitados)==len(self.nodos):
            
            return cola
        else:
            pos=[]
            if nodo not in visitados:
                visitados.append(nodo)
                for i in  self.arista:
                    if nodo == i[0] or nodo==i[1]:
                        listaordenada.append(self.arista[self.arista.index(i)])
                        pos.append(self.arista.index(i))
                for i in pos:
                    self.arista[i]=(0,0,0)
                listaordenada=self.ordenarpeso(listaordenada)    
                arista=listaordenada.pop(0)
                if arista[0] not in visitados or arista[1] not in visitados:
                    cola.append(arista)
                if arista[0] not in  visitados:
                    return self.AlgPrim(arista[0],cola,visitados,listaordenada)
                else:
                    return self.AlgPrim(arista[1],cola,visitados,listaordenada)
            
            else:
                listaordenada=self.ordenarpeso(listaordenada)
                arista=listaordenada.pop(0)
                if arista[0] not in visitados or arista[1] not in visitados:
                    cola.append(arista)        
                if arista[0] not in  visitados:
                    return self.AlgPrim(arista[0],cola,visitados,listaordenada)
                else:
                    return self.AlgPrim(arista[1],cola,visitados,listaordenada)
            
        """
        if len(listaordenada)==0 and len(visitados)== self.nodos:
            return cola
        else:
            if nodo not in visitados:
                visitados.append(nodo)
                print("#",nodo.valor)
                for i in nodo.Get_Adyacente():
                    lista=(nodo,i[0],i[1])
                    print(nodo.valor,i[0].valor,i[1])   
                    listaordenada.append(lista)
                listaordenada=self.ordenarpeso(listaordenada)
                if len(listaordenada)>0:   
                    arista=listaordenada.pop(0)
                    if arista[1] not in visitados:
                        print(arista[0].valor,arista[1].valor)
                        cola.append(arista)
                        return self.AlgPrim(arista[1],cola,visitados, listaordenada)
                    else:
                        listaordenada=self.ordenarpeso(listaordenada)
                        arista=listaordenada.pop(0)
                        return self.AlgPrim(arista[1],cola,visitados, listaordenada)

                else:
                     return self.AlgPrim(nodo,cola,visitados, listaordenada)      
            else:
                listaordenada=self.ordenarpeso(listaordenada)   
                arista=listaordenada.pop(0)
                return self.AlgPrim(arista[1],cola,visitados, listaordenada)
         """       



    def ordenarpeso(self,lista_nodo):
        if len(lista_nodo)>0:
            aux=lista_nodo[0][2]
            pos=-1
            for i in range(1,len(lista_nodo)):
                if (lista_nodo[i])[2]<aux:
                    aux=(lista_nodo[i])[2]
                    pos=i
            if pos!=-1:
                elemento=lista_nodo.pop(pos)
                lista_nodo.insert(0,elemento) 
        return lista_nodo            
        
            
    
    def Set_nodos(self,valor):
        self.nodos=valor

    def Set_listaAd(self,valor):
        self.listaAd=valor    

    def Get_nodosD(self):
        return self.colaparejas

    def Get_Arista(self):
        return self.arista

