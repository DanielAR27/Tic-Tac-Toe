#!/usr/bin/python3

# Autores del programa: Daniel Alemán Ruiz, Víctor Corella Camacho, Justin
# José Jiménez Jiménez
# Carné: C10176, B82354, B94037
# Fecha de elaboración: 7/3/2023 20:50 pm

# LIBRERIAS UTILIZADAS
import tkinter as tk
from tkinter import messagebox
from random import randint
from time import sleep

"""
Descripción del programa:

El siguiente programa es un juego de gato que funciona mediante la interfaz
gráfica Tkinter. El jugador tiene la libertad de si volver a jugar una nueva
partida o bien, si terminar el juego. El programa también se encarga de mostrar
las posiciones en donde el usuario o bien la computadora, haya ganado el juego.
"""


class Notifier():
    def __init__(self, misc: tk.Tk):
        '''
        INICIALIZADOR:
        Se inicializa la clase Messages.

        :param tkinter misc: El root principal de la ventana en Tkinter.
        '''
        self.misc = misc

    @staticmethod
    def player_wins():
        '''
        FUNCIÓN:
        Mensaje de aviso para avisar que el jugador ha ganado.
        '''
        messagebox.showinfo('Felicidades',
                            'Usted ha ganado.')

    @staticmethod
    def pc_wins():
        '''
        FUNCIÓN:
        Mensaje de aviso para avisar que el computador ha ganado.
        '''
        messagebox.showinfo('Advertencia',
                            'La computadora ha ganado.')

    @staticmethod
    def nobody_wins():
        '''
        FUNCIÓN:
        Mensaje de aviso para avisar que nadie ha ganado.
        '''
        messagebox.showinfo('Advertencia',
                            'Nadie ha ganado la partida.')


class Window():
    def __init__(self):
        '''
        INICIALIZADOR:
        Se inicializa la clase Window.
        '''
        # Se crea un objeto de tipo Tkinter, este será por así decirlo nuestro
        # root en donde guardaremos todas las posibles configuraciones.
        self.root = tk.Tk(className='gato')
        # Se crea un notificador.
        self.notifier = Notifier(self.root)
        # Se le otorga una geometría en específico.
        self.root.geometry('400x400')
        # Se aplica este comando para que el tamaño no sea modificable.
        self.root.resizable(0, 0)
        # Se crea un diccionario donde se crean 3 botones.
        self.dict_buttons = {}
        # Se crea un título para el programa.
        self.title = tk.Label(self.root, text='Gato',
                              font='roboto 22 bold').pack()
        # Se crea un mensaje que indica las instrucciones.
        self.game_instructions = tk.Label(self.root,
                                          text='JUGADOR = X  |  PC = O',
                                          font='roboto 14')
        # Se posicionan las instrucciones en la pantalla.
        self.game_instructions.place(x=75, y=40)
        # Se modifica el diccionario creado anteriormente para añadir el
        # tablero de juego.
        self.create_dict()
        # Se corre el programa en un loop.
        self.root.mainloop()

    def open_again(self):
        '''
        FUNCIÓN:
        Abrir una nueva ventana y cerrar la actual.
        '''
        self.root.destroy()  # Destruyendo ventana.
        Window()  # Abriendo nueva ventana.

    def erase_widgets(self):
        """
        FUNCIÓN:
        Borrar todos los widgets después de cierto número.
        """
        # Se obtienen todos los elementos dentro del root.
        wlist = self.root.winfo_children()

        # Cada elemento será eliminado.
        for i in range(len(wlist)):
            wlist[i].destroy()

    def create_dict(self):
        """
        FUNCIÓN:
        Crear un diccionario con información de los botones,
        su respectivo índice y también el valor dentro del botón.
        """
        # Se crean unas coordenadas para el tablero.
        my_x, my_y = 50, 80
        # Se crea un ciclo donde se guardan los botones.
        for i in range(1, 10):
            # Para el número 4 y 7, "x" se va a devolver a su valor
            #  de 50 y el valor de "y" aumentará en 100.
            if i in (4, 7):
                my_x = 50
                my_y += 100
            # En caso contrario, se va a seguir de manera normal.
            else:
                # Siempre que no sea el primer elemento, "x" aumentará en 100.
                if i != 1:
                    my_x += 100
            # Se guarda en un diccionario una lista en conjunto con el botón y
            # el valor del espacio vacío para así inicializar el juego.
            self.dict_buttons[i] = [tk.Button(self.root,
                                              text='  ',
                                              font='roboto 15',
                                              padx=40,
                                              pady=40,
                                              command=lambda num=i:
                                              self.player_plays(num)), ' ']
            # Se posiciona al botón en la pantalla.
            self.dict_buttons[i][0].place(x=my_x, y=my_y)

    def player_plays(self, num):
        """
        FUNCIÓN:
        Función que se encarga de que el jugador pueda hacer su jugada.
        """
        # Si se tiene un espacio vacío, se puede jugar en esa posición
        # sin problema.
        if self.dict_buttons[num][1] == ' ':
            # El valor en la pantalla será cambiado por el caracter de
            # el jugador.
            self.dict_buttons[num][0].configure(text='X')
            # También el valor que se encuentra en el diccionario para
            # revisar las jugadas.
            self.dict_buttons[num][1] = 'X'
            # Se revisa si hay un jugador.
            winner_status = self.check_winner()
            # Si se retornó el caracter del usuario, se avisa que ganó el
            # usuario y se abre un menú en donde se pregunta al usuario que si
            # desea jugar nuevamente.
            if winner_status == 'X':
                self.notifier.player_wins()
                self.play_again_menu()
            elif winner_status == 'O':
                self.notifier.pc_wins()
                self.play_again_menu()
            else:
                # Se llama a una función para que la computadora
                # pueda hacer su jugada.
                self.pc_plays()
                # Se revisa si hay un jugador.
                winner_status = self.check_winner()
                # Si se retornó el caracter del usuario, se avisa que ganó el
                # usuario y se abre un menú en donde se pregunta al usuario
                # que si desea jugar nuevamente.
                if winner_status == 'X':
                    self.notifier.player_wins()
                    self.play_again_menu()
                # Si se retornó el caracter de la computadora, se avisa que
                # ganó la computadora y se abre un menú en donde se pregunta
                # al usuario que si desea jugar nuevamente.
                elif winner_status == 'O':
                    self.notifier.pc_wins()
                    self.play_again_menu()

    def pc_plays(self):
        """
        FUNCIÓN:
        Función que se encarga de que la computadora pueda hacer su jugada.
        """
        # Se guarda en una variable para determinar si se puede jugar, esta por
        # defecto será True.
        can_play = True
        # Se revisa que todas las posiciones esten vacías, si no es así, la
        # condición de que se puede jugar seŕa False.
        for i in range(1, 10):
            # Si se tiene un espacio vacío, se puede suponer que el juego
            # puede seguir y se rompe el ciclo.
            if self.dict_buttons[i][1] == " ":
                break
            else:
                # En caso de que no se cumpla, y se encuentre ya en la última
                # iteración, la variable para determinar si se puede jugar
                # se volverá en False.
                if i == 9:
                    can_play = False
        # Si la condición de que se puede jugar es True, entonces se continua
        # para que la computadora pueda hacer su jugada.
        if can_play is True:
            # Se duerme durante 0.2 segundos, esto para que el juego
            # no sea extremadamente rápido.
            sleep(0.2)
            # Se abre un ciclo, el cual será roto una vez que se encuentre
            # una posición en donde la computadora pueda hacer su jugada.
            while True:
                # Se elige un número del 1 al 9.
                random_button = randint(1, 9)
                # Si el valor de la posición en el diccionario, cumple con que
                # el espacio este vacío entonces será sustituido por el
                # caracter que pertenece a la computadora.
                if self.dict_buttons[random_button][1] == ' ':
                    # El valor en la pantalla será cambiado por el caracter de
                    # la computadora.
                    self.dict_buttons[random_button][0].configure(text='O')
                    # También el valor que se encuentra en el diccionario para
                    # revisar las jugadas.
                    self.dict_buttons[random_button][1] = 'O'
                    break
                # En caso contrario, se continuará hasta elegir un valor que sí
                # cumpla.
                else:
                    continue
        # Si no se puede jugar, es por que nadie ganó la partida.
        else:
            # Se notifica al usuario que nadie ganó el juego.
            self.notifier.nobody_wins()
            # Se abre un menú en donde se pregunta al usuario que si desea
            # jugar nuevamente.
            self.play_again_menu()

    def check_winner(self):
        """
        FUNCIÓN:
        Se encarga de revisar si hay un ganador dentro de la partida.
        """
        # Se revisa por filas
        for i in range(0, 7, 3):
            # Si en todas las posiciones el caracter es el mismo, el juego
            # termina siempre que el caracter no sea el de vacío. Se mostrará
            # la manera en que el jugador/computadora haya ganado.
            if all([self.dict_buttons[1+i][1] == self.dict_buttons[2+i][1],
                    self.dict_buttons[1+i][1] == self.dict_buttons[3+i][1]]):
                if self.dict_buttons[1+i][1] == ' ':
                    pass
                else:
                    self.dict_buttons[1+i][0].configure(background='sky blue',
                                                        foreground='white')
                    self.dict_buttons[2+i][0].configure(background='sky blue',
                                                        foreground='white')
                    self.dict_buttons[3+i][0].configure(background='sky blue',
                                                        foreground='white')
                    return self.dict_buttons[1+i][1]

        # Se revisa por columnas
        for i in range(3):
            # Si en todas las posiciones el caracter es el mismo, el juego
            # termina siempre que el caracter no sea el de vacío. Se mostrará
            # la manera en que el jugador/computadora haya ganado.
            if all([self.dict_buttons[1+i][1] == self.dict_buttons[4+i][1],
                    self.dict_buttons[1+i][1] == self.dict_buttons[7+i][1]]):
                if self.dict_buttons[1+i][1] == ' ':
                    pass
                else:
                    self.dict_buttons[1+i][0].configure(background='sky blue',
                                                        foreground='white')
                    self.dict_buttons[4+i][0].configure(background='sky blue',
                                                        foreground='white')
                    self.dict_buttons[7+i][0].configure(background='sky blue',
                                                        foreground='white')
                    return self.dict_buttons[1+i][1]

        # Se revisa la diagonal

        # Si en todas las posiciones el caracter es el mismo, el juego
        # termina siempre que el caracter no sea el de vacío. Se mostrará
        # la manera en que el jugador/computadora haya ganado.
        if all([self.dict_buttons[1][1] == self.dict_buttons[5][1],
                self.dict_buttons[1][1] == self.dict_buttons[9][1]]):
            if self.dict_buttons[1][1] == ' ':
                pass
            else:
                self.dict_buttons[1][0].configure(background='sky blue',
                                                  foreground='white')
                self.dict_buttons[5][0].configure(background='sky blue',
                                                  foreground='white')
                self.dict_buttons[9][0].configure(background='sky blue',
                                                  foreground='white')
                return self.dict_buttons[1][1]

        # Se revisa la diagonal inversa

        # Si en todas las posiciones el caracter es el mismo, el juego
        # termina siempre que el caracter no sea el de vacío. Se mostrará
        # la manera en que el jugador/computadora haya ganado.
        if all([self.dict_buttons[3][1] == self.dict_buttons[5][1],
                self.dict_buttons[3][1] == self.dict_buttons[7][1]]):
            if self.dict_buttons[3][1] == ' ':
                pass
            else:
                self.dict_buttons[3][0].configure(background='sky blue',
                                                  foreground='white')
                self.dict_buttons[5][0].configure(background='sky blue',
                                                  foreground='white')
                self.dict_buttons[7][0].configure(background='sky blue',
                                                  foreground='white')
                return self.dict_buttons[3][1]

    def play_again_menu(self):
        """
        FUNCIÓN:
        Se muestra un menú para saber si el jugador quiere seguir jugando o no.
        """
        # Se borran los widgets.
        self.erase_widgets()
        # Se cre una etiqueta para preguntar si se desea jugar de nuevo
        # y se posiciona en la pantalla.
        tk.Label(self.root,
                 text='¿Desea jugar de nuevo?',
                 font='roboto 20 bold').place(x=20, y=150)
        # Se crea un botón que si es presionado, el juego comienza de nuevo.
        self.play_again_yes = tk.Button(self.root,
                                        text="Sí",
                                        font='roboto 15',
                                        background="green",
                                        foreground="white",
                                        padx=20,
                                        command=lambda:
                                        self.open_again())
        # Se posiciona el botón en la pantalla.
        self.play_again_yes.place(x=100, y=200)
        # Se crea un botón que si es presionado, el juego termina.
        self.play_again_no = tk.Button(self.root,
                                       text="No",
                                       font='roboto 15',
                                       background="red",
                                       foreground="white",
                                       padx=20,
                                       command=lambda:
                                       self.root.destroy())
        # Se posiciona el botón en la pantalla.
        self.play_again_no.place(x=200, y=200)


# MAIN
if __name__ == "__main__":
    Window()
