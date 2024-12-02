import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from statistics import mean, median, mode


# Conexión a la base de datos
conexion = sqlite3.connect('BD_Torteria')
cursorBD = conexion.cursor()

# Función para seleccionar datos de cualquier tabla
def seleccionarDatos(tabla):
    cursorBD.execute(f"SELECT * FROM {tabla}")
    return cursorBD.fetchall()

# Función para seleccionar los pedidos
def seleccionarPedidos():
    cursorBD.execute("SELECT * FROM PEDIDOS")
    return cursorBD.fetchall()

# Función para mostrar la tabla de tortas 
def mostrarTablaTortas():
    # Insertar los datos de la base de datos
    for torta in seleccionarDatos('TORTAS'):
        tabla_tortas.insert("", "end", values=torta)

# Función para actualizar la tabla de pedidos 
def actualizarTablaPedidos(tabla):
    for row in tabla.get_children():
        tabla.delete(row)
    for pedido in seleccionarPedidos():
        tabla.insert("", "end", values=pedido)

# Función para mostrar ventana para agregar cliente
def ventanaAgregarCliente():
    def agregarCliente():
        try:
            nombre = entry_nombre.get()
            telefono = entry_telefono.get()
            direccion = entry_direccion.get()

            if not nombre or not telefono or not direccion:
                raise ValueError("Todos los campos son obligatorios")

            cursorBD.execute('''
                INSERT INTO CLIENTES (NOMBRE, TELEFONO, DIRECCION)
                VALUES (?, ?, ?)
            ''', (nombre, telefono, direccion))
            conexion.commit()
            messagebox.showinfo("Éxito", "Cliente agregado correctamente")
            actualizarTablaClientes(tabla_clientes)  # Actualizar la tabla después de agregar el cliente
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizarTablaClientes(tabla):
        # Limpiar la tabla antes de actualizarla
        for row in tabla.get_children():
            tabla.delete(row)
        
        # Recuperar todos los clientes
        cursorBD.execute("SELECT IDC, NOMBRE, TELEFONO, DIRECCION FROM CLIENTES")
        clientes = cursorBD.fetchall()

        # Insertar los datos en la tabla
        for cliente in clientes:
            tabla.insert("", "end", values=cliente)

    ventana_cliente = tk.Toplevel()
    ventana_cliente.title("Agregar Cliente")

    # Campos de entrada para agregar nuevo cliente
    tk.Label(ventana_cliente, text="Nombre:", font=fuente_buen_gusto_1).grid(row=0, column=0, padx=5, pady=5)
    entry_nombre = tk.Entry(ventana_cliente)
    entry_nombre.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(ventana_cliente, text="Teléfono:", font=fuente_buen_gusto_1).grid(row=1, column=0, padx=5, pady=5)
    entry_telefono = tk.Entry(ventana_cliente)
    entry_telefono.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(ventana_cliente, text="Dirección:", font=fuente_buen_gusto_1).grid(row=2, column=0, padx=5, pady=5)
    entry_direccion = tk.Entry(ventana_cliente)
    entry_direccion.grid(row=2, column=1, padx=5, pady=5)

    # Botón para agregar cliente
    tk.Button(ventana_cliente, text="Agregar Cliente", command=agregarCliente, font=fuente_buen_gusto_1).grid(row=3, column=0, columnspan=2, pady=10)

    # Tabla de clientes
    tabla_clientes = ttk.Treeview(ventana_cliente, columns=("IDC", "Nombre", "Teléfono", "Dirección"), show="headings")
    tabla_clientes.heading("IDC", text="ID Cliente")
    tabla_clientes.column("IDC", width=100, anchor=tk.CENTER)
    tabla_clientes.heading("Nombre", text="Nombre")
    tabla_clientes.column("Nombre", width=150, anchor=tk.W)
    tabla_clientes.heading("Teléfono", text="Teléfono")
    tabla_clientes.column("Teléfono", width=100, anchor=tk.CENTER)
    tabla_clientes.heading("Dirección", text="Dirección")
    tabla_clientes.column("Dirección", width=300, anchor=tk.W)
    tabla_clientes.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

    # Actualizar la tabla de clientes al cargar la ventana
    actualizarTablaClientes(tabla_clientes)


    # Campos de entrada
    tk.Label(ventana_cliente, text="Nombre:", font=fuente_buen_gusto_1).grid(row=0, column=0, padx=5, pady=5)
    entry_nombre = tk.Entry(ventana_cliente)
    entry_nombre.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(ventana_cliente, text="Teléfono:", font=fuente_buen_gusto_1).grid(row=1, column=0, padx=5, pady=5)
    entry_telefono = tk.Entry(ventana_cliente)
    entry_telefono.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(ventana_cliente, text="Dirección:", font=fuente_buen_gusto_1).grid(row=2, column=0, padx=5, pady=5)
    entry_direccion = tk.Entry(ventana_cliente)
    entry_direccion.grid(row=2, column=1, padx=5, pady=5)

# Función para mostrar ventana para agregar pedidos
def ventanaAgregarPedido():
    def agregarPedido():
        try:
            id_cliente = int(entry_id_cliente.get())
            id_torta = int(entry_id_torta.get())
            fecha = entry_fecha.get()
            cantidad = int(entry_cantidad.get())
            nota = entry_nota.get()
            estatus = combo_estatus.get()

            cursorBD.execute("SELECT PRECIO FROM TORTAS WHERE IDT=?", (id_torta,))
            precio = cursorBD.fetchone()
            if not precio:
                raise ValueError("ID de torta no válido")
            total = precio[0] * cantidad

            cursorBD.execute(''' 
                INSERT INTO PEDIDOS (ID_CLIENTE, ID_TORTA, FECHA, CANTIDAD, NOTA, TOTAL, ESTATUS)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (id_cliente, id_torta, fecha, cantidad, nota, total, estatus))
            conexion.commit()
            messagebox.showinfo("Éxito", "Pedido agregado correctamente")
            actualizarTablaPedidos(tabla_pedidos)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ventana_agregar = tk.Toplevel()
    ventana_agregar.title("Agregar Pedido")

    # Campos de entrada
    tk.Label(ventana_agregar, text="ID Cliente:", font=fuente_buen_gusto_1).grid(row=0, column=0, padx=5, pady=5)
    entry_id_cliente = tk.Entry(ventana_agregar)
    entry_id_cliente.grid(row=0, column=1, padx=2, pady=2)

    tk.Label(ventana_agregar, text="ID Torta:", font=fuente_buen_gusto_1).grid(row=1, column=0, padx=5, pady=5)
    entry_id_torta = tk.Entry(ventana_agregar)
    entry_id_torta.grid(row=1, column=1, padx=2, pady=2)

    tk.Label(ventana_agregar, text="Fecha (YYYY-MM-DD):", font=fuente_buen_gusto_1).grid(row=2, column=0, padx=5, pady=5)
    entry_fecha = tk.Entry(ventana_agregar)
    entry_fecha.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(ventana_agregar, text="Cantidad:", font=fuente_buen_gusto_1).grid(row=3, column=0, padx=5, pady=5)
    entry_cantidad = tk.Entry(ventana_agregar)
    entry_cantidad.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(ventana_agregar, text="Nota:", font=fuente_buen_gusto_1).grid(row=4, column=0, padx=5, pady=5)
    entry_nota = tk.Entry(ventana_agregar)
    entry_nota.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(ventana_agregar, text="Estatus:", font=fuente_buen_gusto_1).grid(row=5, column=0, padx=5, pady=5)
    combo_estatus = ttk.Combobox(ventana_agregar, values=["en proceso", "pagado", "cancelado"])
    combo_estatus.grid(row=5, column=1, padx=5, pady=5)

    tk.Button(ventana_agregar, text="Agregar Pedido", command=agregarPedido, font=fuente_buen_gusto_1).grid(row=6, column=0, columnspan=2, pady=10)

    # Botón para abrir ventana de agregar cliente
    tk.Button(ventana_agregar, text="Agregar Cliente", command=ventanaAgregarCliente, font=fuente_buen_gusto_1).grid(row=7, column=0, columnspan=2, pady=10)

    # Tabla de pedidos
    tabla_pedidos = ttk.Treeview(ventana_agregar, columns=("ID", "ID Cliente", "ID Torta", "Fecha", "Cantidad", "Nota", "Total", "Estatus"), show="headings")
    tabla_pedidos.heading("ID", text="ID")
    tabla_pedidos.column("ID", width=50, anchor=tk.CENTER)
    tabla_pedidos.heading("ID Cliente", text="ID Cliente")
    tabla_pedidos.column("ID Cliente", width=50, anchor=tk.CENTER)
    tabla_pedidos.heading("ID Torta", text="ID Torta")
    tabla_pedidos.column("ID Torta", width=50, anchor=tk.CENTER)
    tabla_pedidos.heading("Fecha", text="Fecha")
    tabla_pedidos.column("Fecha", width=100, anchor=tk.CENTER)
    tabla_pedidos.heading("Cantidad", text="Cantidad")
    tabla_pedidos.column("Cantidad", width=50, anchor=tk.CENTER)
    tabla_pedidos.heading("Nota", text="Nota")
    tabla_pedidos.column("Nota", width=150, anchor=tk.W)
    tabla_pedidos.heading("Total", text="Total")
    tabla_pedidos.column("Total", width=50, anchor=tk.CENTER)
    tabla_pedidos.heading("Estatus", text="Estatus")
    tabla_pedidos.column("Estatus", width=100, anchor=tk.CENTER)
    tabla_pedidos.grid(row=8, column=0, columnspan=2, padx=5, pady=10)

    actualizarTablaPedidos(tabla_pedidos)

# Función para mostrar ventana para editar pedidos
def ventanaEditarPedido():
    def cargarPedido():
        try:
            id_pedido = int(entry_id_pedido.get())
            cursorBD.execute("SELECT * FROM PEDIDOS WHERE IDP=?", (id_pedido,))
            pedido = cursorBD.fetchone()
            if not pedido:
                raise ValueError("ID de pedido no encontrado")
            entry_id_cliente.delete(0, tk.END)
            entry_id_cliente.insert(0, pedido[1])
            entry_id_torta.delete(0, tk.END)
            entry_id_torta.insert(0, pedido[2])
            entry_fecha.delete(0, tk.END)
            entry_fecha.insert(0, pedido[3])
            entry_cantidad.delete(0, tk.END)
            entry_cantidad.insert(0, pedido[4])
            entry_nota.delete(0, tk.END)
            entry_nota.insert(0, pedido[5])
            combo_estatus.set(pedido[7])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def editarPedido():
        try:
            id_pedido = int(entry_id_pedido.get())
            id_cliente = int(entry_id_cliente.get())
            id_torta = int(entry_id_torta.get())
            fecha = entry_fecha.get()
            cantidad = int(entry_cantidad.get())
            nota = entry_nota.get()
            estatus = combo_estatus.get()

            cursorBD.execute(''' 
                UPDATE PEDIDOS SET ID_CLIENTE=?, ID_TORTA=?, FECHA=?, CANTIDAD=?, NOTA=?, ESTATUS=? 
                WHERE IDP=?
            ''', (id_cliente, id_torta, fecha, cantidad, nota, estatus, id_pedido))
            conexion.commit()
            messagebox.showinfo("Éxito", "Pedido actualizado correctamente")
            actualizarTablaPedidos(tabla_pedidos)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ventana_editar = tk.Toplevel()
    ventana_editar.title("Editar Pedido")

    tk.Label(ventana_editar, text="ID Pedido:", font=fuente_buen_gusto_1).grid(row=0, column=0, padx=5, pady=5)
    entry_id_pedido = tk.Entry(ventana_editar)
    entry_id_pedido.grid(row=0, column=1, padx=5, pady=5)


    # Campos de entrada
    tk.Label(ventana_editar, text="ID Cliente:", font=fuente_buen_gusto_1).grid(row=1, column=0, padx=5, pady=5)
    entry_id_cliente = tk.Entry(ventana_editar)
    entry_id_cliente.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(ventana_editar, text="ID Torta:", font=fuente_buen_gusto_1).grid(row=2, column=0, padx=5, pady=5)
    entry_id_torta = tk.Entry(ventana_editar)
    entry_id_torta.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(ventana_editar, text="Fecha (YYYY-MM-DD):", font=fuente_buen_gusto_1).grid(row=3, column=0, padx=5, pady=5)
    entry_fecha = tk.Entry(ventana_editar)
    entry_fecha.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(ventana_editar, text="Cantidad:", font=fuente_buen_gusto_1).grid(row=4, column=0, padx=5, pady=5)
    entry_cantidad = tk.Entry(ventana_editar)
    entry_cantidad.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(ventana_editar, text="Nota:", font=fuente_buen_gusto_1).grid(row=5, column=0, padx=5, pady=5)
    entry_nota = tk.Entry(ventana_editar)
    entry_nota.grid(row=5, column=1, padx=5, pady=5)

    tk.Label(ventana_editar, text="Estatus:", font=fuente_buen_gusto_1).grid(row=6, column=0, padx=5, pady=5)
    combo_estatus = ttk.Combobox(ventana_editar, values=["en proceso", "pagado", "cancelado"])
    combo_estatus.grid(row=6, column=1, padx=5, pady=5)

    tk.Button(ventana_editar, text="Editar Pedido", command=editarPedido, font=fuente_buen_gusto_1).grid(row=7, column=0, padx=5, pady=5, sticky= "e")
    tk.Button(ventana_editar, text="Cargar Pedido", command=cargarPedido, font=fuente_buen_gusto_1).grid(row=7, column=1, padx=5, pady=5, sticky="w")

    # Tabla de pedidos
    tabla_pedidos = ttk.Treeview(ventana_editar, columns=("ID", "ID Cliente", "ID Torta", "Fecha", "Cantidad", "Nota", "Total", "Estatus"), show="headings")
    tabla_pedidos.heading("ID", text="ID")
    tabla_pedidos.column("ID", width=50, anchor=tk.CENTER)
    tabla_pedidos.heading("ID Cliente", text="ID Cliente")
    tabla_pedidos.column("ID Cliente", width=50, anchor=tk.CENTER)
    tabla_pedidos.heading("ID Torta", text="ID Torta")
    tabla_pedidos.column("ID Torta", width=50, anchor=tk.CENTER)
    tabla_pedidos.heading("Fecha", text="Fecha")
    tabla_pedidos.column("Fecha", width=100, anchor=tk.CENTER)
    tabla_pedidos.heading("Cantidad", text="Cantidad")
    tabla_pedidos.column("Cantidad", width=50, anchor=tk.CENTER)
    tabla_pedidos.heading("Nota", text="Nota")
    tabla_pedidos.column("Nota", width=150, anchor=tk.W)
    tabla_pedidos.heading("Total", text="Total")
    tabla_pedidos.column("Total", width=50, anchor=tk.CENTER)
    tabla_pedidos.heading("Estatus", text="Estatus")
    tabla_pedidos.column("Estatus", width=100, anchor=tk.CENTER)
    tabla_pedidos.grid(row=10, column=0, columnspan=2, padx=5, pady=10)

    actualizarTablaPedidos(tabla_pedidos)

# Función para mostrar ventana para graficar
def ventanaGraficacion():
    def obtenerTortasMasPedidas():
        try:
            cursorBD.execute('''
                SELECT ID_TORTA, COUNT(*) as cantidad
                FROM PEDIDOS
                GROUP BY ID_TORTA
                ORDER BY cantidad DESC
            ''')
            tortas = cursorBD.fetchall()
            if not tortas:
                raise ValueError("No hay datos en la tabla PEDIDOS")
            return tortas
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return []

    def graficarBarras(tab):
        tortas = obtenerTortasMasPedidas()
        if not tortas:
            return

        ids_tortas = [torta[0] for torta in tortas]
        cantidades = [torta[1] for torta in tortas]

        # Calcular estadísticos
        promedio = mean(cantidades)
        mediana = median(cantidades)
        try:
            moda = mode(cantidades)
        except:
            moda = "No única"

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar([str(id_torta) for id_torta in ids_tortas], cantidades, color="skyblue", edgecolor="black")
        ax.set_title("BARRAS TORTA MÁS PEDIDA")
        ax.set_xlabel("ID Torta")
        ax.set_ylabel("Cantidad de Pedidos")
        ax.set_xticks(range(len(ids_tortas)))
        ax.set_xticklabels([str(id_torta) for id_torta in ids_tortas], rotation=45, ha="right")
        ax.grid(True, axis="y", linestyle="--", alpha=0.7)

        # Media, mediana, moda en eje Y
        ax.axhline(promedio, color="green", linestyle="--", label=f"Media: {promedio:.2f}")
        ax.axhline(mediana, color="orange", linestyle="--", label=f"Mediana: {mediana:.2f}")
        if isinstance(moda, (int, float)):
            ax.axhline(moda, color="red", linestyle="--", label=f"Moda: {moda}")
        else:
            ax.text(0.5, 0.95, "Moda: No única", transform=ax.transAxes, color="red", fontsize=10, ha="center")

        ax.legend()
        canvas = FigureCanvasTkAgg(fig, tab)
        canvas.get_tk_widget().pack(pady=10)
        canvas.draw()

    def graficarBigote(tab):
        tortas = obtenerTortasMasPedidas()
        if not tortas:
            return

        # Extraer ID de tortas y cantidades
        ids_tortas = [torta[0] for torta in tortas]
        cantidades = [torta[1] for torta in tortas]

        fig, ax = plt.subplots(figsize=(8, 5))

        # Dibujar gráfica de caja y bigotes con las cantidades
        ax.boxplot(cantidades, vert=False, patch_artist=True,
                   boxprops=dict(facecolor="lightblue", color="black"),
                   medianprops=dict(color="red"))

        # Configurar etiquetas
        ax.set_title("BIGOTE FRECUENCIA TORTA MÁS PEDIDA")
        ax.set_xlabel("Cantidad de Pedidos")
        ax.set_yticks([1])  # Solo un conjunto de datos
        ax.set_yticklabels(["ID Torta"])  # Título descriptivo

        # Agregar IDs de tortas en etiquetas de valores
        for i, id_torta in enumerate(ids_tortas):
            ax.annotate(f"T {id_torta},", 
                        (cantidades[i], 1.02), 
                        textcoords="offset points", 
                        xytext=(5, 10), 
                        ha='center', fontsize=9)

        canvas = FigureCanvasTkAgg(fig, tab)
        canvas.get_tk_widget().pack(pady=10)
        canvas.draw()

    def graficarPastel(tab):
        tortas = obtenerTortasMasPedidas()
        if not tortas:
            return

        ids_tortas = [f"Torta {torta[0]}" for torta in tortas]
        cantidades = [torta[1] for torta in tortas]

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.pie(cantidades, labels=ids_tortas, autopct='%1.1f%%', startangle=90, colors=plt.cm.tab10.colors)
        ax.set_title("PASTEL PORCENTAJE TORTA MÁS PEDIDA")

        canvas = FigureCanvasTkAgg(fig, tab)
        canvas.get_tk_widget().pack(pady=10)
        canvas.draw()

    # Crear ventana con pestañas
    ventana_graficacion = tk.Toplevel()
    ventana_graficacion.title("Gráficas de Tortas Más Pedidas")
    notebook = ttk.Notebook(ventana_graficacion)

    # Pestaña de barras
    tab_barras = ttk.Frame(notebook)
    notebook.add(tab_barras, text="GRÁFICA DE BARRAS")
    graficarBarras(tab_barras)

    # Pestaña de pastel
    tab_pastel = ttk.Frame(notebook)
    notebook.add(tab_pastel, text="GRÁFICA DE PASTEL")
    graficarPastel(tab_pastel)

    # Pestaña de bigote
    tab_bigote = ttk.Frame(notebook)
    notebook.add(tab_bigote, text="GRÁFICA DE BIGOTE")
    graficarBigote(tab_bigote)

    notebook.pack(expand=True, fill="both")

# Ventana principal
ventana_principal = tk.Tk()
fuente_buen_gusto_1= tkFont.Font(family="Caviar Dreams", size=12)
fuente_buen_gusto_2= tkFont.Font(family="HALO DEK", size=40)
ventana_principal.title("DANGEROSAS")
titulo = tk.Label(ventana_principal,text="TORTAS",font=fuente_buen_gusto_2, fg="darkred")
titulo.pack(pady=20) 
subtitulo = tk.Label(ventana_principal,text="DANGEROSAS",font=fuente_buen_gusto_2, fg="red")
subtitulo.pack(pady=10)

# Tabla de tortas en la ventana principal
tabla_tortas = ttk.Treeview(ventana_principal, columns=("ID", "Nombre", "Descripcion", "Precio"), show="headings")
tabla_tortas.heading("ID", text="ID")
tabla_tortas.column("ID", width=50, anchor=tk.CENTER)
tabla_tortas.heading("Nombre", text="Nombre")
tabla_tortas.column("Nombre", width=200, anchor=tk.CENTER)
tabla_tortas.heading("Descripcion", text="Descripción")
tabla_tortas.column("Descripcion", width=900, anchor=tk.CENTER)
tabla_tortas.heading("Precio", text="Precio")
tabla_tortas.column("Precio", width=50, anchor=tk.CENTER)
tabla_tortas.pack(fill="both", expand=True)

# Botones para abrir las ventanas de agregar pedidos, editar pedidos y la graficación
tk.Button(ventana_principal, text="Agregar Pedido", command=ventanaAgregarPedido).pack(padx=5, pady=5)
tk.Button(ventana_principal, text="Editar Pedido", command=ventanaEditarPedido).pack(padx=5, pady=5)
tk.Button(ventana_principal, text="Mostrar Graficación", command=ventanaGraficacion).pack(padx=5, pady=5)


# Actualizar la tabla de tortas al iniciar la ventana principal
mostrarTablaTortas()

ventana_principal.mainloop()

# Cerrar conexión a la base de datos
conexion.close()