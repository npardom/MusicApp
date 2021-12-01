#Queue y Stack implementadas usando Arrays
class Stack:
    def __init__(self):
        self.notes = []

    def isEmpty(self):
        return self.notes == []

    def push(self, element):
        self.notes.append(element)

    def size(self):
        return len(self.notes)  

    def peek(self):
        return self.notes[-1]

    def pop(self):
        duration = self.notes.pop()
        note = self.notes.pop()
        return (note, duration)

    def getFirstElement(self):
        return self.notes[0]

    def getAsArray(self):
        return self.notes

    def initializeFromArray(self, array):
        self.notes = array

    def __str__(self):
        return str(self.getAsArray())
        
class Queue:
    def __init__(self):
        self.notes = []

    def isEmpty(self):
        return self.notes == []

    def enqueue(self, element):
        self.notes.insert(0,element)
        
    def size(self):
        return len(self.notes) 

    def getFirstElement(self):
        return self.notes[self.size() - 1] 

    def dequeue(self):
        return self.notes.pop()

    def getAsArray(self):
        array = list(reversed(self.notes))
        return array

    def initializeFromArray(self, array):
        array.reverse()
        self.notes = array

    def __str__(self):
        return str(self.getAsArray())