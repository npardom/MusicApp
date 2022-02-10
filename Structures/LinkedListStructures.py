#Se crea la estructura de lista enlazada
class Node:
    def __init__(self, element = None, next = None):
        self.next = next
        self.element = element

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0
    
    def isEmpty(self):
        return (self.size() == 0)
    
    def getSize(self):
        return self.size

    def get(self, index):
        currentNode = self.head
        for i in range(index):
            currentNode = currentNode.next
        return currentNode.element
    
    def indexOf(self, element):
        currentNode = self.head
        index = 0
        while((currentNode != None) and not(currentNode.element == element)):
            currentNode = currentNode.next
            index += 1
        if(currentNode == None):
            return -1
        else:
            return index

    def remove(self, index):
        removedElement = None
        if index == 0:
            removedElement = self.head.element
            self.head = self.head.next
        else:
            q = self.head
            for i in range(index - 1):
                q = q.next
            removedElement = q.next.element
            q.next = q.next.next
        self.size -= 1
        return removedElement

    def add(self, index, element):
        if index == 0:
            self.head = Node(element, self.head)
        else:
            p = self.head
            for i in range(index - 1):    
                p = p.next
            p.next = Node(element, p.next)
        self.size += 1

    def getFirstElement(self):
        return self.head.element

    def getAsArray(self):
        array = []
        for i in range(self.getSize()):
            array.append(self.get(i))
        return array

    def initializeFromArray(self, array):
        index = 0
        for element in array:    
            self.add(index, element)   
            index += 1
            
    def __str__(self):
        return str(self.getAsArray())

#Stack y Queue, derivadas de la clase LinkedList
class Stack(LinkedList):
    def __init__(self):
        LinkedList.__init__(self)

    def push(self, element):
        self.add(0, element)

    def peek(self):
        return self.get(0)

    def pop(self):
        return self.remove(0)

    def getAsArray(self):
        array = []
        for i in range(self.getSize()-1,-1,-1):
            array.append(self.get(i))
        return array

    def initializeFromArray(self, array):
        array.reverse()
        index = 0
        for element in array:
            self.add(index, element)
            index += 1

    def getFirstElement(self):
        return self.get(self.getSize() - 1)

class Queue(LinkedList):
    def __init__(self):
        LinkedList.__init__(self)

    def enqueue(self, element):
        if self.getSize() == 0:
            self.add(0, element)
        else:
            self.add(self.getSize(), element)

    def dequeue(self):
        return self.remove(0) 