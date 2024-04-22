import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3



class ProductCRUD:
    def __init__(self, root):
        self.root = root
        self.root.title("CRUD de Productos")
        self.root.geometry("800x600")  # Establecer el tamaño de la ventana principal

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
        
    def limpiar_campos(self):
        # Limpiar los campos de entrada
        self.nombre_var.set("")
        self.codigo_var.set("")
        self.marca_var.set("")
        self.precio_var.set("")
        self.cantidad_var.set("")

    def create_gui(self):
        # Crear un LabelFrame para los campos de entrada
        input_frame = ttk.LabelFrame(self.root, text="Datos del Producto")
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Etiquetas y campos de entrada dentro del LabelFrame
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

        # Crear un LabelFrame para los botones CRUD
        button_frame = ttk.LabelFrame(self.root, text="Acciones")
        button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Botón Limpiar
        tk.Button(button_frame, text="Limpiar", command=self.limpiar_campos).grid(row=0, column=4, padx=5, pady=5, sticky="ew")

        # Botones CRUD dentro del LabelFrame
        tk.Button(button_frame, text="Crear", command=self.create_product).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(button_frame, text="Buscar", command=self.buscar_product).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        tk.Button(button_frame, text="Actualizar", command=self.update_product).grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        tk.Button(button_frame, text="Eliminar", command=self.delete_selected_product).grid(row=0, column=3, padx=5, pady=5, sticky="ew")
       
        # Campo de entrada para el código de barras
        codigo_entry = tk.Entry(input_frame, textvariable=self.codigo_var)
        codigo_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Configurar un botón para iniciar la operación de escaneo y procesamiento del código de barras
        scan_button = tk.Button(input_frame, text="Operar con escáner", command=self.procesar_codigo_barras)
        scan_button.grid(row=1, column=2, padx=5, pady=5, sticky="w")
            
        # Crear un Treeview para mostrar los datos de la base de datos
        self.tree = ttk.Treeview(self.root, columns=("ID", "Nombre", "Código de Barras", "Marca", "Precio", "Cantidad"))
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

        # En el método create_gui, después de crear el Treeview
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_producto)


        # Configurar el Grid para que los componentes se expandan automáticamente
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
    
    def seleccionar_producto(self, event):
        # Obtener la fila seleccionada
        selected_item = self.tree.selection()
        if not selected_item:
            return

        # Obtener los valores de la fila seleccionada
        item_values = self.tree.item(selected_item, 'values')

        # Llenar los campos de entrada con los valores obtenidos
        self.nombre_var.set(item_values[1])  # Nombre del producto
        self.codigo_var.set(item_values[2])  # Código de Barras
        self.marca_var.set(item_values[3])   # Marca
        self.precio_var.set(item_values[4])  # Precio
        self.cantidad_var.set(item_values[5])# Cantidad


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
            
    def procesar_codigo_barras(self):
        # Obtener el código de barras del campo de entrada
        codigo_barras = self.codigo_var.get()
        # Verificar si el campo no está vacío y se ha ingresado un código
        if codigo_barras.strip():
            # Verificar si el código de barras está en la base de datos
            producto = self.verificar_codigo_barras(codigo_barras)
            if producto:
                # Si el producto existe, actualizar la cantidad
                self.actualizar_cantidad_producto(codigo_barras)
                messagebox.showinfo("Éxito", "Producto encontrado en la base de datos. La cantidad ha sido actualizada.")
                # Limpiar los campos después de la actualización
                self.limpiar_campos()
                # Actualizar la vista del Treeview
                self.show_data_in_treeview()
            else:
                messagebox.showerror("Error", "El producto con el código de barras ingresado no existe en la base de datos.")
    

    def show_data_in_treeview(self):
        self.tree.delete(*self.tree.get_children())
        self.cursor.execute("SELECT * FROM productos")
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)
    
    
        

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductCRUD(root)
    root.mainloop()
