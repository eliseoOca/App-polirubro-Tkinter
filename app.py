import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from ttkthemes import ThemedStyle


class ProductCRUD:
    def __init__(self, root):
        self.root = root
        self.root.title("CRUD de Productos, Ventas y Gestión de Fiados y Embases Prestados")
        self.root.geometry("832x624")  # Establecer el tamaño de la ventana principal

        # Conectar a la base de datos o crearla si no existe
        self.conn = sqlite3.connect("productos.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        # Variables de control para los campos de entrada
        self.nombre_var = tk.StringVar()
        self.codigo_var = tk.IntVar()
        self.marca_var = tk.StringVar()
        self.precio_var = tk.DoubleVar()
        self.cantidad_var = tk.IntVar()

        # Variables de control para la pestaña de ventas
        self.codigo_venta_var = tk.IntVar()
        
        # Variables de control para la pestaña de embases prestados
        self.nombre_emb_var = tk.StringVar()
        self.monto_emb_var = tk.DoubleVar()
        self.fecha_emb_var = tk.StringVar()

        # Crear la interfaz de usuario
        self.create_gui()
        
    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
                                id INTEGER PRIMARY KEY,
                                nombre TEXT,
                                codigo_de_barras INTEGER,
                                marca TEXT,
                                precio REAL,
                                cantidad INTEGER)''')
        self.conn.commit()
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS embases (
                                id INTEGER PRIMARY KEY,
                                nombre TEXT,
                                monto REAL,
                                fecha TEXT)''')
        self.conn.commit()

    def create_gui(self):
        # Crear un objeto de estilo ttkthemes
        style = ThemedStyle(self.root)
        style.set_theme("blue")
        
        # Crear un ttk.Notebook para agregar pestañas
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True)

        # Pestaña de Productos
        product_tab = ttk.Frame(notebook)
        notebook.add(product_tab, text='Productos')

        # Crear un LabelFrame para los campos de entrada en la pestaña de productos
        input_frame = ttk.LabelFrame(product_tab, text="Datos del Producto")
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Etiquetas y campos de entrada dentro del LabelFrame en la pestaña de productos
        tk.Label(input_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(input_frame, textvariable=self.nombre_var).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(input_frame, text="Código de Barras:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(input_frame, textvariable=self.codigo_var).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(input_frame, text="Marca:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(input_frame, textvariable=self.marca_var).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(input_frame, text="Precio:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(input_frame, textvariable=self.precio_var).grid(row=3, column=1, padx=5, pady=5, sticky="w")

        tk.Label(input_frame, text="Cantidad:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(input_frame, textvariable=self.cantidad_var).grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Crear un LabelFrame para los botones CRUD en la pestaña de productos
        button_frame = ttk.LabelFrame(product_tab, text="Acciones")
        button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Botón Limpiar en la pestaña de productos
        tk.Button(button_frame, text="Limpiar", command=self.limpiar_campos).grid(row=0, column=4, padx=5, pady=5, sticky="ew")

        # Botones CRUD dentro del LabelFrame en la pestaña de productos
        tk.Button(button_frame, text="Crear", command=self.create_product).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(button_frame, text="Buscar", command=self.buscar_product).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        tk.Button(button_frame, text="Actualizar", command=self.update_product).grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        tk.Button(button_frame, text="Eliminar", command=self.delete_selected_product).grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Campo de entrada para el código de barras en la pestaña de productos
        codigo_entry = tk.Entry(input_frame, textvariable=self.codigo_var)
        codigo_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Crear un Treeview para mostrar los datos de la base de datos en la pestaña de productos
        self.tree = ttk.Treeview(product_tab, columns=("ID", "Nombre", "Código de Barras", "Marca", "Precio", "Cantidad"))
        self.tree.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.tree.heading("#0", text="")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Código de Barras", text="Código de Barras")
        self.tree.heading("Marca", text="Marca")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.column("#0", width=50)  # Configurar la anchura de la columna ID
        for col in ("Nombre", "Código de Barras", "Marca", "Precio", "Cantidad"):
            self.tree.column(col, width=100)  # Configurar la anchura de las otras columnas
        self.show_data_in_treeview()

        # Pestaña de Ventas
        self.add_sales_tab(notebook)

        # Pestaña de Cobro de Fiados
        self.add_fiados_tab(notebook)

        # Pestaña de Embases Prestados
        self.add_embases_prestados_tab(notebook)

        # Configurar el Grid para que los componentes se expandan automáticamente
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

    def add_sales_tab(self, notebook):
        # Agregar la pestaña de ventas al cuaderno
        sales_tab = ttk.Frame(notebook)
        notebook.add(sales_tab, text='Ventas')
        
        # Variables de control para los campos de entrada
        self.nombre_sales = tk.StringVar()
        self.marca_sales = tk.StringVar()
        self.precio_sales = tk.DoubleVar()
        self.cantidad_sales = tk.IntVar()
        self.codigo_sales = tk.IntVar()
       
            # Crear una etiqueta y un campo de entrada para el código de barras en la pestaña de ventas
        tk.Label(sales_tab, text="Código de Barras:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(sales_tab, textvariable=self.codigo_sales).grid(row=0, column=1, padx=5, pady=5, sticky="w")
            
            # Vincular la función de captura al evento de modificación del campo de entrada del código de barras
            
        input_sales_tab = ttk.LabelFrame(sales_tab, text="Datos del Venta")
        input_sales_tab.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
            
        tk.Label(input_sales_tab, text="Nombre:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(input_sales_tab, textvariable=self.nombre_sales).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(input_sales_tab, text="Marca:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(input_sales_tab, textvariable=self.marca_sales ).grid(row=3, column=1, padx=5, pady=5, sticky="w")

        tk.Label(input_sales_tab, text="Precio:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(input_sales_tab, textvariable=self.precio_sales).grid(row=4, column=1, padx=5, pady=5, sticky="w")

        tk.Label(input_sales_tab, text="Cantidad:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(input_sales_tab, textvariable=self.cantidad_sales).grid(row=5, column=1, padx=5, pady=5, sticky="w")
            
        # Crear un LabelFrame para los botones CRUD en la pestaña de productos
        button_frame_sales_tab = ttk.LabelFrame(sales_tab, text="Acciones")
        button_frame_sales_tab.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
            
        # Botón Limpiar en la pestaña de productos
        tk.Button(button_frame_sales_tab, text="Limpiar Venta", command=self.limpiar_campos_sales).grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Botones CRUD dentro del LabelFrame en la pestaña de productos
        tk.Button(button_frame_sales_tab, text="Actualizar Venta", command=self.update_product).grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(button_frame_sales_tab, text="Eliminar Venta", command=self.delete_selected_product).grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        # Crear un Treeview para mostrar los datos de ventas en la pestaña de ventas
        sales_tree = ttk.Treeview(sales_tab, columns=("ID", "Nombre", "Código de Barras", "Marca", "Precio", "Cantidad"))
        sales_tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        sales_tree.heading("#0", text="")
        sales_tree.heading("ID", text="ID")
        sales_tree.heading("Nombre", text="Nombre")
        sales_tree.heading("Código de Barras", text="Código de Barras")
        sales_tree.heading("Marca", text="Marca")
        sales_tree.heading("Precio", text="Precio")
        sales_tree.heading("Cantidad", text="Cantidad")
        sales_tree.column("#0", width=50)  # Configurar la anchura de la columna ID
        for col in ("Nombre", "Código de Barras", "Marca", "Precio", "Cantidad"):
            sales_tree.column(col, width=100)  # Configurar la anchura de las otras columnas

        
    def limpiar_campos_sales(self):
        # Limpiar los campos de entrada
        self.nombre_sales.set("")
        self.codigo_sales.set("")
        self.marca_sales.set("")
        self.precio_sales.set("")
        self.cantidad_sales.set("")

    def add_fiados_tab(self, notebook):
        # Agregar la pestaña de cobro de fiados al cuaderno
        fiados_tab = ttk.Frame(notebook)
        notebook.add(fiados_tab, text='Cobro de Fiados')

        # Crear una etiqueta y un campo de entrada para el nombre en la pestaña de cobro de fiados
        tk.Label(fiados_tab, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        nombre_entry = tk.Entry(fiados_tab)
        nombre_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Crear una etiqueta y un campo de entrada para el monto en la pestaña de cobro de fiados
        tk.Label(fiados_tab, text="Monto:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        monto_entry = tk.Entry(fiados_tab)
        monto_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Crear una etiqueta y un campo de entrada para la fecha en la pestaña de cobro de fiados
        tk.Label(fiados_tab, text="Fecha:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        fecha_entry = tk.Entry(fiados_tab)
        fecha_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Crear un Treeview para mostrar los datos de cobro de fiados
        fiados_tree = ttk.Treeview(fiados_tab, columns=("ID", "Nombre", "Monto", "Fecha"))
        fiados_tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        fiados_tree.heading("#0", text="")
        fiados_tree.heading("ID", text="ID")
        fiados_tree.heading("Nombre", text="Nombre")
        fiados_tree.heading("Monto", text="Monto")
        fiados_tree.heading("Fecha", text="Fecha")
        fiados_tree.column("#0", width=50)  # Configurar la anchura de la columna ID
        for col in ("Nombre", "Monto", "Fecha"):
            fiados_tree.column(col, width=100)  # Configurar la anchura de las otras columnas

        # Botones para agregar, eliminar, actualizar y buscar cobro de fiados
        button_frame = tk.Frame(fiados_tab)
        button_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        tk.Button(button_frame, text="Agregar").pack(side="left", padx=5, pady=5, fill="x", expand=True)
        tk.Button(button_frame, text="Eliminar").pack(side="left", padx=5, pady=5, fill="x", expand=True)
        tk.Button(button_frame, text="Actualizar").pack(side="left", padx=5, pady=5, fill="x", expand=True)
        tk.Button(button_frame, text="Buscar").pack(side="left", padx=5, pady=5, fill="x", expand=True)

    def add_embases_prestados_tab(self, notebook):
        # Agregar la pestaña de embases prestados al cuaderno
        embases_tab = ttk.Frame(notebook)
        notebook.add(embases_tab, text='Embases Prestados')

        # Etiqueta y campo de entrada para el nombre
        tk.Label(embases_tab, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(embases_tab).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Etiqueta y campo de entrada para el tipo
        tk.Label(embases_tab, text="Tipo:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(embases_tab).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Etiqueta y campo de entrada para la fecha
        tk.Label(embases_tab, text="Fecha:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(embases_tab).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Crear un Treeview para mostrar los datos de embases prestados
        embases_tree = ttk.Treeview(embases_tab, columns=("ID", "Nombre", "Tipo", "Fecha"))
        embases_tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        embases_tree.heading("#0", text="")
        embases_tree.heading("ID", text="ID")
        embases_tree.heading("Nombre", text="Nombre")
        embases_tree.heading("Tipo", text="Tipo")
        embases_tree.heading("Fecha", text="Fecha")
        embases_tree.column("#0", width=50)  # Configurar la anchura de la columna ID
        for col in ("Nombre", "Tipo", "Fecha"):
            embases_tree.column(col, width=100)  # Configurar la anchura de las otras columnas

        # Botones para agregar, eliminar, actualizar y buscar embases prestados
        button_frame = tk.Frame(embases_tab)
        button_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        tk.Button(button_frame, text="Agregar").pack(side="left", padx=5, pady=5, fill="x", expand=True)
        tk.Button(button_frame, text="Eliminar").pack(side="left", padx=5, pady=5, fill="x", expand=True)
        tk.Button(button_frame, text="Actualizar").pack(side="left", padx=5, pady=5, fill="x", expand=True)
        tk.Button(button_frame, text="Buscar").pack(side="left", padx=5, pady=5, fill="x", expand=True)

    def limpiar_campos(self):
        # Limpiar los campos de entrada
        self.nombre_var.set("")
        self.codigo_var.set("")
        self.marca_var.set("")
        self.precio_var.set("")
        self.cantidad_var.set("")

    def create_product(self):
        nombre = self.nombre_var.get()
        codigo = self.codigo_var.get()
        marca = self.marca_var.get()
        precio = self.precio_var.get()
        cantidad = self.cantidad_var.get()

        if nombre and codigo and marca and precio and cantidad:
            self.cursor.execute("INSERT INTO productos (nombre, codigo_de_barras, marca, precio, cantidad) VALUES (?, ?, ?, ?, ?)",
                                (nombre, codigo, marca, precio, cantidad))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Producto creado correctamente.")
            self.show_data_in_treeview()  # Actualizar la vista de Treeview
            
            # Limpiar los campos excepto el nombre
            self.codigo_var.set("")
            self.marca_var.set("")
            self.precio_var.set("")
            self.cantidad_var.set("")
        else:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")

    def buscar_product(self):
        nombre_busqueda = self.nombre_var.get().strip()  # Obtener el nombre de búsqueda y eliminar espacios en blanco

        if nombre_busqueda:
            # Realizar la búsqueda en la base de datos por nombre
            self.cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", ('%' + nombre_busqueda + '%',))
            productos_encontrados = self.cursor.fetchall()

            if productos_encontrados:
                # Limpiar el Treeview antes de mostrar los resultados de la búsqueda
                self.tree.delete(*self.tree.get_children())

                # Mostrar los productos encontrados en el Treeview
                for producto in productos_encontrados:
                    self.tree.insert("", "end", values=producto)
            else:
                messagebox.showinfo("Información", f"No se encontraron productos con el nombre '{nombre_busqueda}'.")
        else:
            # Si no se ingresó ningún nombre de búsqueda, mostrar todos los productos en el Treeview
            self.show_data_in_treeview()

    def update_product(self):
        # Obtener el ID del producto seleccionado en el Treeview
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, selecciona un producto para actualizar.")
            return

        # Obtener los detalles del producto seleccionado
        item_values = self.tree.item(selected_item, 'values')
        product_id = item_values[0]  # El ID del producto es el primer valor

        # Obtener los valores actuales del producto seleccionado
        nombre_actual = self.nombre_var.get()
        codigo_actual = self.codigo_var.get()
        marca_actual = self.marca_var.get()
        precio_actual = self.precio_var.get()
        cantidad_actual = self.cantidad_var.get()

        # Validar si se han realizado cambios en los campos
        if nombre_actual == item_values[1] and codigo_actual == item_values[2] and marca_actual == item_values[3] \
                and precio_actual == item_values[4] and cantidad_actual == item_values[5]:
            messagebox.showinfo("Información", "No se han realizado cambios en los campos.")
            return

        # Obtener los nuevos valores introducidos por el usuario
        nombre_nuevo = self.nombre_var.get()
        codigo_nuevo = self.codigo_var.get()
        marca_nueva = self.marca_var.get()
        precio_nuevo = self.precio_var.get()
        cantidad_nueva = self.cantidad_var.get()

        # Actualizar el producto en la base de datos con los nuevos valores
        self.cursor.execute("UPDATE productos SET nombre=?, codigo_de_barras=?, marca=?, precio=?, cantidad=? WHERE id=?",
                            (nombre_nuevo, codigo_nuevo, marca_nueva, precio_nuevo, cantidad_nueva, product_id))
        self.conn.commit()
        messagebox.showinfo("Éxito", "Producto actualizado correctamente.")

        # Actualizar el Treeview para reflejar los cambios
        self.show_data_in_treeview()

    def delete_selected_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un producto para eliminar.")
            return

        confirm = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar el producto seleccionado?")
        if confirm:
            for item in selected_item:
                product_id = self.tree.item(item, "values")[0]
                self.cursor.execute("DELETE FROM productos WHERE id=?", (product_id,))
                self.conn.commit()
            messagebox.showinfo("Éxito", "Producto(s) eliminado(s) correctamente.")
            self.show_data_in_treeview()  # Actualizar la vista de Treeview

    def show_data_in_treeview(self):
        self.tree.delete(*self.tree.get_children())
        self.cursor.execute("SELECT * FROM productos")
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)


if __name__ == "__main__":
    root = tk.Tk()
    app = ProductCRUD(root)
    root.mainloop()
