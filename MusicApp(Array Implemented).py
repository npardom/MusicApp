from pydub import AudioSegment
import os
from Structures.ArrayStructures import *  #Importa las estructuras Stack y Queue, implementadas usando Arrays

#Listas y diccionarios usados
notes =["C","D","E","F","G","A","B","C#","D#","F#","G#","A#"]
specialNotes = {"CB":"B","DB":"C#","EB":"D#","FB":"E","GB":"F#","AB":"G#","BB":"A#","B#":"C","E#":"F"}
durations ={'1':"whole", '2':"half", '2.':"whole", '4':"quarter",'4.':"half", '8':"eigth",'8.':"quarter",'16':"semiquaver" }
notValidString = "Entrada no válida"
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

#Recibe y restringe las entradas del usuario
def getInput(status):
        match status:
            case "instrument":
                while (True):
                    userIn = input("\nElige el instrumento para esta linea (P = piano, G = Guitarra, C = Cuerdas): ").upper()
                    if userIn == "HELP":
                        print("Los instrumentos que puedes elegir son:\nP = Piano\nG = Guitarra\nC = Cuerdas")
                    elif userIn == "P" or userIn == "G" or userIn == "C":
                        return userIn
                    else:
                        print(notValidString+": Instrumento no encontrado") 
            case "note":
                while (True):
                    notValid = False
                    userIn = input("\nInserta el nombre de la nota. Para finalizar esta línea, digita 'Q': ").upper()
                    if userIn == "S" or userIn == "Q" or userIn == "E":
                        return userIn
                    elif len(userIn) == 2:
                        note = userIn[0]
                    elif len(userIn) == 3:
                        note = userIn[0:2]
                    try:
                        octave = int(userIn[-1]) 
                        if(note not in notes and note not in specialNotes) or octave > 7 or octave < 1:
                            notValid = True  
                    except:
                        notValid = True              
                    if userIn == "HELP":
                        print("Debes ingresar una nota siguiendo: Nota+Octava. Como por ejemplo: C#4 o Db4.\nNombres de notas: B#/C  C#/Db  D  D#/Eb  E/Fb  E#/F  F#/Gb  G  G#/Ab  A  A#/Bb  B/Cb\nPara insertar un silencio, escribe 'S'\nPara eliminar la nota anterior, escriba 'E'")
                    elif notValid or userIn == "B#7" or userIn == "CB1":
                        print(notValidString+": Nota no válida")
                    else: 
                        if note in notes:
                            if note == "B#":
                                return note + str(octave+1)
                            else:
                                return note + str(octave)
                        elif note in specialNotes:
                            if note == "CB":
                                return specialNotes.get(note) + str(octave-1)
                            else:
                                return specialNotes.get(note) + str(octave)
            case "duration":
                while (True):
                    userIn = input("Inserta la duración de la nota: ").upper()
                    if userIn == "HELP":
                        print("Puedes ingresar una de las siguientes duraciones:\n1 (redonda)\n2 (blanca)\n2. (blanca con punto)\n4 (negra)\n4. (negra con punto)\n8 (corchea)\n8. (corchea con punto)\n16 (semicorchea)\n")
                    elif(userIn in durations):
                        return userIn
                    else:
                        print(notValidString+": Duración no válida\n")
            case "nextLine":
                while(True):
                    userIn = input("\nPara añadir otra linea musical escribe N, si no, escribe Q: ").upper()
                    if(userIn == 'N' or userIn == 'Q'):
                        return userIn
                    else:
                        print(notValidString)
            case "nextAction":
                while(True):
                    userIn = input("Inserta:\n'A' para crear un archivo de audio\n'T' para crear un archivo de texto\n'G' para generar un audio a partir de un archivo .matf\n'F' para finalizar el programa\n").upper()
                    if(userIn == 'A' or userIn == 'G' or userIn == 'T' or userIn == 'F'):
                        return userIn
                    else:
                        print(notValidString+": Acción no válida\n")
            case "tempo":
                while(True):
                    userIn = input("\nInserta el tempo (BPM) de la pieza: ")
                    notValid = False
                    if userIn == "HELP":
                        print("Inserta un tempo, expresado en BPM. Sus valores aceptados van de 60 a 240")
                    else:
                        try:
                            userIn = int(userIn)
                            if(userIn < 60 or userIn >240):
                                notValid = True
                        except:
                            notValid = True
                        if notValid:
                            print(notValidString+": Tempo no válido")
                        else: 
                            return userIn
            case "title":
                while(True):
                    userIn = input("\nInserta el nombre de la pieza: ").strip()
                    notValid = False
                    if userIn == '':
                        notValid = True
                    else:
                        for i in range(len(userIn)):
                            if userIn[i] in forbiddenCharacters:
                                notValid = True
                                break
                    if userIn.upper() == "HELP":
                        print("No puedes usar estos caracteres: \, /, :, *, ?, \", <, >, |")
                    elif notValid:
                        print(notValidString+": Inserta un nombre válido")
                    else: 
                        return userIn
     
#Cambia la velocidad del audio
def changeSpeed(sound, speed):
    finalSound = sound._spawn(sound.raw_data, overrides={"frame_rate": int(sound.frame_rate * speed)})
    return finalSound.set_frame_rate(sound.frame_rate)

#Crea una linea de musica
def createMusicLine(queue):
    instrument = queue.dequeue()
    audioFinal = 0
    exit = "1"
    while(exit=="1"):
        noteName = queue.dequeue()
        if(noteName != "Q"):
            noteDuration = queue.dequeue()
            route = 'Samples/'+ instrument +'/'+durations.get(noteDuration)+'/' + noteName + '.wav' 
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
    return audioFinal

#Crea el archivo de musica
def createMusicFile(stack):
    newLine = "N"
    audioArray = []
    queue = Queue()
    queue.initializeFromArray(stack.getAsArray())
    fileName = queue.dequeue()
    tempo = int(queue.dequeue())/120
    while(newLine=="N"):
        audioArray.append(createMusicLine(queue))
        newLine = queue.dequeue()
    audioFinal = audioArray[0]
    if audioFinal != 0:
        for i in range(1, len(audioArray)):
            audioFinal = audioFinal.overlay(audioArray[i], position=0)
        audioFinal = changeSpeed(audioFinal, tempo)
        finalName = getUniqueName(fileName, ".wav")
        audioFinal.export(finalName, format="wav")
        print('Tu obra "'+ finalName + '" fue guardada con éxito.\n')
    else:
        print('\nNo se generó ningun archivo, ya que no se encontró ninguna nota/silencio\n')

#Crea el archivo de texto
def createTextFile(stack):
    fileName = stack.getFirstElement()
    finalName = getUniqueName(fileName, ".matf")
    textFile= open(finalName,"w")
    array = stack.getAsArray()
    textFile.write("\n".join(map(str,array)))
    textFile.close()
    print('Tu obra "'+ finalName + '" fue guardada con éxito.\n')

#Crea el array con los datos usando input
def createStackByInput():
    noteStack = Stack()
    newLine = "N"
    noteStack.push(getInput("title"))
    noteStack.push(getInput("tempo"))
    while(newLine=="N"):
        noteStack.push(getInput("instrument"))
        exit = "1"
        while(exit=="1"):
            note  = getInput("note")
            if(note == "Q"):
                noteStack.push(note)
                exit = "0"
            elif(note == "E"):
                lastInput = noteStack.peek()
                if (lastInput == "C" or lastInput == "P" or lastInput == "G" or lastInput == "N" or lastInput == "Q") or ((type (lastInput)==int) and lastInput>60) :
                    print("No hay notas por remover")
                else:
                    removed = noteStack.pop()
                    print("Se eliminó la nota",removed[0],"con duración",removed[1])
            else:
                noteStack.push(note)  
                noteStack.push(getInput("duration"))          
        newLine = getInput("nextLine")
        noteStack.push(newLine)
    return noteStack

#Crea el array con los datos usando un archivo .txt
def createStackByFile(file):
    noteStack = Stack()
    newLine = "N"
    noteStack.push(file.readline().rstrip())
    noteStack.push(file.readline().rstrip())
    while(newLine=="N"):
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

print("--------------------------")
print("♪ BIENVENIDO A MUSIC APP ♪")
print("--------------------------")
action = ""
while(action != 'F'):
    action = getInput("nextAction")
    if action == "A":
        createMusicFile(createStackByInput())
    elif action == "T":
        createTextFile(createStackByInput())
    elif action == "G":
        while(True):
            textFile = input("\nIntroduzca la ruta del archivo de texto: ")
            if(os.path.isfile(textFile) and textFile[-5:] == ".matf"):
                file = open(textFile,"r")
                break
            else:
                print("La ruta y/o el archivo no son válidos/no existen")
        try:
            createMusicFile(createStackByFile(file))
        except:
            print("Hay un error en el archivo. Intentalo nuevamente con otro archivo\n")     