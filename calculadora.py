import tkinter as tk
from tkinter import ttk
import math
from datetime import datetime

# Paleta de colores Kawaii
COLOR_FONDO = "#FFF0F5"  # Rosa muy pálido (Lavender Blush)
COLOR_MARCO = "#FFF0F5"
COLOR_PANTALLA_BG = "#FFFFFF" # Blanco
COLOR_PANTALLA_FG = "#6A5ACD" # Slate Blue (para texto)
COLOR_BOTON_NUM = "#FFFFFF" # Blanco
COLOR_BOTON_NUM_FG = "#6A5ACD" # Slate Blue
COLOR_BOTON_OP = "#ADD8E6"  # Azul claro (Light Blue)
COLOR_BOTON_OP_FG = "#FFFFFF" # Blanco
COLOR_BOTON_ESP = "#FFB6C1" # Rosa claro (Light Pink)
COLOR_BOTON_ESP_FG = "#FFFFFF" # Blanco
COLOR_BOTON_IGUAL = "#98FB98" # Verde pálido (Pale Green)
COLOR_BOTON_IGUAL_FG = "#FFFFFF" # Blanco
COLOR_BOTON_CONV = "#E6E6FA" # Lavanda
COLOR_BOTON_CONV_FG = "#6A5ACD" # Slate Blue
COLOR_HISTORIAL_BG = "#FFFFFF" # Blanco
COLOR_HISTORIAL_FG = "#6A5ACD" # Slate Blue
COLOR_HISTORIAL_SEL = "#FFDAB9" # Peach Puff (para selección)
COLOR_BOTON_LIMPIAR_BG = "#FFA07A" # Salmón claro (Light Salmon)
COLOR_BOTON_LIMPIAR_FG = "#FFFFFF" # Blanco

# Fuente Kawaii (si está disponible, si no, usará Arial)
FONT_KAWAII = ("Comic Sans MS", 16, "bold") # O prueba con "Arial Rounded MT Bold"
FONT_PANTALLA = ("Comic Sans MS", 24)
FONT_HISTORIAL = ("Comic Sans MS", 12)
FONT_TITULO_HISTORIAL = ("Comic Sans MS", 14, "bold")
FONT_BOTON_LIMPIAR = ("Comic Sans MS", 12)


class Calculadora:
    def __init__(self, root):
        # Configuración de la ventana principal
        self.root = root
        self.root.title("Calculadora Kawaii ✨")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg=COLOR_FONDO)

        # Variables
        self.expresion = ""
        self.input_text = tk.StringVar()
        self.historial = []
        self.modo_conversion = False

        # Crear marcos para organizar la interfaz
        self.crear_marcos()

        # Crear los widgets
        self.crear_pantalla()
        self.crear_botones()
        self.crear_historial()

    def crear_marcos(self):
        # Marco principal dividido en dos secciones
        self.marco_principal = tk.Frame(self.root, bg=COLOR_MARCO)
        self.marco_principal.pack(fill="both", expand=True, padx=10, pady=10)

        # Marco izquierdo para la calculadora
        self.marco_calculadora = tk.Frame(self.marco_principal, bg=COLOR_MARCO)
        self.marco_calculadora.pack(side="left", fill="both", expand=True, padx=5)

        # Marco derecho para el historial
        self.marco_historial = tk.Frame(self.marco_principal, bg=COLOR_MARCO)
        self.marco_historial.pack(side="right", fill="both", expand=True, padx=5)

    def crear_pantalla(self):
        # Marco para la pantalla
        pantalla_frame = tk.Frame(self.marco_calculadora, bg=COLOR_MARCO)
        pantalla_frame.pack(fill="x", pady=10)

        # Widget de entrada para mostrar la expresión
        pantalla = tk.Entry(
            pantalla_frame,
            font=FONT_PANTALLA,
            textvariable=self.input_text,
            bd=0,
            bg=COLOR_PANTALLA_BG,
            fg=COLOR_PANTALLA_FG, # Color de texto añadido
            justify="right",
            relief="flat" # Estilo de borde más suave
        )
        pantalla.pack(fill="both", ipady=15)

    def crear_botones(self):
        # Marco para los botones
        botones_frame = tk.Frame(self.marco_calculadora, bg=COLOR_MARCO)
        botones_frame.pack(fill="both", expand=True)

        # Definir los botones con colores kawaii
        # Formato: (texto, fila, columna, bg_color, fg_color)
        botones = [
            ("C", 0, 0, COLOR_BOTON_ESP, COLOR_BOTON_ESP_FG),
            ("±", 0, 1, COLOR_BOTON_OP, COLOR_BOTON_OP_FG),
            ("%", 0, 2, COLOR_BOTON_OP, COLOR_BOTON_OP_FG),
            ("÷", 0, 3, COLOR_BOTON_OP, COLOR_BOTON_OP_FG),
            ("7", 1, 0, COLOR_BOTON_NUM, COLOR_BOTON_NUM_FG),
            ("8", 1, 1, COLOR_BOTON_NUM, COLOR_BOTON_NUM_FG),
            ("9", 1, 2, COLOR_BOTON_NUM, COLOR_BOTON_NUM_FG),
            ("×", 1, 3, COLOR_BOTON_OP, COLOR_BOTON_OP_FG),
            ("4", 2, 0, COLOR_BOTON_NUM, COLOR_BOTON_NUM_FG),
            ("5", 2, 1, COLOR_BOTON_NUM, COLOR_BOTON_NUM_FG),
            ("6", 2, 2, COLOR_BOTON_NUM, COLOR_BOTON_NUM_FG),
            ("-", 2, 3, COLOR_BOTON_OP, COLOR_BOTON_OP_FG),
            ("1", 3, 0, COLOR_BOTON_NUM, COLOR_BOTON_NUM_FG),
            ("2", 3, 1, COLOR_BOTON_NUM, COLOR_BOTON_NUM_FG),
            ("3", 3, 2, COLOR_BOTON_NUM, COLOR_BOTON_NUM_FG),
            ("+", 3, 3, COLOR_BOTON_OP, COLOR_BOTON_OP_FG),
            ("0", 4, 0, COLOR_BOTON_NUM, COLOR_BOTON_NUM_FG),
            (".", 4, 1, COLOR_BOTON_NUM, COLOR_BOTON_NUM_FG),
            ("⌫", 4, 2, COLOR_BOTON_ESP, COLOR_BOTON_ESP_FG),
            ("=", 4, 3, COLOR_BOTON_IGUAL, COLOR_BOTON_IGUAL_FG),
            # Nuevos botones de conversión
            ("BIN", 5, 0, COLOR_BOTON_CONV, COLOR_BOTON_CONV_FG),
            ("OCT", 5, 1, COLOR_BOTON_CONV, COLOR_BOTON_CONV_FG),
            ("HEX", 5, 2, COLOR_BOTON_CONV, COLOR_BOTON_CONV_FG),
            ("DEC", 5, 3, COLOR_BOTON_CONV, COLOR_BOTON_CONV_FG)
        ]

        # Crear los botones y configurarlos
        for (texto, fila, columna, bg_color, fg_color) in botones:
            boton = tk.Button(
                botones_frame,
                text=texto,
                font=FONT_KAWAII, # Usar fuente Kawaii
                bd=0,
                bg=bg_color,
                fg=fg_color,
                activebackground=bg_color, # Evitar cambio de color al presionar
                activeforeground=fg_color,
                relief="flat", # Estilo de borde más suave
                command=lambda t=texto: self.click_boton(t)
            )
            # Redondear esquinas (esto es más complejo y depende del SO/tema)
            # Podríamos usar imágenes o ttk.Style si fuera necesario,
            # pero por ahora mantenemos botones estándar con colores.
            boton.grid(row=fila, column=columna, padx=5, pady=5, sticky="nsew")

        # Configurar el peso de las filas y columnas
        for i in range(6):  # Ahora son 6 filas
            botones_frame.rowconfigure(i, weight=1)
        for i in range(4):
            botones_frame.columnconfigure(i, weight=1)

    def crear_historial(self):
        # Etiqueta para el historial
        titulo_historial = tk.Label(
            self.marco_historial,
            text="Historial Kawaii 💖",
            font=FONT_TITULO_HISTORIAL, # Fuente Kawaii
            bg=COLOR_MARCO,
            fg=COLOR_HISTORIAL_FG # Color de texto
        )
        titulo_historial.pack(pady=10)

        # Marco para el historial con scroll
        historial_frame = tk.Frame(self.marco_historial, bg=COLOR_MARCO)
        historial_frame.pack(fill="both", expand=True)

        # Scrollbar (estilo estándar)
        scrollbar = tk.Scrollbar(historial_frame)
        scrollbar.pack(side="right", fill="y")

        # Listbox para mostrar el historial
        self.historial_listbox = tk.Listbox(
            historial_frame,
            font=FONT_HISTORIAL, # Fuente Kawaii
            bd=0,
            bg=COLOR_HISTORIAL_BG,
            fg=COLOR_HISTORIAL_FG, # Color de texto
            highlightthickness=0,
            selectbackground=COLOR_HISTORIAL_SEL, # Color de selección Kawaii
            selectforeground=COLOR_HISTORIAL_FG, # Color de texto seleccionado
            yscrollcommand=scrollbar.set,
            relief="flat" # Estilo de borde más suave
        )
        self.historial_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.historial_listbox.yview)

        # Botón para limpiar historial
        boton_limpiar = tk.Button(
            self.marco_historial,
            text="Limpiar Historial",
            font=FONT_BOTON_LIMPIAR, # Fuente Kawaii
            bd=0,
            bg=COLOR_BOTON_LIMPIAR_BG,
            fg=COLOR_BOTON_LIMPIAR_FG,
            activebackground=COLOR_BOTON_LIMPIAR_BG,
            activeforeground=COLOR_BOTON_LIMPIAR_FG,
            relief="flat", # Estilo de borde más suave
            command=self.limpiar_historial
        )
        boton_limpiar.pack(pady=10, fill="x")

    def click_boton(self, texto):
        if texto in ["BIN", "OCT", "HEX", "DEC"]:
            try:
                # Obtener el número actual
                if not self.expresion:
                    return

                # Intentar convertir a entero primero para conversiones de base
                try:
                    numero_int = int(eval(self.expresion.replace("×", "*").replace("÷", "/")))
                except ValueError: # Si no es entero, no convertir base
                     self.input_text.set("Error Base")
                     self.expresion = ""
                     return
                except Exception as e: # Otro error de evaluación
                     self.input_text.set("Error Eval")
                     self.expresion = ""
                     return


                # Realizar la conversión según el botón presionado
                if texto == "BIN":
                    resultado = bin(numero_int)[2:]  # Eliminar el prefijo '0b'
                elif texto == "OCT":
                    resultado = oct(numero_int)[2:]  # Eliminar el prefijo '0o'
                elif texto == "HEX":
                    resultado = hex(numero_int)[2:].upper()  # Eliminar el prefijo '0x'
                else:  # DEC (volver a decimal desde la expresión actual, que debería ser un número)
                    # Si la expresión actual ya es decimal, no hacer nada o mostrarla
                    # Si viene de otra base, necesitaríamos saber la base original.
                    # Por simplicidad, asumimos que DEC es para volver a mostrar el número
                    # evaluado si la expresión actual es válida.
                    # O quizás DEC debería convertir *desde* otra base?
                    # Por ahora, solo mostramos el entero evaluado.
                    resultado = str(numero_int)


                # Guardar en historial
                operacion = f"{self.expresion} → {texto} = {resultado}"
                timestamp = datetime.now().strftime("%H:%M:%S")
                self.historial.append(f"{timestamp} - {operacion}")
                self.historial_listbox.insert(tk.END, f"{timestamp} - {operacion}")
                self.historial_listbox.see(tk.END)

                # Actualizar pantalla
                self.expresion = resultado # Guardamos el resultado de la conversión
                self.input_text.set(resultado)

            except Exception as e:
                self.input_text.set("Error Conv")
                self.expresion = ""

        elif texto == "=":
            try:
                # Reemplazar símbolos especiales por operadores reconocibles por Python
                expresion_evaluable = self.expresion.replace("×", "*").replace("÷", "/")

                # Evaluar la expresión y formatear el resultado
                resultado = eval(expresion_evaluable)

                # Formatear el resultado para mostrar enteros sin decimales
                if isinstance(resultado, float) and resultado.is_integer():
                    resultado = int(resultado)
                else:
                    # Opcional: redondear floats a ciertos decimales
                    resultado = round(resultado, 8) # Redondear a 8 decimales

                # Guardar en historial
                operacion = f"{self.expresion} = {resultado}"
                timestamp = datetime.now().strftime("%H:%M:%S")
                self.historial.append(f"{timestamp} - {operacion}")
                self.historial_listbox.insert(tk.END, f"{timestamp} - {operacion}")
                self.historial_listbox.see(tk.END)  # Auto-scroll al último elemento

                # Actualizar pantalla
                self.input_text.set(str(resultado))
                self.expresion = str(resultado)
            except ZeroDivisionError:
                self.input_text.set("Div / 0!")
                self.expresion = ""
            except Exception as e:
                self.input_text.set("Error Calc")
                self.expresion = ""

        elif texto == "C":
            # Limpiar la expresión y la pantalla
            self.expresion = ""
            self.input_text.set("")

        elif texto == "⌫":
            # Borrar el último carácter
            self.expresion = self.expresion[:-1]
            self.input_text.set(self.expresion)

        elif texto == "±":
            # Cambiar signo
            if self.expresion:
                try:
                    # Intentar evaluar para manejar casos como "-(-5)"
                    valor = eval(self.expresion.replace("×", "*").replace("÷", "/"))
                    self.expresion = str(-valor)
                    # Formatear si es entero
                    if isinstance(-valor, float) and (-valor).is_integer():
                         self.expresion = str(int(-valor))

                except: # Si no se puede evaluar, intentar cambiar signo manualmente
                     if self.expresion.startswith('-'):
                         self.expresion = self.expresion[1:]
                     else:
                         self.expresion = '-' + self.expresion
            else: # Si no hay expresión, empezar con "-"
                self.expresion = "-"

            self.input_text.set(self.expresion)


        elif texto == "%":
            try:
                # Calcular porcentaje
                valor = eval(self.expresion.replace("×", "*").replace("÷", "/"))
                resultado = valor / 100
                # Formatear si es entero
                if isinstance(resultado, float) and resultado.is_integer():
                    resultado = int(resultado)
                self.expresion = str(resultado)
                self.input_text.set(self.expresion)
            except Exception as e:
                self.input_text.set("Error %")
                self.expresion = ""

        else:
            # Añadir el texto del botón a la expresión
            # Evitar múltiples puntos decimales en un número
            if texto == '.':
                # Buscar el último operador o el inicio de la cadena
                partes = self.expresion.replace('+', ' ').replace('-', ' ').replace('×', ' ').replace('÷', ' ').split()
                ultimo_numero = partes[-1] if partes else ''
                if '.' in ultimo_numero:
                    return # Ya hay un punto en el número actual

            # Evitar operadores consecutivos (simple verificación)
            ultimo_char = self.expresion[-1:]
            if texto in "+-×÷" and ultimo_char in "+-×÷":
                 # Opcional: reemplazar el último operador
                 # self.expresion = self.expresion[:-1] + texto
                 return # No añadir operador consecutivo

            self.expresion += texto
            self.input_text.set(self.expresion)

    def limpiar_historial(self):
        # Limpiar el historial
        self.historial = []
        self.historial_listbox.delete(0, tk.END)

def main():
    root = tk.Tk()
    # Intentar establecer el icono (usamos el existente calculator.ico por ahora)
    try:
        root.iconbitmap("calculator.ico")
    except tk.TclError:
        print("Advertencia: No se pudo cargar 'calculator.ico'. Asegúrate de que el archivo existe y tiene el formato correcto.")
    app = Calculadora(root)
    root.mainloop()

if __name__ == "__main__":
    main()