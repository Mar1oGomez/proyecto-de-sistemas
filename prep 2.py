import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from itertools import product
import os

# Directorio de almacenamiento en el escritorio
directorio_guardado = os.path.join(os.path.expanduser("~"), "Desktop", "Proposiciones")

# Crear el directorio si no existe
os.makedirs(directorio_guardado, exist_ok=True)

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
    mostrar_reglas(operadores, proposiciones_simples)

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

# Función para mostrar la ventana de reglas y permitir correcciones
def mostrar_reglas(operadores, proposiciones_simples):
    ventana_reglas = tk.Tk()
    ventana_reglas.title("Reglas")

    # Crear un área de texto para mostrar las reglas
    texto_reglas = scrolledtext.ScrolledText(ventana_reglas, width=70, height=15)
    texto_reglas.pack()

    # Mostrar las proposiciones simples
    reglas_texto = "Proposiciones simples:\n"
    for i, prop in enumerate(proposiciones_simples):
        reglas_texto += f"{chr(65 + i)}: {prop.replace('¬', '').strip()}\n"

    texto_reglas.insert(tk.END, reglas_texto)

    # Función para guardar las proposiciones en un archivo
    def guardar_proposiciones():
        # Abrir un cuadro de diálogo para seleccionar la ubicación del archivo
        archivo_guardar = filedialog.asksaveasfilename(initialdir=directorio_guardado, defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if archivo_guardar:
            try:
                with open(archivo_guardar, 'w') as f:
                    f.write(reglas_texto)
                messagebox.showinfo("Éxito", "Proposiciones guardadas correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

    # Crear un botón para guardar las proposiciones
    boton_guardar = tk.Button(ventana_reglas, text="Guardar Proposiciones", command=guardar_proposiciones)
    boton_guardar.pack()

    # Crear un botón para corregir la proposición
    def corregir_proposicion():
        texto_reglas.delete('1.0', tk.END)  # Limpiar el área de texto
        texto_reglas.insert(tk.END, "Ingresa la nueva proposición:\n")

        def aplicar_correcion():
            nueva_proposicion = texto_reglas.get("1.0", tk.END).strip()
            if nueva_proposicion:
                global proposiciones_simples  # Hacer global para actualizar
                proposiciones_simples = [nueva_proposicion]
                messagebox.showinfo("Éxito", "Corrección aplicada.")
                ventana_reglas.destroy()  # Cerrar la ventana de reglas

        # Crear un botón para aplicar la corrección
        boton_aplicar = tk.Button(ventana_reglas, text="Aplicar Corrección", command=aplicar_correcion)
        boton_aplicar.pack()

    # Crear un botón para corregir la proposición
    boton_corregir = tk.Button(ventana_reglas, text="Corregir Proposición", command=corregir_proposicion)
    boton_corregir.pack()

    # Crear un botón para ver archivos guardados
    def ver_archivos_guardados():
        ventana_archivos = tk.Tk()
        ventana_archivos.title("Archivos Guardados")

        lista_archivos = tk.Listbox(ventana_archivos, width=70, height=15)
        lista_archivos.pack()

        # Listar archivos en el directorio de almacenamiento
        archivos = [f for f in os.listdir(directorio_guardado) if f.endswith('.txt')]
        for archivo in archivos:
            lista_archivos.insert(tk.END, archivo)

        # Función para corregir un archivo
        def corregir_archivo():
            seleccion = lista_archivos.curselection()
            if seleccion:
                archivo_seleccionado = lista_archivos.get(seleccion[0])
                with open(os.path.join(directorio_guardado, archivo_seleccionado), 'r') as f:
                    contenido = f.read()
                texto_reglas.delete('1.0', tk.END)
                texto_reglas.insert(tk.END, contenido)

                def aplicar_correccion_archivo():
                    nueva_proposicion = texto_reglas.get("1.0", tk.END).strip()
                    with open(os.path.join(directorio_guardado, archivo_seleccionado), 'w') as f:
                        f.write(nueva_proposicion)
                    messagebox.showinfo("Éxito", "Archivo corregido.")
                    ventana_archivos.destroy()

                # Crear un botón para aplicar la corrección del archivo
                boton_aplicar_archivo = tk.Button(ventana_archivos, text="Aplicar Corrección", command=aplicar_correccion_archivo)
                boton_aplicar_archivo.pack()

        # Función para borrar un archivo
        def borrar_archivo():
            seleccion = lista_archivos.curselection()
            if seleccion:
                archivo_seleccionado = lista_archivos.get(seleccion[0])
                os.remove(os.path.join(directorio_guardado, archivo_seleccionado))
                messagebox.showinfo("Éxito", f"Archivo {archivo_seleccionado} borrado.")
                lista_archivos.delete(seleccion)  # Remover el archivo de la lista

        # Crear botones para corregir y borrar archivos
        boton_corregir_archivo = tk.Button(ventana_archivos, text="Corregir Archivo", command=corregir_archivo)
        boton_corregir_archivo.pack()
        boton_borrar_archivo = tk.Button(ventana_archivos, text="Borrar Archivo", command=borrar_archivo)
        boton_borrar_archivo.pack()

    # Crear un botón para ver archivos guardados
    boton_ver_archivos = tk.Button(ventana_reglas, text="Ver Archivos Guardados", command=ver_archivos_guardados)
    boton_ver_archivos.pack()

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



 seleccion de reglas 
 mostrar_arbol
 que no se repitan atomos ]
 guardar y cargar reglas 
 arbol gigante de los atomos 
  y mostrar tabla de atomos y de reglas 
  preguntar por los atomos 




