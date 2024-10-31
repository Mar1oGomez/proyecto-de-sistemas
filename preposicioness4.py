import tkinter as tk
from tkinter import scrolledtext
from itertools import product

# Identifica operadores y proposiciones simples en la proposición dada
def identificar_operadores(proposicion):
    proposicion = proposicion.lower()
    operadores = []
    proposiciones_simples = []
    tokens = proposicion.split()
    temp_proposicion = []
    negacion = False  

    for token in tokens:
        if token == "no":
            negacion = True  
        elif token in ["y", "and", "o", "or"]:
            operadores.append("and" if token in ["y", "and"] else "or")
            proposicion_texto = " ".join(temp_proposicion).strip()
            if negacion:
                proposiciones_simples.append("¬" + proposicion_texto)
                negacion = False  
            else:
                proposiciones_simples.append(proposicion_texto)
            temp_proposicion = []
        else:
            temp_proposicion.append(token)

    # Agregar la última proposición, con negación si aplica
    proposicion_texto = " ".join(temp_proposicion).strip()
    if negacion:
        proposiciones_simples.append("¬" + proposicion_texto)
    else:
        proposiciones_simples.append(proposicion_texto)

    return operadores, proposiciones_simples

# Procesa la proposición ingresada por el usuario
def procesar_proposicion():
    global operadores, proposiciones_simples, formula  
    proposicion = entrada_proposicion.get().lower()
    operadores, proposiciones_simples = identificar_operadores(proposicion)

    if operadores and proposiciones_simples:
        formula = construir_formula(proposiciones_simples, operadores)
        mostrar_resultados(operadores, proposiciones_simples, formula)
        boton_cerrar.pack()  
    else:
        etiqueta_resultado.config(text="Proposición no válida")

# Construye la fórmula lógica a partir de las proposiciones simples y los operadores
def construir_formula(proposiciones_simples, operadores):
    formula = 'A' if not proposiciones_simples[0].startswith('¬') else '¬A'
    for i in range(1, len(proposiciones_simples)):
        formula += ' ∧ ' if operadores[i - 1] == 'and' else ' ∨ '
        formula += chr(65 + i) if not proposiciones_simples[i].startswith('¬') else '¬' + chr(65 + i)
    return formula

# Muestra los resultados en la etiqueta de resultado
def mostrar_resultados(operadores, proposiciones_simples, formula):
    text_result = f"Operadores identificados: {', '.join(operadores).upper()}\nProposiciones simples:\n"
    for i, prop in enumerate(proposiciones_simples):
        text_result += f"{chr(65 + i)}: {prop.replace('¬', '').strip()}\n"
    text_result += f"Fórmula: {formula}"
    etiqueta_resultado.config(text=text_result)

# Cierra la ventana y muestra la tabla de verdad y el árbol
def cerrar_y_mostrar():
    ventana.destroy()  
    mostrar_tabla_verdad(operadores, proposiciones_simples)
    mostrar_arbol(operadores, proposiciones_simples, formula)

# Evalúa el resultado de la proposición en función de los valores ingresados
def evaluar_resultado(valores, operadores):
    resultado = valores[0]
    for i in range(1, len(valores)):
        resultado = resultado and valores[i] if operadores[i - 1] == 'and' else resultado or valores[i]
    return int(resultado)

# Función para mostrar la tabla de verdad en una ventana
def mostrar_tabla_verdad(operadores, proposiciones_simples):
    ventana_tabla = tk.Tk()
    ventana_tabla.title("Tabla de verdad")
    texto = scrolledtext.ScrolledText(ventana_tabla, width=70, height=15)
    texto.pack()

    texto.insert(tk.END, "Tabla de verdad:\n\n")
    headers = ' | '.join([chr(65 + i) for i in range(len(proposiciones_simples))]) + " | Resultado\n"
    texto.insert(tk.END, headers)
    texto.insert(tk.END, "--|" * (len(proposiciones_simples) + 1) + "----------\n")

    for valores in product([1, 0], repeat=len(proposiciones_simples)):
        valores_negados = [
            int(not val) if proposiciones_simples[i].startswith('¬') else val
            for i, val in enumerate(valores)
        ]
        resultado = evaluar_resultado(valores_negados, operadores)
        valores_str = ' | '.join(map(str, valores_negados)) + f" | {resultado}\n"
        texto.insert(tk.END, valores_str)
        
    ventana_tabla.mainloop()

# Función para mostrar el árbol lógico en una ventana
def mostrar_arbol(operadores, proposiciones_simples, formula):
    ventana_arbol = tk.Tk()
    ventana_arbol.title("Árbol Lógico")
    texto = scrolledtext.ScrolledText(ventana_arbol, width=70, height=15)
    texto.pack()

    texto.insert(tk.END, "Árbol Lógico:\n\n")
    for valores in product([1, 0], repeat=len(proposiciones_simples)):
        valores_negados = [
            int(not val) if proposiciones_simples[i].startswith('¬') else val
            for i, val in enumerate(valores)
        ]
        resultado = evaluar_resultado(valores_negados, operadores)

        # Construir el árbol lógico como texto
        arbol_str = construir_arbol(valores_negados, operadores)
        texto.insert(tk.END, f"Valores: {valores_negados} -> Resultado: {resultado}\n")
        texto.insert(tk.END, f"Árbol: {arbol_str}\n\n")

    ventana_arbol.mainloop()

# Función para construir el árbol lógico como un string
def construir_arbol(valores_negados, operadores):
    arbol = []
    for i, val in enumerate(valores_negados):
        if val == 1:
            arbol.append(chr(65 + i))  # 'A', 'B', etc.
        else:
            arbol.append('¬' + chr(65 + i))  # Negación de 'A', 'B', etc.

    for i in range(len(operadores)):
        operador = operadores[i]
        if operador == 'and':
            # Combinar con AND
            arbol.append(f"({arbol.pop(0)} ∧ {arbol.pop(0)})")
        elif operador == 'or':
            # Combinar con OR
            arbol.append(f"({arbol.pop(0)} ∨ {arbol.pop(0)})")
    
    return arbol[0] if arbol else ""

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Analizador de Proposiciones")
tk.Label(ventana, text="Ingresa la proposición:").pack()
entrada_proposicion = tk.Entry(ventana, width=70)
entrada_proposicion.pack()
boton_procesar = tk.Button(ventana, text="Procesar", command=procesar_proposicion)
boton_procesar.pack()
etiqueta_resultado = tk.Label(ventana, text="")
etiqueta_resultado.pack()
boton_cerrar = tk.Button(ventana, text="Cerrar y mostrar resultados", command=cerrar_y_mostrar)
boton_cerrar.pack_forget()
ventana.mainloop()


