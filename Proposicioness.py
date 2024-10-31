import tkinter as tk
from tkinter import scrolledtext, ttk

# Función para centrar la ventana en la pantalla
def centrar_ventana(ventana, ancho=400, alto=300):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

# Función para identificar el operador
def identificar_operador(proposicion):
    if ' y ' in proposicion:
        operador = 'and'
        proposiciones_simples = proposicion.split(' y ')
    elif ' o ' in proposicion:
        operador = 'or'
        proposiciones_simples = proposicion.split(' o ')
    else:
        return None
    return operador, [p.strip() for p in proposiciones_simples]

# Función para procesar la proposición ingresada
def procesar_proposicion():
    proposicion = entrada_proposicion.get().lower()
    resultado = identificar_operador(proposicion)

    if isinstance(resultado, tuple):
        global operador, proposiciones_simples
        operador, proposiciones_simples = resultado
        formula = f"A ∧ B" if operador == 'and' else "A ∨ B"

        etiqueta_resultado.config(
            text=f"Operador: {operador.upper()}\n"
                 f"A: {proposiciones_simples[0]}\n"
                 f"B: {proposiciones_simples[1]}\n"
                 f"Fórmula: {formula}"
        )
        boton_cerrar.grid(row=4, column=0, columnspan=2, pady=10)
    else:
        etiqueta_resultado.config(text="Proposición no válida")

# Función para mostrar la tabla de verdad
def mostrar_tabla_verdad(operador):
    ventana_tabla = tk.Toplevel()
    ventana_tabla.title(f"Tabla de Verdad - {operador.upper()}")
    centrar_ventana(ventana_tabla, 400, 300)

    texto = scrolledtext.ScrolledText(ventana_tabla, width=40, height=10, font=("Arial", 12))
    texto.pack(padx=10, pady=10)

    texto.insert(tk.END, f"Tabla de Verdad para {operador.upper()}:\n\n")
    texto.insert(tk.END, "A | B | Resultado\n")
    texto.insert(tk.END, "--|---|----------\n")

    for A in [1, 0]:
        for B in [1, 0]:
            resultado = A and B if operador == 'and' else A or B
            texto.insert(tk.END, f"{A} | {B} | {resultado}\n")

# Función para mostrar el diagrama de árbol
def mostrar_arbol(operador):
    ventana_arbol = tk.Toplevel()
    ventana_arbol.title(f"Árbol de Estados - {operador.upper()}")
    centrar_ventana(ventana_arbol, 600, 400)

    canvas = tk.Canvas(ventana_arbol, width=600, height=400, bg="#f0f0f0")
    canvas.pack(padx=10, pady=10)

    x0, y0 = 300, 50  # Coordenadas iniciales
    dx, dy = 100, 100

    canvas.create_text(x0, y0 - 40, text=f"A: {proposiciones_simples[0]}", font=("Arial", 12, "bold"))
    canvas.create_text(x0, y0 - 20, text=f"B: {proposiciones_simples[1]}", font=("Arial", 12, "bold"))

    nodo_raiz = f"A {operador.upper()} B"
    canvas.create_text(x0, y0, text=nodo_raiz, font=("Arial", 12, "bold"))

    for i, A in enumerate([0, 1]):
        x1, y1 = x0 - dx + i * 2 * dx, y0 + dy
        canvas.create_text(x1, y1, text=f"A={A}", font=("Arial", 12))
        canvas.create_line(x0, y0, x1, y1)

        for j, B in enumerate([0, 1]):
            x2, y2 = x1 - dx/2 + j * dx, y1 + dy
            canvas.create_text(x2, y2, text=f"B={B}", font=("Arial", 12))
            canvas.create_line(x1, y1, x2, y2)

            resultado = A and B if operador == 'and' else A or B
            canvas.create_text(x2, y2 + dy, text=f"R={resultado}", font=("Arial", 12))
            canvas.create_line(x2, y2, x2, y2 + dy)

# Función para cerrar la ventana principal y mostrar los resultados
def cerrar_y_mostrar():
    ventana.destroy()
    mostrar_tabla_verdad(operador)
    mostrar_arbol(operador)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Analizador de Proposiciones")
ventana.config(bg="#dfe6e9")
centrar_ventana(ventana)

# Crear el contenedor para los widgets
frame = tk.Frame(ventana, bg="#dfe6e9", padx=20, pady=20)
frame.grid(row=0, column=0)

# Widgets de entrada y botones
tk.Label(frame, text="Ingresa la proposición:", font=("Arial", 14), bg="#dfe6e9").grid(row=0, column=0, pady=5)
entrada_proposicion = tk.Entry(frame, width=40, font=("Arial", 12))
entrada_proposicion.grid(row=1, column=0, pady=5)

boton_procesar = ttk.Button(frame, text="Procesar", command=procesar_proposicion)
boton_procesar.grid(row=2, column=0, pady=5)

etiqueta_resultado = tk.Label(frame, text="", font=("Arial", 12), bg="#dfe6e9", justify="left")
etiqueta_resultado.grid(row=3, column=0, pady=10)

boton_cerrar = ttk.Button(frame, text="Cerrar y mostrar resultados", command=cerrar_y_mostrar)
boton_cerrar.grid(row=4, column=0, pady=10)
boton_cerrar.grid_remove()  # Ocultar inicialmente

# Iniciar el bucle principal de la interfaz
ventana.mainloop()

