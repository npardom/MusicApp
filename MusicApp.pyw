import tkinter as tk                   #Libreria para Interfaz Grafica 
from tkinter import filedialog as fd   #Libreria para abrir File Explorer
from pydub import AudioSegment         #Libreria para procesar audios
import os                               #Libreria para comprobar rutas de archivo
from Structures.BinaryTree import *        #Importa la estructura AVLTree                      
from Structures.ArrayStructures import *       #Importa las estructuras Stack y Queue, implementadas usando Arrays
from tkinter import messagebox                 #Libreria para cuadros de dialogo
from Structures.HashTable_LinkedList import *  #Importa la estructura HashTable

def generateDurations():
    hashTable = HashTable()
    array = ['1',"whole", '2',"half", '2.',"whole", '4',"quarter",'4.',"half", '8',"eigth",'8.',"quarter",'16',"semiquaver" ]
    hashTable.hashTableFromArray(array)
    return hashTable

#Listas y diccionarios usados
durations =generateDurations()
forbiddenCharacters = ["\\", "/", ':', '*', '?', '"', '<', '>']

#Genera nombres únicos para guardar los archivos
def getUniqueName(fileName, format):
    finalName = fileName + format
    if(os.path.isfile(finalName)):
        i = 1
        while(os.path.isfile(finalName)):
            finalName = fileName + '(' + str(i) +')' + format
            i = i + 1
        return finalName
    else:
        return finalName
     
#Cambia la velocidad del audio
def changeSpeed(sound, speed):
    finalSound = sound._spawn(sound.raw_data, overrides={"frame_rate": int(sound.frame_rate * speed)})
    return finalSound.set_frame_rate(sound.frame_rate)

#Crea el stack con los datos usando input
def createStackByInput():
    global newLine, flag1, flag2,flag3, lineHasNote, lineNames
    flag1 = 1
    noteStack = Stack()
    temporalStack = Stack()
    getNameAndTempo(noteStack)
    if flag1 == 1:
        return
    newLine = "N"
    while(newLine=="N"):
        flag2 = 1
        flag3 = 1
        lineHasNote = 0
        getLineNameAndInstrument(noteStack)
        if flag2 == 1:
            return
        getNote(noteStack, temporalStack)
        if flag3 == 1:
            return
    lineNames = []
    return noteStack

#Crea el stack con los datos usando un archivo .matf
def createStackByFile(file):
    noteStack = Stack()
    newLine = "N"
    noteStack.push(file.readline().rstrip())
    noteStack.push(file.readline().rstrip())
    while(newLine=="N"):
        lineName = file.readline().rstrip()
        noteStack.push(lineName)
        noteStack.push(file.readline().rstrip())
        exit = "1"
        while(exit=="1"):
            note = file.readline().rstrip()
            if(note == "Q"):
                noteStack.push(note)
                exit = "0"
            else:
                noteStack.push(note)  
                noteStack.push(file.readline().rstrip()) 
        newLine = file.readline().rstrip()
        noteStack.push(newLine)
    file.close()
    return noteStack

#Crea una linea de musica
def createMusicLine(queue):
    lineName = queue.dequeue()
    instrument = queue.dequeue()
    audioFinal = 0
    exit = "1"
    while(exit=="1"):
        noteName = queue.dequeue()
        if(noteName != "Q"):
            noteDuration = queue.dequeue()
            route = 'Samples/'+ instrument +'/'+durations.find(noteDuration)+'/' + noteName + '.wav'  
            audio = AudioSegment.from_file(route, format="wav")
            #Esto es para las duraciones intermedias
            if (noteDuration == '2.'):
                audio = audio[0:1500]
            elif (noteDuration == '4.'):
                audio = audio[0:750]
            elif (noteDuration == '8.'):
                audio = audio[0:375]
            audioFinal += audio
        else:
            exit ="0"
    return (lineName, audioFinal)

#Funcion para iniciar todo
def createMusicFile(stack):
    def saveMusicFile(savedLines, root):
        #Se toma cada línea del árbol
        readTree = savedLines.inOrder(root)
        audioFinal = readTree[0].data
        for node in readTree[1:]:
            audioFinal = audioFinal.overlay(node.data, position=0)
        audioFinal = changeSpeed(audioFinal, tempo)
        finalName = getUniqueName(fileName, ".wav")
        audioFinal.export(finalName, format="wav")
        text = 'Tu obra "'+ finalName + '" fue guardada con éxito.'
        messagebox.showinfo(message=text, title="Proceso exitoso")
        firstScreen()
    def saveA():
        global xPosition
        global yPosition
        xPosition = window.winfo_x()
        yPosition = window.winfo_y()
        window.destroy()
        saveMusicFile(audioTree,root)
    def saveS():
        savedLines = BinaryTree()
        tempRoot = None
        for i in variables:
            name = i.get() 
            if name != "":
                tempLine =  audioTree.find(root,name).data
                tempRoot = savedLines.insert(tempRoot,name,tempLine)
        if not tempRoot:
            text = 'Debes seleccionar al menos una línea'
            messagebox.showinfo(message=text, title="No se puede guardar")
        else:
            global xPosition
            global yPosition
            xPosition = window.winfo_x()
            yPosition = window.winfo_y()
            window.destroy()
            saveMusicFile(savedLines,tempRoot)

    #Creamos el queue a partir del stack
    queue = Queue()
    queue.initializeFromArray(stack.getAsArray())
    audioTree = BinaryTree()
    root = None
    fileName = queue.dequeue()
    tempo = int(queue.dequeue())/120
    newLine = "N"
    #Creamos la ventana de espera
    global xPosition
    global yPosition
    window0 = setWindow(xPosition, yPosition)
    #Ponemos la imagen de espera
    w = tk.Canvas(window0, width=750,height=500)
    w.pack(fill="both", expand=True)
    img = tk.PhotoImage(file = "Pictures/GUI/loading.png")
    w.create_image(0,0,image = img, anchor = "nw")
    #Activamos la ventana
    window0.update()
    #Guardamos cada linea en un arbol AVT segun su nombre
    while(newLine=="N"):
        line = createMusicLine(queue)
        root = audioTree.insert(root,line[0],line[1])
        newLine = queue.dequeue()
    #Eliminamos ventana de espera
    xPosition = window0.winfo_x()
    yPosition = window0.winfo_y()
    window0.destroy()
    #Si el archivo solo tiene una linea, se guarda
    if audioTree.getSize()  == 1:
        saveMusicFile(audioTree,root) 
    else:
        #Creamos la ventana de seleccion de lineas
        window = setWindow(xPosition, yPosition)
        #Ponemos la imagen de fondo
        w = tk.Canvas(window, width=750,height=500)
        w.pack(fill="both", expand=True)
        img = tk.PhotoImage(file = "Pictures/GUI/screen5.png")
        w.create_image(0,0,image = img, anchor = "nw")
        #Tenemos los checkbox de seleccion de lineas
        variables = []
        xPos = 280
        yPos = 155
        counter = 0
        for element in audioTree.inOrder(root):
            if counter%8 == 0:
                xPos = xPos + 100
                yPos = 155
            counter +=1 
            var=tk.StringVar()
            variables.append(var)
            c = tk.Checkbutton(window, text=element.id, variable=var, onvalue = element.id, offvalue = "")
            c.place(x=xPos,y=yPos) 
            yPos = yPos + 29
        #Creamos el boton saveAll
        saveAll = tk.PhotoImage(file = "Pictures/GUI/saveAll.png")
        button = tk.Button(window, bg="#18ACC6", image = saveAll ,command = saveA)
        button.place(x=100,y=160) 
        #Creamos el boton saveSome
        saveSome = tk.PhotoImage(file = "Pictures/GUI/saveSome.png")
        button1 = tk.Button(window, bg="#D84747", image = saveSome ,command = saveS)
        button1.place(x=385,y=390) 
        #Generamos la ventana
        window.lift()
        window.attributes('-topmost',True)
        window.after_idle(window.attributes,'-topmost',False)
        window.mainloop()

#Crea el archivo de texto .matf
def createTextFile(stack):
    fileName = stack.getFirstElement()
    finalName = getUniqueName(fileName, ".matf")
    textFile= open(finalName,"w")
    array = stack.getAsArray()
    textFile.write("\n".join(map(str,array)))
    textFile.close()
    text = 'Tu archivo "'+ finalName + '" fue guardado con éxito.'
    messagebox.showinfo(message=text, title="Proceso exitoso")
    firstScreen()

#Funcion para la pantalla de Nombre y Tempo
def getNameAndTempo(noteStack):
    def undo():
        global xPosition
        global yPosition
        xPosition = window.winfo_x()
        yPosition = window.winfo_y()
        window.destroy()
        firstScreen()
    def next():
        name = entry.get()
        if name == "":
            name = "Untitled"
            notValid = False
        else:
            for i in range(len(name)):
                if name[i] in forbiddenCharacters:
                    notValid = True
                    text = "Inserta un nombre válido (no puedes usar estos caracteres: \, /, :, *, ?, \", <, >, |)"
                    messagebox.showinfo(message=text, title="Nombre no permitido")
                    break
                else:
                    notValid = False
        if not notValid:
            tempo = int(w2.get())
            if tempo > 240:
                tempo = 240
            elif tempo < 60:
                tempo = 60
            tempo = str(tempo)
            noteStack.push(name)
            noteStack.push(tempo)
            global flag1
            flag1 = 0
            global xPosition
            global yPosition
            xPosition = window.winfo_x()
            yPosition = window.winfo_y()
            window.destroy()
 
    #Se crea la ventana
    window = setWindow(xPosition, yPosition)
    #Ponemos la imagen de fondo
    w = tk.Canvas(window, width=750,height=500)
    w.pack(fill="both", expand=True)
    img = tk.PhotoImage(file = "Pictures/GUI/screen2.png")
    w.create_image(0,0,image = img, anchor = "nw")
    #Ingresamos nombre de la obra
    entry = tk.Entry(window, width =20, font = (None, 20))
    entry.place(x=225, y= 160)
    #Ingresamos tempo
    var1 = tk.IntVar(value=120)  # Valor Inicial
    w2 = tk.Spinbox(window, from_=60, to=240,width=10, font = (None, 20),textvariable=var1)
    w2.place(x=295, y= 290)
    #Ponemos el boton de continuar
    icon = tk.PhotoImage(file = "Pictures/GUI/continuar.png")
    button1 = tk.Button(window, image = icon, bg="#D84747", command = next)
    button1.place(x=295, y= 350)
    icon2 = tk.PhotoImage(file = "Pictures/GUI/goBack.png")
    undo = tk.Button(window,image = icon2, bg="#D84747", command = undo)
    undo.place(x=20, y= 20)
    #Generamos la ventana
    window.mainloop()

global lineNames
lineNames = []
#Funcion para la pantalla de nombre de Linea e instrumento
def getLineNameAndInstrument(noteStack):
    def piano():
        global lineNames
        lineName = entry.get()
        if lineName == "":
            lineName = "Piano"
            notValid = False
        else:
            for i in range(len(lineName)):
                if lineName[i] in forbiddenCharacters:
                    notValid = True
                    text = "Inserta un nombre válido (no puedes usar estos caracteres: \, /, :, *, ?, \", <, >, |)"
                    messagebox.showinfo(message=text, title="Nombre no permitido")
                    break
                else:
                    notValid = False
        if not notValid:
            finalName = lineName
            i = 1
            while finalName in lineNames:
                finalName = lineName + str(i) 
                i = i + 1
            lineNames.append(finalName)
            noteStack.push(finalName)
            noteStack.push("P")
            global flag2
            flag2 = 0
            global xPosition
            global yPosition
            xPosition = window.winfo_x()
            yPosition = window.winfo_y()
            window.destroy()
    def strings():
        global lineNames
        lineName = entry.get()
        if lineName == "":
            lineName = "Cuerdas"
            notValid = False
        else:
            for i in range(len(lineName)):
                if lineName[i] in forbiddenCharacters:
                    notValid = True
                    text = "Inserta un nombre válido (no puedes usar estos caracteres: \, /, :, *, ?, \", <, >, |)"
                    messagebox.showinfo(message=text, title="Nombre no permitido")
                    break
                else:
                    notValid = False
        if not notValid:
            finalName = lineName
            i = 1
            while finalName in lineNames:
                finalName = lineName + str(i) 
                i = i + 1
            lineNames.append(finalName)
            noteStack.push(finalName)
            noteStack.push("C")
            global flag2
            flag2 = 0
            global xPosition
            global yPosition
            xPosition = window.winfo_x()
            yPosition = window.winfo_y()
            window.destroy()
    def guitar():
        global lineNames
        lineName = entry.get()
        if lineName == "":
            lineName = "Guitarra"
            notValid = False
        else:
            for i in range(len(lineName)):
                if lineName[i] in forbiddenCharacters:
                    notValid = True
                    text = "Inserta un nombre válido (no puedes usar estos caracteres: \, /, :, *, ?, \", <, >, |)"
                    messagebox.showinfo(message=text, title="Nombre no permitido")
                    break
                else:
                    notValid = False
        if not notValid:
            finalName = lineName
            i = 1
            while finalName in lineNames:
                finalName = lineName + str(i) 
                i = i + 1
            lineNames.append(finalName)
            noteStack.push(finalName)
            noteStack.push("G")
            global flag2
            flag2 = 0
            global xPosition
            global yPosition
            xPosition = window.winfo_x()
            yPosition = window.winfo_y()
            window.destroy()

    #Se crea la ventana
    window = setWindow(xPosition, yPosition)
    #Ponemos la imagen de fondo
    w = tk.Canvas(window, width=750,height=500)
    w.pack(fill="both", expand=True)
    img = tk.PhotoImage(file = "Pictures/GUI/screen3.png")
    w.create_image(0,0,image = img, anchor = "nw")
    #Ingresamos nombre de la linea
    entry = tk.Entry(window, width =20, font = (None, 20))
    entry.place(x=225, y= 135)
    #Ponemos los botones
    icon1 = tk.PhotoImage(file = "Pictures/GUI/piano.png")
    button1 = tk.Button(window, bg="#D84747", image = icon1, command = piano)
    button1.place(x=50, y= 260)
    icon2 = tk.PhotoImage(file = "Pictures/GUI/cuerdas.png")
    button2 = tk.Button(window, bg="white", image = icon2, command = strings)
    button2.place(x=275, y= 260)
    icon3 = tk.PhotoImage(file = "Pictures/GUI/guitarra.png")
    button3 = tk.Button(window, bg="#18ACC6", image = icon3, command = guitar)
    button3.place(x=500, y= 260)
    #Generamos la ventana
    window.mainloop()

#Funcion para la pantalla de seleccion de notas
def getNote(noteStack, temporalStack):
    def cleanButtons():
        c.config(image = C, bg = "white")
        d.config(image = D, bg = "white")
        e.config(image = E, bg = "white")
        f.config(image = F, bg = "white")
        g.config(image = G, bg = "white")
        a.config(image = A, bg = "white")
        b.config(image = B, bg = "white")
        s.config(image = S, bg = "#35B0CB")
        cS.config(image = CS, bg = "#0C1C32")
        dS.config(image = DS, bg = "#0C1C32")
        fS.config(image = FS, bg = "#0C1C32")
        gS.config(image = GS, bg = "#0C1C32")
        aS.config(image = AS, bg = "#0C1C32")
    def cleanButtons2():
        o1.config(image = O1, bg = "white")
        o2.config(image = O2, bg = "white")
        o3.config(image = O3, bg = "white")
        o4.config(image = O4, bg = "white")
        o5.config(image = O5, bg = "white")
        o6.config(image = O6, bg = "white")
        o7.config(image = O7, bg = "white")
    def cleanButtons3():
        w.config(image = icon5, bg = "white")
        h.config(image = icon6, bg = "white")
        q.config(image = icon7, bg = "white")
        eig.config(image = icon8, bg = "white")
        six.config(image = icon9, bg = "white")
        hDot.config(image = icon10, bg = "white")
        qDot.config(image = icon11, bg = "white")
        eDot.config(image = icon12, bg = "white")
    def pressC():
        global currentNote
        currentNote = "C"
        cleanButtons()
        c.config(image = Cin, bg = "black")
    def pressD():
        global currentNote
        currentNote = "D"
        cleanButtons()
        d.config(image = Din, bg = "black")
    def pressE():
        global currentNote
        currentNote = "E"
        cleanButtons()
        e.config(image = Ein, bg = "black")
    def pressF():
        global currentNote
        currentNote = "F"
        cleanButtons()
        f.config(image = Fin, bg = "black")
    def pressG():
        global currentNote
        currentNote = "G"
        cleanButtons()
        g.config(image = Gin, bg = "black")
    def pressA():
        global currentNote
        currentNote = "A"
        cleanButtons()
        a.config(image = Ain, bg = "black")
    def pressB():
        global currentNote
        currentNote = "B"
        cleanButtons()
        b.config(image = Bin, bg = "black")
    def pressS():
        global currentNote
        currentNote = "S"
        cleanButtons()
        s.config(image = Sin, bg = "#CA4F34")
    def pressCS():
        global currentNote
        currentNote = "C#"
        cleanButtons()
        cS.config(image = CSin, bg = "#F3E3CD")
    def pressDS():
        global currentNote
        currentNote = "D#"
        cleanButtons()
        dS.config(image = DSin, bg = "#F3E3CD")
    def pressFS():
        global currentNote
        currentNote = "F#"
        cleanButtons()
        fS.config(image = FSin, bg ="#F3E3CD")
    def pressGS():
        global currentNote
        currentNote = "G#"
        cleanButtons()
        gS.config(image = GSin, bg = "#F3E3CD")
    def pressAS():
        global currentNote
        currentNote = "A#"
        cleanButtons()
        aS.config(image = ASin, bg = "#F3E3CD")
    def pressO1():
        global currentOctave
        currentOctave = "1"
        cleanButtons2()
        o1.config(image = O1in, bg = "black")
    def pressO2():
        global currentOctave
        currentOctave = "2"
        cleanButtons2()
        o2.config(image = O2in, bg = "black")
    def pressO3():
        global currentOctave
        currentOctave = "3"
        cleanButtons2()
        o3.config(image = O3in, bg = "black")
    def pressO4():
        global currentOctave
        currentOctave = "4"
        cleanButtons2()
        o4.config(image = O4in, bg = "black")
    def pressO5():
        global currentOctave
        currentOctave = "5"
        cleanButtons2()
        o5.config(image = O5in, bg = "black")
    def pressO6():
        global currentOctave
        currentOctave = "6"
        cleanButtons2()
        o6.config(image = O6in, bg = "black")
    def pressO7():
        global currentOctave
        currentOctave = "7"
        cleanButtons2()
        o7.config(image = O7in, bg = "black")
    def pressW():
        global currentDuration
        currentDuration = "1"
        cleanButtons3()
        w.config(image = icon5in, bg = "black")
    def pressH():
        global currentDuration
        currentDuration = "2"
        cleanButtons3()
        h.config(image = icon6in, bg = "black")
    def pressQ():
        global currentDuration
        currentDuration = "4"
        cleanButtons3()
        q.config(image = icon7in, bg = "black")
    def pressEIG():
        global currentDuration
        currentDuration = "8"
        cleanButtons3()
        eig.config(image = icon8in, bg = "black")
    def pressSIX():
        global currentDuration
        currentDuration = "16"
        cleanButtons3()
        six.config(image = icon9in, bg = "black")
    def pressHDOT():
        global currentDuration
        currentDuration = "2."
        cleanButtons3()
        hDot.config(image = icon10in, bg = "black")
    def pressQDOT():
        global currentDuration
        currentDuration = "4."
        cleanButtons3()
        qDot.config(image = icon11in, bg = "black")
    def pressEDOT():
        global currentDuration
        currentDuration = "8."
        cleanButtons3()
        eDot.config(image = icon12in, bg = "black")
    def resetValues():
        global currentNote, currentOctave, currentDuration
        currentNote = None
        currentOctave = None
        currentDuration = None
    def addNote():
        global currentNote, currentOctave, lineHasNote
        b = 0
        if currentNote != None and currentDuration != None:  
            if currentNote != "S" and currentOctave != None:
                currentNote = currentNote + currentOctave
            elif currentNote != "S" and currentOctave == None:
                messagebox.showinfo(message="Inserta una nota válida", title="Aviso")
                b = 1
            if not b:
                noteStack.push(currentNote)  
                noteStack.push(currentDuration)
                lineHasNote = 1
                resetValues()
                cleanButtons()
                cleanButtons2()
                cleanButtons3()
        else:
            messagebox.showinfo(message="Inserta una nota válida", title="Aviso")
    def deleteNote():
        global lineHasNote
        lastInput = noteStack.peek()
        if (lastInput == "C" or lastInput == "P" or lastInput == "G" or lastInput == "N" or lastInput == "Q") or ((type (lastInput)==int) and lastInput>60) :
            messagebox.showinfo(message="No hay ninguna nota/silencio en esta línea", title="Aviso")
        else:
            deletedDuration = noteStack.pop()
            deletedNote = noteStack.pop()
            temporalStack.push(deletedDuration)
            temporalStack.push(deletedNote)
            if deletedNote == "S":
                text = "Se eliminó el silencio con duración " + deletedDuration
            else:
                text = "Se eliminó la nota " + deletedNote + " con duración " + deletedDuration
            messagebox.showinfo(message=text, title="Aviso")
            lastInput = noteStack.peek()
            if (lastInput == "C" or lastInput == "P" or lastInput == "G"):
                lineHasNote = 0
    def reinsertNote():
        if temporalStack.size() != 0:
            reinsertedNote = temporalStack.pop()
            reinsertedDuration = temporalStack.pop()
            noteStack.push(reinsertedNote)
            noteStack.push(reinsertedDuration)
            text = "Se reinsertó la nota " + reinsertedNote + " con duración " + reinsertedDuration
        else:
            text = "No hay más notas por reinsertar"
        messagebox.showinfo(message=text, title="Aviso")
    def newLine():
        lastInput = noteStack.peek()
        if (lastInput == "C" or lastInput == "P" or lastInput == "G"):
            text = "No puedes finalizar esta línea hasta que insertes al menos 1 nota/silencio"
            messagebox.showinfo(message=text, title="Aviso")
        else:
            noteStack.push("Q")
            noteStack.push("N")
            global flag3
            flag3 = 0
            global xPosition
            global yPosition
            xPosition = window.winfo_x()
            yPosition = window.winfo_y()
            window.destroy()
    def finishWork():
        lastInput = noteStack.peek()
        if (lastInput == "C" or lastInput == "P" or lastInput == "G") and noteStack.size() == 4:
            text = "No puedes finalizar esta obra hasta que insertes al menos 1 nota/silencio"
            messagebox.showinfo(message=text, title="Aviso")
        else:
            global lineNames, lineHasNote
            if not lineHasNote:
                lineNames.pop()
                noteStack.pop()
                noteStack.pop()
                noteStack.pop()
                noteStack.pop()
            noteStack.push("Q")
            noteStack.push("Q")
            global newLine
            newLine = "Q"
            global flag3
            flag3 = 0
            global xPosition
            global yPosition
            xPosition = window.winfo_x()
            yPosition = window.winfo_y()
            window.destroy()
  
    global currentNote, currentDuration, currentOctave
    currentNote = None
    currentDuration = None
    currentOctave= None
    #Se crea la siguiente ventana
    window = setWindow(xPosition, yPosition)
    #Ponemos la imagen de fondo
    w = tk.Canvas(window, width=750,height=500)
    w.pack(fill="both", expand=True)
    img = tk.PhotoImage(file = "Pictures/GUI/screen4.png")
    w.create_image(0,0,image = img, anchor = "nw")
    #Botones de teclas
    C = tk.PhotoImage(file = "Pictures/GUI/C.png")
    D = tk.PhotoImage(file = "Pictures/GUI/D.png")
    E = tk.PhotoImage(file = "Pictures/GUI/E.png")
    F = tk.PhotoImage(file = "Pictures/GUI/F.png")
    G = tk.PhotoImage(file = "Pictures/GUI/G.png")
    A = tk.PhotoImage(file = "Pictures/GUI/A.png")
    B = tk.PhotoImage(file = "Pictures/GUI/B.png")
    S = tk.PhotoImage(file = "Pictures/GUI/SILENCIO.png")
    Cin = tk.PhotoImage(file = "Pictures/GUI/Cin.png")
    Din = tk.PhotoImage(file = "Pictures/GUI/Din.png")
    Ein = tk.PhotoImage(file = "Pictures/GUI/Ein.png")
    Fin = tk.PhotoImage(file = "Pictures/GUI/Fin.png")
    Gin = tk.PhotoImage(file = "Pictures/GUI/Gin.png")
    Ain = tk.PhotoImage(file = "Pictures/GUI/Ain.png")
    Bin = tk.PhotoImage(file = "Pictures/GUI/Bin.png")
    Sin = tk.PhotoImage(file = "Pictures/GUI/Sin.png")
    CS = tk.PhotoImage(file = "Pictures/GUI/CS.png")
    DS = tk.PhotoImage(file = "Pictures/GUI/DS.png")
    FS = tk.PhotoImage(file = "Pictures/GUI/FS.png")
    GS = tk.PhotoImage(file = "Pictures/GUI/GS.png")
    AS = tk.PhotoImage(file = "Pictures/GUI/AS.png")
    CSin = tk.PhotoImage(file = "Pictures/GUI/CSin.png")
    DSin = tk.PhotoImage(file = "Pictures/GUI/DSin.png")
    FSin = tk.PhotoImage(file = "Pictures/GUI/FSin.png")
    GSin = tk.PhotoImage(file = "Pictures/GUI/GSin.png")
    ASin = tk.PhotoImage(file = "Pictures/GUI/ASin.png")
    O1 = tk.PhotoImage(file = "Pictures/GUI/o1.png")
    O2 = tk.PhotoImage(file = "Pictures/GUI/o2.png")
    O3 = tk.PhotoImage(file = "Pictures/GUI/o3.png")
    O4 = tk.PhotoImage(file = "Pictures/GUI/o4.png")
    O5 = tk.PhotoImage(file = "Pictures/GUI/o5.png")
    O6 = tk.PhotoImage(file = "Pictures/GUI/o6.png")
    O7 = tk.PhotoImage(file = "Pictures/GUI/o7.png")
    O1in = tk.PhotoImage(file = "Pictures/GUI/o1in.png")
    O2in = tk.PhotoImage(file = "Pictures/GUI/o2in.png")
    O3in = tk.PhotoImage(file = "Pictures/GUI/o3in.png")
    O4in = tk.PhotoImage(file = "Pictures/GUI/o4in.png")
    O5in = tk.PhotoImage(file = "Pictures/GUI/o5in.png")
    O6in = tk.PhotoImage(file = "Pictures/GUI/o6in.png")
    O7in = tk.PhotoImage(file = "Pictures/GUI/o7in.png")
    icon1 = tk.PhotoImage(file = "Pictures/GUI/addNote.png")
    icon2 = tk.PhotoImage(file = "Pictures/GUI/delete.png")
    icon21 = tk.PhotoImage(file = "Pictures/GUI/reinsert.png")
    icon3 = tk.PhotoImage(file = "Pictures/GUI/finishLine.png")
    icon4 = tk.PhotoImage(file = "Pictures/GUI/finishObra.png")
    icon5 = tk.PhotoImage(file = "Pictures/GUI/whole.png")
    icon6 = tk.PhotoImage(file = "Pictures/GUI/half.png")
    icon7 = tk.PhotoImage(file = "Pictures/GUI/quarter.png")
    icon8 = tk.PhotoImage(file = "Pictures/GUI/eight.png")
    icon9 = tk.PhotoImage(file = "Pictures/GUI/sixteenth.png")
    icon10 = tk.PhotoImage(file = "Pictures/GUI/halfDot.png")
    icon11 = tk.PhotoImage(file = "Pictures/GUI/quarterDot.png")
    icon12 = tk.PhotoImage(file = "Pictures/GUI/eightDot.png")
    icon5in = tk.PhotoImage(file = "Pictures/GUI/wholein.png")
    icon6in = tk.PhotoImage(file = "Pictures/GUI/halfin.png")
    icon7in = tk.PhotoImage(file = "Pictures/GUI/quarterin.png")
    icon8in = tk.PhotoImage(file = "Pictures/GUI/eightin.png")
    icon9in = tk.PhotoImage(file = "Pictures/GUI/sixteenthin.png")
    icon10in = tk.PhotoImage(file = "Pictures/GUI/halfDotin.png")
    icon11in = tk.PhotoImage(file = "Pictures/GUI/quarterDotin.png")
    icon12in = tk.PhotoImage(file = "Pictures/GUI/eightDotin.png")
    c = tk.Button(window, bg="white", image = C, command = pressC)
    c.place(x=20, y= 140)
    d = tk.Button(window, bg="white", image = D, command = pressD)
    d.place(x=78, y= 140)
    e = tk.Button(window, bg="white", image = E, command = pressE)
    e.place(x=134, y= 140)
    f = tk.Button(window, bg="white", image = F, command = pressF)
    f.place(x=190, y= 140)
    g = tk.Button(window, bg="white", image = G, command = pressG)
    g.place(x=246, y= 140)
    a = tk.Button(window, bg="white", image = A, command = pressA)
    a.place(x=302, y= 140)
    b = tk.Button(window, bg="white", image = B, command = pressB)
    b.place(x=358, y= 140)
    s = tk.Button(window, bg="#35B0CB", image = S, command = pressS)
    s.place(x=415, y= 140)
    cS = tk.Button(window, bg="#0C1C32", image = CS, command = pressCS)
    cS.place(x=52, y= 140)
    dS = tk.Button(window, bg="#0C1C32", image = DS, command = pressDS)
    dS.place(x=109, y= 140)
    fS = tk.Button(window, bg="#0C1C32", image = FS, command = pressFS)
    fS.place(x=220, y= 140)
    gS = tk.Button(window, bg="#0C1C32", image = GS, command = pressGS)
    gS.place(x=278, y= 140)
    aS = tk.Button(window, bg="#0C1C32", image = AS, command = pressAS)
    aS.place(x=335, y= 140)
    #Botones de octava
    o1 = tk.Button(window, bg="white", image = O1, command = pressO1)
    o1.place(x=486, y= 139)
    o2 = tk.Button(window, bg="white", image = O2, command = pressO2)
    o2.place(x=523, y= 139)
    o3 = tk.Button(window, bg="white", image = O3, command = pressO3)
    o3.place(x=560, y= 139)
    o4 = tk.Button(window, bg="white", image = O4, command = pressO4)
    o4.place(x=597, y= 139)
    o5 = tk.Button(window, bg="white", image = O5, command = pressO5)
    o5.place(x=634, y= 139)
    o6 = tk.Button(window, bg="white", image = O6, command = pressO6)
    o6.place(x=671,y= 139)
    o7 = tk.Button(window, bg="white", image = O7, command = pressO7)
    o7.place(x=708, y= 139)
    #Ponemos los botones de duracion
    w = tk.Button(window, bg="white", image = icon5, command = pressW)
    w.place(x=488, y= 228)
    h = tk.Button(window, bg="white", image = icon6, command = pressH)
    h.place(x=538, y= 228)
    q = tk.Button(window, bg="white", image = icon7, command = pressQ)
    q.place(x=589, y= 228)
    eig = tk.Button(window, bg="white", image = icon8, command = pressEIG)
    eig.place(x=643, y= 228)
    six = tk.Button(window, bg="white", image = icon9, command = pressSIX)
    six.place(x=693, y= 228)
    hDot = tk.Button(window, bg="white", image = icon10, command = pressHDOT)
    hDot.place(x=538, y= 297)
    qDot = tk.Button(window, bg="white", image = icon11, command = pressQDOT)
    qDot.place(x=589, y= 297)
    eDot = tk.Button(window, bg="white", image = icon12, command = pressEDOT)
    eDot.place(x=643, y= 297)
    #Ponemos los botones de abajo
    button1 = tk.Button(window, bg="#00C2CB", image = icon1, command = addNote)
    button1.place(x=20, y= 375)
    button2 = tk.Button(window, bg="#D84747", image = icon2, command = deleteNote)
    button2.place(x=200, y= 375)
    button3 = tk.Button(window, bg="#91A834", image = icon21, command = reinsertNote)
    button3.place(x=300, y= 375)
    button4 = tk.Button(window, bg="white", image = icon3, command = newLine)
    button4.place(x=402, y= 375)
    button5 = tk.Button(window, bg="white", image = icon4, command = finishWork)
    button5.place(x=575, y= 375)
    #Generamos la ventana
    window.mainloop()

#Metodo para crear una ventana
def setWindow(x, y):
    window = tk.Tk()
    window.title("MusicApp")
    window.geometry("750x500+"+str(x)+"+"+str(y))
    window.configure(bg='black')
    return window
  
#Metodo para la primera Pantalla
def firstScreen():
    def option1():
        global xPosition
        global yPosition
        xPosition = window.winfo_x()
        yPosition = window.winfo_y()
        window.destroy()
        createMusicFile(createStackByInput())
    def option2():
        global xPosition
        global yPosition
        xPosition = window.winfo_x()
        yPosition = window.winfo_y()
        window.destroy()
        createTextFile(createStackByInput())
    def option3():
        global xPosition
        global yPosition
        xPosition = window.winfo_x()
        yPosition = window.winfo_y()
        window.destroy()
        while(True):
            textFile = fd.askopenfilename(title='Selecciona un archivo .matf',initialdir='./Examples',filetypes=[("MusicApp File", "*.matf")])
            if textFile == "":
                firstScreen()
                break
            else:
                file = open(textFile,"r")
                try:
                    createMusicFile(createStackByFile(file))
                    break
                except:
                    messagebox.showinfo(message="Hay un error en el archivo. Intentalo nuevamente con otro archivo", title="Error al leer el archivo")

    #Se crea la ventana
    window = setWindow(xPosition, yPosition)
    #Ponemos la imagen de fondo
    w = tk.Canvas(window, width=750,height=500)
    w.pack(fill="both", expand=True)
    img = tk.PhotoImage(file = "Pictures/GUI/screen1.png")
    w.create_image(0,0,image = img, anchor = "nw")
    #Ponemos los botones
    icon1 = tk.PhotoImage(file = "Pictures/GUI/icon1.png")
    button1 = tk.Button(window, bg="#D84747", image = icon1, command = option1)
    button1.place(x=50, y= 130)
    icon2 = tk.PhotoImage(file = "Pictures/GUI/icon2.png")
    button2 = tk.Button(window, bg="white", image = icon2, command = option2)
    button2.place(x=275, y= 130)
    icon3 = tk.PhotoImage(file = "Pictures/GUI/icon3.png")
    button3 = tk.Button(window, bg="#18ACC6", image = icon3, command = option3)
    button3.place(x=500, y= 130)
    #Generamos la ventana
    window.lift()
    window.attributes('-topmost',True)
    window.after_idle(window.attributes,'-topmost',False)
    window.mainloop()

#Funcion para iniciar todo
def initializeProgram():
    def next():
        global xPosition
        global yPosition
        xPosition = window.winfo_x()
        yPosition = window.winfo_y()
        window.destroy()
        firstScreen()
    #Creamos la ventana de inicio
    window = setWindow(xPosition, yPosition)
    #Ponemos la imagen de fondo
    w = tk.Canvas(window, width=750,height=500)
    w.pack(fill="both", expand=True)
    img = tk.PhotoImage(file = "Pictures/GUI/start.png")
    w.create_image(0,0,image = img, anchor = "nw")
    #Creamos el boton INICIAR
    icon0 = tk.PhotoImage(file = "Pictures/GUI/iniciar.png")
    button = tk.Button(window, bg="#18ACC6", image = icon0 ,command = next)
    button.place(x=295,y=340) 
    #Generamos la ventana
    window.mainloop()

#Configuramos la posicion inicial de la ventana
global xPosition
global yPosition
xPosition = 350
yPosition = 150
#Iniciamos el programa
initializeProgram()