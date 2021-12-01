# MusicApp
**MusicApp** es un programa que te permite crear tus propios archivos de audio a partir de la introducción lineal de las notas musicales y sus duraciones.

## Como funciona
1. Primero debes elegir el modo de trabajo que desees, hay 3 modos disponibles:
    - **Crear un archivo de audio (A)**
  
      Permite generar un archivo de audio en formato *.wav*
    - **Crear un archivo de texto (T)**

      Permite generar un archivo de texto con la información de la obra. Con este archivo, podrás generar el archivo de audio de manera automática en otro momento.
    - **Generar un audio usando un archivo de texto (G)** 

      Permite generar un archivo de audio de forma automática usando la información almacenada en un archivo *.matf (MusicApp Text File).*
2. Al elegir las opciones 'A' o 'T', MusicApp te pedirá el nombre de la obra y su tempo (Ver ["Introducción del Tempo"](#tempo)). Tras esto, el programa te guiará para que insertes el nombre de cada nota y su duración correspondiente, de forma lineal (Ver ["Introducción de Notas"](#notas)).

    Al elegir la opción 'G', solo deberás escribir la ruta donde se encuentra el archivo *.matf*.
4. Al finalizar el proceso, el programa lanzará un mensaje notificando que el archivo ha sido guardado correctamente.
5. Tras guardar un archivo, el programa te da la opción de crear un nuevo archivo o de escribir F para finalizar el programa.

<a name="tempo"></a>
## Introducción del Tempo
MusicApp tiene la opción de definir el tempo (velocidad) de una pieza. Para esto, solo debes introducir el valor del tempo en **BPM** (*Beats Per Minute*).

El tempo coincide con la indicación metronómica presente en las partituras:
> ♩ = 120

Para insertar esto en MusicApp, simplemente ponemos 120 cuando se nos pida el tempo:
> `Inserta el tempo (BPM) de la pieza: 120`

<a name="notas"></a>
## Introducción de Notas
Para introducir una nota, MusicApp requiere dos datos:

1. Nombre
        
    - Consiste en la nota y su octava correspondiente. MusicApp usa el **cifrado americano** para nombrar las notas. Es decir, las notas siguen la nomenclatura 'C', 'D', 'E', 'F', 'G', 'A', 'B' (en vez de 'Do', 'Re', 'Mi', 'Fa', 'Sol', 'La', 'Si').

    - Para insertar alteraciones (notas con sostenido o bemol), solo añade '#' para sostenido o 'b' para bemol.

    - Finalmente se inserta la octava. MusicApp permite 7 octavas (1-7) , que abarcan aproximadamente todas las notas de un piano tradicional.

         ![piano](/Pictures/piano.png)

    - Por ejemplo, si quieres añadir la nota Do de la octava 4, debes escribir esto:
      > `Inserta el nombre de la nota: C4`

    - Si quieres añadir la nota F# de la octava 5, debes escribir esto:
      > `Inserta el nombre de la nota: F#5`

    - Tambien puedes escribir la nota usando bemol:
      > `Inserta el nombre de la nota: Gb5`

      En este caso, 'F#5' y 'Gb5' representan la misma nota, escrita de dos distintas maneras.

    - Si quieres añadir un silencio, solo escribe 'S':
      > `Inserta el nombre de la nota: S`

    - A continuación, algunos ejemplos de notaciones erroneas:
      > `B#2` <--- Las notas B y E no pueden tener sostenidos  
      > `Cb4` <--- Las notas C y F no pueden tener bemoles  
      > `F8` <--- La octava 8 se sale del rango permitido (1-7)

2. Duración
    - Hay 5 duraciones básicas: 1 (redonda), 2 (blanca), 4 (negra), 8 (corchea) y 16 (semicorchea).

        ![notes](/Pictures/notes.png)
    
    - Las duraciones siguen la lógica estandar de la teoría musical:
      - La nota redonda tiene la duración más larga entre todas.
      - Dos notas blancas duran lo mismo que una redonda (1 redonda = 2 blancas)
      - Dos notas negras duran lo mismo que una blanca (1 redonda = 2 blancas = 4 negras)
      - Dos corcheas duran lo mismo que una negra (1 redonda = 2 blancas = 4 negras = 8 corcheas)
      - Dos semicorcheas duran lo mismo que una corchea (1 redonda = 2 blancas = 4 negras = 8 corcheas = 16 semicorcheas)

    - Por ejemplo, si quieres la nota Re bemol de la octava 3, con duración de corchea, debes escribir esto:
      > `Inserta el nombre de la nota: Db3`   
      > `Inserta la duración de la nota: 8`

    - Los silencios también se rigen con la misma notación para su duración.

    - Por ejemplo, para añadir un silencio con duración de redonda , debes escribir esto:
      > `Inserta el nombre de la nota: S`   
      > `Inserta la duración de la nota: 1`
      
    - Las notas blanca (2), negra (4) y corchea (8) permiten añadir un punto para denotar una duración extra del 50% respecto a su valor original, siguiendo la notación musical tradicional:
      > `Inserta el nombre de la nota: Bb3`   
      > `Inserta la duración de la nota: 2.`

        ![dot](/Pictures/dot.png)

    - A continuación, algunos ejemplos de duraciones erroneas:
      > `5` <--- Las unicas entradas permitidas son '1', '2', '2.', '4', '4.', '8', '8.', '16'  
      > `1.` <--- Las notas de duración 1 y 16 no permiten poner el punto  

 ## Líneas de música 
En MusicApp puedes crear varias lineas de música en un mismo archivo para generar armonía.
![lines](/Pictures/lines.png)
Para hacer esto, solo escribe 'N' cuando aparezca la opción de crear una nueva línea:
> `Para añadir otra linea musical escribe N, si no, escribe Q: " N`

Puedes elegir entre tres instrumentos diferentes para cada línea:
> `Elige el instrumento para esta linea (P = piano, G = Guitarra, C = Cuerdas): P`
