import tkinter as tk
from tkinter import ttk
import math
from datetime import datetime

class Calculadora:
    def __init__(self, root):
        # Configuración de la ventana principal
        self.root = root
        self.root.title("Calculadora con Historial")
        self.root.geometry("800x600")  # Aumentamos el tamaño para acomodar más botones
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
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
        self.marco_principal = tk.Frame(self.root, bg="#f0f0f0")
        self.marco_principal.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Marco izquierdo para la calculadora
        self.marco_calculadora = tk.Frame(self.marco_principal, bg="#f0f0f0")
        self.marco_calculadora.pack(side="left", fill="both", expand=True, padx=5)
        
        # Marco derecho para el historial
        self.marco_historial = tk.Frame(self.marco_principal, bg="#f0f0f0")
        self.marco_historial.pack(side="right", fill="both", expand=True, padx=5)
    
    def crear_pantalla(self):
        # Marco para la pantalla
        pantalla_frame = tk.Frame(self.marco_calculadora, bg="#f0f0f0")
        pantalla_frame.pack(fill="x", pady=10)
        
        # Widget de entrada para mostrar la expresión
        pantalla = tk.Entry(
            pantalla_frame,
            font=("Arial", 24),
            textvariable=self.input_text,
            bd=0,
            bg="#ffffff",
            justify="right",
            relief="ridge"
        )
        pantalla.pack(fill="both", ipady=15)
    
    def crear_botones(self):
        # Marco para los botones
        botones_frame = tk.Frame(self.marco_calculadora, bg="#f0f0f0")
        botones_frame.pack(fill="both", expand=True)
        
        # Definir los botones (ahora con más funciones)
        botones = [
            ("C", 0, 0, "#ff6b6b", "#ffffff"),
            ("±", 0, 1, "#a29bfe", "#ffffff"),
            ("%", 0, 2, "#a29bfe", "#ffffff"),
            ("÷", 0, 3, "#a29bfe", "#ffffff"),
            ("7", 1, 0, "#ffffff", "#333333"),
            ("8", 1, 1, "#ffffff", "#333333"),
            ("9", 1, 2, "#ffffff", "#333333"),
            ("×", 1, 3, "#a29bfe", "#ffffff"),
            ("4", 2, 0, "#ffffff", "#333333"),
            ("5", 2, 1, "#ffffff", "#333333"),
            ("6", 2, 2, "#ffffff", "#333333"),
            ("-", 2, 3, "#a29bfe", "#ffffff"),
            ("1", 3, 0, "#ffffff", "#333333"),
            ("2", 3, 1, "#ffffff", "#333333"),
            ("3", 3, 2, "#ffffff", "#333333"),
            ("+", 3, 3, "#a29bfe", "#ffffff"),
            ("0", 4, 0, "#ffffff", "#333333"),
            (".", 4, 1, "#ffffff", "#333333"),
            ("⌫", 4, 2, "#fdcb6e", "#ffffff"),
            ("=", 4, 3, "#74b9ff", "#ffffff"),
            # Nuevos botones de conversión
            ("BIN", 5, 0, "#6c5ce7", "#ffffff"),
            ("OCT", 5, 1, "#6c5ce7", "#ffffff"),
            ("HEX", 5, 2, "#6c5ce7", "#ffffff"),
            ("DEC", 5, 3, "#6c5ce7", "#ffffff")
        ]
        
        # Crear los botones y configurarlos
        for (texto, fila, columna, bg_color, fg_color) in botones:
            boton = tk.Button(
                botones_frame,
                text=texto,
                font=("Arial", 16, "bold"),
                bd=0,
                bg=bg_color,
                fg=fg_color,
                command=lambda t=texto: self.click_boton(t)
            )
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
            text="Historial de Operaciones",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0"
        )
        titulo_historial.pack(pady=10)
        
        # Marco para el historial con scroll
        historial_frame = tk.Frame(self.marco_historial, bg="#f0f0f0")
        historial_frame.pack(fill="both", expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(historial_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Listbox para mostrar el historial
        self.historial_listbox = tk.Listbox(
            historial_frame,
            font=("Arial", 12),
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            selectbackground="#a29bfe",
            yscrollcommand=scrollbar.set
        )
        self.historial_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.historial_listbox.yview)
        
        # Botón para limpiar historial
        boton_limpiar = tk.Button(
            self.marco_historial,
            text="Limpiar Historial",
            font=("Arial", 12),
            bd=0,
            bg="#ff7675",
            fg="#ffffff",
            command=self.limpiar_historial
        )
        boton_limpiar.pack(pady=10, fill="x")
    
    def click_boton(self, texto):
        if texto in ["BIN", "OCT", "HEX", "DEC"]:
            try:
                # Obtener el número actual
                if not self.expresion:
                    return
                
                numero = eval(self.expresion.replace("×", "*").replace("÷", "/"))
                
                # Realizar la conversión según el botón presionado
                if texto == "BIN":
                    resultado = bin(int(numero))[2:]  # Eliminar el prefijo '0b'
                elif texto == "OCT":
                    resultado = oct(int(numero))[2:]  # Eliminar el prefijo '0o'
                elif texto == "HEX":
                    resultado = hex(int(numero))[2:].upper()  # Eliminar el prefijo '0x'
                else:  # DEC
                    resultado = str(int(numero))
                
                # Guardar en historial
                operacion = f"{self.expresion} → {texto} = {resultado}"
                timestamp = datetime.now().strftime("%H:%M:%S")
                self.historial.append(f"{timestamp} - {operacion}")
                self.historial_listbox.insert(tk.END, f"{timestamp} - {operacion}")
                self.historial_listbox.see(tk.END)
                
                # Actualizar pantalla
                self.expresion = resultado
                self.input_text.set(resultado)
                
            except Exception as e:
                self.input_text.set("Error")
                self.expresion = ""
        
        elif texto == "=":
            try:
                # Reemplazar símbolos especiales por operadores reconocibles por Python
                expresion_evaluable = self.expresion.replace("×", "*").replace("÷", "/")
                
                # Evaluar la expresión y formatear el resultado
                resultado = eval(expresion_evaluable)
                
                # Formatear el resultado para mostrar enteros sin decimales
                if resultado == int(resultado):
                    resultado = int(resultado)
                
                # Guardar en historial
                operacion = f"{self.expresion} = {resultado}"
                timestamp = datetime.now().strftime("%H:%M:%S")
                self.historial.append(f"{timestamp} - {operacion}")
                self.historial_listbox.insert(tk.END, f"{timestamp} - {operacion}")
                self.historial_listbox.see(tk.END)  # Auto-scroll al último elemento
                
                # Actualizar pantalla
                self.input_text.set(str(resultado))
                self.expresion = str(resultado)
            except Exception as e:
                self.input_text.set("Error")
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
            if self.expresion and self.expresion[0] == "-":
                self.expresion = self.expresion[1:]
            else:
                self.expresion = "-" + self.expresion
            self.input_text.set(self.expresion)
        
        elif texto == "%":
            try:
                # Calcular porcentaje
                valor = eval(self.expresion.replace("×", "*").replace("÷", "/"))
                self.expresion = str(valor / 100)
                self.input_text.set(self.expresion)
            except:
                self.input_text.set("Error")
                self.expresion = ""
        
        else:
            # Añadir el texto del botón a la expresión
            self.expresion += texto
            self.input_text.set(self.expresion)
    
    def limpiar_historial(self):
        # Limpiar el historial
        self.historial = []
        self.historial_listbox.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = Calculadora(root)
    root.mainloop()

if __name__ == "__main__":
    main()