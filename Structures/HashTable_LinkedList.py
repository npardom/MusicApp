# Hash Table con direccionamiento abierto
from Structures.LinkedListStructures import LinkedList

# Contiene el key y el value
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        
# Tabla Hash
class HashTable:
    
    def __init__(self,capacity = 50):
        self.capacity = capacity
        self.size = 0
        self.buckets = [None]*self.capacity
    
    # función hash
    def hashFunction(self, key):
        idx = 0
        pos = 1
        for character in key:
            idx += (ord(character)+len(key))*pos
            pos+=1
        return idx % self.capacity
        
    # función insert --> inserta un key y le asigna un value
    def insert(self, key, value):
        self.size += 1

        # se obtiene el idx según la función hashFunction
        idx = self.hashFunction(key)

        # se obtiene la listaEnlazada (si la hay) en dicho idx
        linkedList = self.buckets[idx]

        # Si aún no hay lista enlazada
        if linkedList is None:
            # Se crea la lista enlazada y se inserta (key,value)
            self.buckets[idx] = LinkedList()
            self.buckets[idx].add(0,Node(key, value))
            return
        
        # Si hay más de un elemento en dicho idx, se inserta al final de la lista enlazada
        sizeLinkedList = self.buckets[idx].getSize()
        if not self.contains(key):
            self.buckets[idx].add(sizeLinkedList,Node(key, value))
        
    # Función find --> encuentra el (value) correspondiente al (key)
    def find(self, key):
        # se obtiene el idx según la función hashFunction
        idx = self.hashFunction(key)

        # se obtiene la listaEnlazada (si la hay) en dicho idx
        linkedList = self.buckets[idx]
        currentNode = None

        # Si hay elementos en dicho idx, el currentNode será el que esté en la cabeza de la lista
        if linkedList != None:
            currentNode = linkedList.head
        
        # Mientras hayan elementos en dicho idx, y la llave ingresada sea distinta a la de currentNode, se itera 
        try:
            while linkedList is not None and currentNode.element.key != key:
                currentNode = currentNode.next              
        # Si currentNode es None, retorna None
        except:
            return

        # Si (luego de iterar) no se encuentra (key), retorna None
        if currentNode is None:
            return None
        # Encuentra (key) --> devuelve (value)
        else:
            return currentNode.element.value

    #Función contains --> verifica si un (key) dado está en la HashTable 
    def contains(self,key):
        result = self.find(key)
        if result is None:
            return False
        else:
            return True

    #Función hashTableFromArray --> crea un HashTable partiendo de un array
    def hashTableFromArray(self,array):
        while len(array)!=0:
            key = array.pop(0)
            value = array.pop(0)
            self.insert(key,value)
        
    # Función remove --> elimina la pareja (key, value) dado un (key)
    def remove(self, key):
        # Se obtiene el idx según la función hashFunction
        idx = self.hashFunction(key)

        # Se obtiene la listaEnlazada (si la hay) en dicho idx
        linkedList = self.buckets[idx]
        currentNode=None
        # Counter para eliminar el elemento
        idxDeleted=0   

        # Si hay elementos en dicho idx, el currentNode será el que esté en la cabeza de la lista 
        if linkedList!=None:
            currentNode=linkedList.head
        
        # Mientras hayan elementos en dicho idx, y la llave ingresada sea distinta a la de currentNode, se itera 
        try:
            while linkedList is not None and currentNode.element.key != key:
                idxDeleted +=1
                currentNode = currentNode.next
        # Si currentNode es None, retorna None
        except:
            return

        # Si (luego de iterar) no se encuentra (key), retorna None
        if currentNode is None:
            return None
        # Encuentra (key) --> elimina (key,value)
        else:
            self.size -= 1

            #Si la lista tiene 1 solo elemento, se elimina la lista 
            if linkedList.getSize()==1:
                self.buckets[idx] = None
            #Si la lista tiene más de un elemento, se elimina el del idxDeleted
            else:
                linkedList.remove(idxDeleted)

            # Retorna (value)
            return currentNode.element.value
            