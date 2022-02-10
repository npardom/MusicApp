#Queue y Stack implementadas usando Arrays
import numpy as np

class ArrayList:
    def __init__(self):
        self.arr = np.empty(1,object)
        self.trueSize = 0

    def isEmpty(self):
        return bool(self.trueSize)
    
    def size(self):
        return self.trueSize

    def add(self,index,element):
        self.arr[1 + index:self.trueSize + 1] = self.arr[index:self.trueSize]
        self.trueSize += 1
        self.arr[index] = element
        if self.trueSize  == self.arr.size :
            self.arr.resize(2*self.arr.size)

    def remove(self,index): 
        try:
            element = self.arr[index]
            self.arr[index:self.trueSize - 1] = self.arr[index+1:self.trueSize]
        except:
            raise Exception
        self.trueSize -=1
        return element
 
    def getAsArray(self):
        return self

    def __str__(self):
        return str(self.arr[:self.trueSize])

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n <= self.trueSize-1:
            self.n += 1
            return self.arr[self.n-1]
        else:
            raise StopIteration

class Stack(ArrayList):
    def __init__(self):
        ArrayList.__init__(self)

    def peek(self):
        return self.arr[self.trueSize-1]
 
    def pop(self):
        return self.remove(self.trueSize-1)

    def push(self,element):
        self.arr[self.trueSize] = element
        self.trueSize += 1
        if self.trueSize  == self.arr.size :
            newArray = np.empty((self.trueSize)*2,object)          
            newArray[0:self.trueSize] = self.arr
            self.arr = newArray

    def getFirstElement(self):
        return self.arr[0]

    def initializeFromArray(self, arrayList):
        self.arr = np.array(arrayList.arr,copy=1)
        self.trueSize = arrayList.trueSize 

class Queue(ArrayList):
    def __init__(self):
        ArrayList.__init__(self)

    def enqueue(self, element):
        self.add(0,element)

    def dequeue(self):
        self.trueSize -=1
        return self.arr[self.trueSize]
        
    def getFirstElement(self):
        return self.arr[self.size() - 1] 

    def getAsArray(self):
        return self
        
    def initializeFromArray(self, arrayList):
        self.arr = np.empty(arrayList.arr.size,object)
        self.arr[0:arrayList.trueSize] = np.flipud(arrayList.arr)[arrayList.arr.size - arrayList.trueSize :]
        self.trueSize  = arrayList.trueSize      