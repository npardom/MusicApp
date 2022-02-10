import random
import numpy as np
# Hash Table con direccionamiento abierto
# Con linear probing

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
        self.buckets = np.empty(capacity,Node)
    
    # función hash (linear probing)
    def hashFunction(self,key,increment):
        idx=0
        for char in key:
            idx+=ord(char)
        return (idx+increment)%self.capacity 

    # función insert --> inserta un key y le asigna un value
    def insert(self, key, value):
        # Counter del hashing
        timesHashIsCalled = 0

        while self.size < self.capacity:
            # se obtiene el idx según la función hashFunction
            idx = self.hashFunction(key,timesHashIsCalled)
            
            # se obtiene el elemento (si lo hay) en dicho idx
            elem = self.buckets[idx]

            # si la posición está vacía
            if elem is None:
                # Inserta (key,value) en ese idx y retorna
                self.buckets[idx] = Node(key,value)
                self.size += 1
                return
            #Si hay elementos en el idx, se hace hashing
            else:
                timesHashIsCalled+=1
        
        raise Exception("The Hash Table has reached it's capacity.")
    
    # Función find --> encuentra el (value) correspondiente al (key)
    def find(self, key):
        # Counter del hashing
        timesHashIsCalled = 0

        while True:
            # se obtiene el idx según la función hashFunction
            idx = self.hashFunction(key,timesHashIsCalled)
            
            # se obtiene el elemento (si lo hay) en dicho idx
            elem = self.buckets[idx]

            # si la posición está vacía ó el hashTable esté lleno
            if elem is None or timesHashIsCalled > self.capacity:
                return
            # si la llave coincide, retorna el (value) de dicha (key)
            elif elem.key == key:
                return elem.value
            #Si hay elementos en el idx, se hace hashing
            else:
                timesHashIsCalled+=1
    
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
    def remove(self,key):
        # Counter del hashing
        timesHashIsCalled = 0

        while True:
            # se obtiene el idx según la función hashFunction
            idx = self.hashFunction(key,timesHashIsCalled)
            
            # se obtiene el elemento (si lo hay) en dicho idx
            elem = self.buckets[idx]

            # si la posición está vacía ó el hashTable esté lleno
            if elem is None or timesHashIsCalled > self.capacity:
                return
            # si la llave coincide, elimina el elemento y devuelve el (value) eliminado
            elif elem.key == key:
                self.size -= 1
                deletedValue = elem.value
                self.buckets[idx] = None
                return deletedValue
            #Si hay elementos en el idx, se hace hashing
            else:
                timesHashIsCalled+=1