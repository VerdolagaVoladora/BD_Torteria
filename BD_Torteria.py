import sqlite3

conexion = sqlite3.connect('BD_Torteria')
cursorBD = conexion.cursor()

def tablaExiste(nombre_tabla, query_creacion):
    cursorBD.execute('''SELECT COUNT(name) FROM SQLITE_MASTER WHERE TYPE='table' AND name=?''', (nombre_tabla,))
    if cursorBD.fetchone()[0] == 0:
        cursorBD.execute(query_creacion)
        conexion.commit()

# CREACIÓN DE TABLAS

# Tabla Tortas
tablaExiste('TORTAS', '''CREATE TABLE TORTAS (IDT INTEGER PRIMARY KEY AUTOINCREMENT, NOMBRE TEXT, DESCRIPCION TEXT, PRECIO REAL)''')
# Tabla Clientes
tablaExiste('CLIENTES', '''CREATE TABLE CLIENTES (IDC INTEGER PRIMARY KEY AUTOINCREMENT, NOMBRE TEXT, TELEFONO TEXT, DIRECCION TEXT)''')
# Tabla Pedidos
tablaExiste('PEDIDOS', '''CREATE TABLE PEDIDOS (IDP INTEGER PRIMARY KEY AUTOINCREMENT, ID_CLIENTE INTEGER, ID_TORTA INTEGER, FECHA DATE, CANTIDAD INTEGER, NOTA TEXT, TOTAL REAL, ESTATUS, FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTES(IDC), FOREIGN KEY (ID_TORTA) REFERENCES TORTAS(IDT))''')

# INSERCIÓN DE DATOS

# Función para insertar datos en tabla Tortas
def insertarTortas(nombre, descripcion, precio):
  cursorBD.execute('''INSERT INTO TORTAS (NOMBRE, DESCRIPCION, PRECIO) VALUES (?, ?, ?)''', (nombre, descripcion, precio))
  conexion.commit()

# Función para insertar datos en tabla Clientes
def insertarCliente(nombre, direccion, telefono):
    cursorBD.execute('''INSERT INTO CLIENTES (NOMBRE, DIRECCION, TELEFONO) VALUES (?, ?, ?)''', (nombre, telefono, direccion))
    conexion.commit()

# Función para insertar datos en la tabla Pedidos
def insertarPedido(id_cliente, id_torta, fecha, cantidad, nota, estatus= 'en proceso'):
    cursorBD.execute('''SELECT PRECIO FROM TORTAS WHERE IDT=?''', (id_torta,))
    precio = cursorBD.fetchone()[0]
    total = precio * cantidad
    cursorBD.execute('''INSERT INTO PEDIDOS (ID_CLIENTE, ID_TORTA, FECHA, CANTIDAD, NOTA, TOTAL, ESTATUS) VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                     (id_cliente, id_torta, fecha, cantidad, nota, total, estatus))
    conexion.commit()

# Datos Tortas
#insertarTortas('Torta Jamón', 'Jamón, aguacate, lechuga, jitomate, cebolla y chiles en vinagre (mayonesa y crema)', 50)
#insertarTortas('Torta Salchicha', 'Salchicha, aguacate, lechuga, jitomate, cebolla y chiles en vinagre (mayonesa y crema)', 50)
#insertarTortas('Torta Queso', 'Queso oaxaca, lechuga, jitomate, cebolla y chiles en vinagre (mayonesa y crema)', 65)
#insertarTortas('Torta Aguacate', 'Aguacate, lechuga, jitomate, cebolla y chiles en vinagre (mayonesa y crema)', 65)
#insertarTortas('Torta Carnitas', 'Carnitas, lechuga, jitomate, cebolla y chiles en vinagre (mayonesa y crema)', 70)
#insertarTortas('Torta Milanesa', 'Milanesa de pollo, frijoles, lechuga, jitomate, cebolla y chiles en vinagre (mayonesa y crema)', 70)
#insertarTortas('Torta Cubana', 'Jamón, pierna horneada, milanesa, salchicha, queso oaxaca, frijoles, huevo, aguacate, lechuga, jitomate, cebolla y chiles en vinagre (mayonesa y crema)', 85)

# Datos Clientes
#insertarCliente('Carlos Méndez', '4641234567', 'Calle Hidalgo #123, Col. Centro, Salamanca, Gto.')
#insertarCliente('Fernanda Torres', '4642345678', 'Av. Faja de Oro #456, Col. Bellavista, Salamanca, Gto.')
#insertarCliente('Luis González', '4643456789', 'Calle Obregón #789, Col. El Rosario, Salamanca, Gto.')
#insertarCliente('Valeria Ramírez', '4644567890', 'Calle Morelos #321, Col. San Juan de la Presa, Salamanca, Gto.')
#insertarCliente('Jorge Hernández', '4645678901', 'Calle Zaragoza #654, Col. Guadalupe, Salamanca, Gto.')
#insertarCliente('Ana Martínez', '4646789012', 'Calle Juárez #987, Col. San Pedro, Salamanca, Gto.')
#insertarCliente('Pedro Gutiérrez', '4647890123', 'Calle Allende #432, Col. Infonavit 1, Salamanca, Gto.')
#insertarCliente('Sofía López', '4648901234', 'Calle Revolución #876, Col. Las Reinas, Salamanca, Gto.')
#insertarCliente('Ricardo Pérez', '4649012345', 'Calle Madero #543, Col. El Vergel, Salamanca, Gto.')
#insertarCliente('Laura Ortiz', '4640123456', 'Calle Pípila #678, Col. Tamaulipas, Salamanca, Gto.')
#insertarCliente('Mario Vázquez', '4641352468', 'Calle Álvaro Obregón #901, Col. Villa Salamanca 400, Salamanca, Gto.')
#insertarCliente('Daniela Jiménez', '4642463579', 'Calle Emiliano Zapata #234, Col. La Gloria, Salamanca, Gto.')
#insertarCliente('Alejandro Sánchez', '4643574680', 'Calle Benito Juárez #789, Col. Ampliación Bellavista, Salamanca, Gto.')
#insertarCliente('Gabriela Castro', '4644685791', 'Calle Francisco I. Madero #567, Col. San Isidro, Salamanca, Gto.')
#insertarCliente('Juan Rodríguez', '4645796802', 'Calle Independencia #890, Col. Las Granjas, Salamanca, Gto.')
#insertarCliente('Mariana Morales', '4646807913', 'Calle Ignacio Allende #123, Col. El Durazno, Salamanca, Gto.')
#insertarCliente('Roberto Díaz', '4647918024', 'Calle Vicente Guerrero #456, Col. La Cruz, Salamanca, Gto.')
#insertarCliente('Cecilia Aguirre', '4648029135', 'Calle Felipe Ángeles #789, Col. Primavera, Salamanca, Gto.')
#insertarCliente('Enrique Navarro', '4649130246', 'Calle Lázaro Cárdenas #321, Col. Benito Juárez, Salamanca, Gto.')
#insertarCliente('Isabel Rojas', '4640241357', 'Calle Venustiano Carranza #654, Col. Ampliación Primavera, Salamanca, Gto.')
#insertarCliente('Francisco Flores', '4641350246', 'Calle Leona Vicario #987, Col. Lindavista, Salamanca, Gto.')
#insertarCliente('Patricia Herrera', '4642461357', 'Calle Pedro Moreno #432, Col. San Javier, Salamanca, Gto.')
#insertarCliente('Miguel Álvarez', '4643572468', 'Calle Matamoros #876, Col. Las Maravillas, Salamanca, Gto.')
#insertarCliente('Victoria Ruiz', '4644683579', 'Calle Miguel Hidalgo #543, Col. El Progreso, Salamanca, Gto.')
#insertarCliente('Eduardo Paredes', '4645794680', 'Calle José María Morelos #678, Col. Las Américas, Salamanca, Gto.')
#insertarCliente('Carla Salinas', '4646805791', 'Calle Ignacio Zaragoza #901, Col. Ampliación El Vergel, Salamanca, Gto.')
#insertarCliente('Felipe Escobar', '4647916802', 'Calle Antonio Caso #234, Col. Francisco Villa, Salamanca, Gto.')
#insertarCliente('Claudia Domínguez', '4648027913', 'Calle Mariano Abasolo #789, Col. Los Sauces, Salamanca, Gto.')
#insertarCliente('Samuel Castillo', '4649138024', 'Calle Benito Juárez #567, Col. Ampliación Guadalupe, Salamanca, Gto.')
#insertarCliente('Paola Vega', '4640249135', 'Calle Juan Aldama #890, Col. Campo Militar, Salamanca, Gto.')
#insertarCliente('Andrés Silva', '4641359135', 'Calle Vasco de Quiroga #123, Col. El Olimpo, Salamanca, Gto.')
#insertarCliente('Alejandra Núñez', '4642460246', 'Calle Francisco Villa #456, Col. Santa María, Salamanca, Gto.')
#insertarCliente('Santiago Valdez', '4643571357', 'Calle Morelia #789, Col. El Molinito, Salamanca, Gto.')
#insertarCliente('Alicia Fuentes', '4644682468', 'Calle San Antonio #321, Col. Las Lomas, Salamanca, Gto.')
#insertarCliente('Adrián Serrano', '4645793579', 'Calle Constitución #654, Col. Guadalupe Sur, Salamanca, Gto.')
#insertarCliente('Marcela Ibarra', '4646804680', 'Calle Juan Escutia #987, Col. Ampliación Primavera Norte, Salamanca, Gto.')
#insertarCliente('Leonardo Arce', '4647915791', 'Calle Francisco I. Madero #432, Col. El Pirul, Salamanca, Gto.')
#insertarCliente('Mónica Báez', '4648026802', 'Calle Libertad #876, Col. El Fénix, Salamanca, Gto.')
#insertarCliente('Javier Carrillo', '4649137913', 'Calle Fray Juan de San Miguel #543, Col. San Roque, Salamanca, Gto.')
#insertarCliente('Teresa Miranda', '4640248024', 'Calle Francisco Márquez #678, Col. La Esperanza, Salamanca, Gto.')
#insertarCliente('Diego Cordero', '4641350246', 'Calle Álvaro Obregón #901, Col. Puente de Palo, Salamanca, Gto.')
#insertarCliente('Lucía Figueroa', '4642461357', 'Calle Serafín Olarte #234, Col. Las Granjas Norte, Salamanca, Gto.')
#insertarCliente('Nicolás Montoya', '4643572468', 'Calle Vicente Guerrero #789, Col. Santa Teresa, Salamanca, Gto.')
#insertarCliente('Camila Ponce', '4644683579', 'Calle Plutarco Elías Calles #567, Col. Real de Minas, Salamanca, Gto.')
#insertarCliente('Alberto Espinoza', '4645794680', 'Calle Álamos #890, Col. La Luz, Salamanca, Gto.')
#insertarCliente('Fabiola Mejía', '4646805791', 'Calle Cerrada del Sol #123, Col. San Gabriel, Salamanca, Gto.')
#insertarCliente('Manuel Bautista', '4647916802', 'Calle Camino Real #456, Col. Los Olivos, Salamanca, Gto.')
#insertarCliente('Elena Zamora', '4648027913', 'Calle Privada de Morelos #789, Col. El Panteón, Salamanca, Gto.')
#insertarCliente('Cristian Solís', '4649138024', 'Calle José Fortiz de Domínguez #321, Col. Villas del Sol, Salamanca, Gto.')
#insertarCliente('Elena Rivas', '4640249135', 'Calle De la Rosa #654, Col. Jardines de Salamanca, Salamanca, Gto.')
#insertarCliente('Fernando Cruz', '4641355791', 'Calle Arboledas #987, Col. El Manantial, Salamanca, Gto.')
#insertarCliente('Patricia Muñoz', '4642466802', 'Calle Las Palmas #432, Col. El Cedro, Salamanca, Gto.')
#insertarCliente('Raúl Romero', '4643579135', 'Calle Las Flores #876, Col. El Valle, Salamanca, Gto.')
#insertarCliente('Julia Sánchez', '4644680246', 'Calle Hacienda de San Antonio #543, Col. El Refugio, Salamanca, Gto.')
#insertarCliente('David Vargas', '4645791357', 'Calle Avenida del Sol #678, Col. Praderas del Sol, Salamanca, Gto.')
#insertarCliente('Lorena Molina', '4646802468', 'Calle Miguel Hidalgo #901, Col. La Joya, Salamanca, Gto.')
#insertarCliente('Antonio Luna', '4647913579', 'Calle Independencia #234, Col. Las Huertas, Salamanca, Gto.')
#insertarCliente('Miriam Peña', '4648024680', 'Calle Avenida del Trabajo #789, Col. El Bajío, Salamanca, Gto.')
#insertarCliente('Esteban Ocampo', '4649135791', 'Calle 16 de Septiembre #567, Col. El Vergel Norte, Salamanca, Gto.')
#insertarCliente('Iván Sandoval', '4640246802', 'Calle Del Sol #890, Col. La Campiña, Salamanca, Gto.')

# Datos Pedidos
insertarPedido(1, 2, '2024-01-06', 2, 'Sin cebolla y jitomate (todas)', 'pagado')
insertarPedido(1, 5, '2024-01-06', 5, 'Pan tostado (todas)', 'cancelado')
insertarPedido(2, 3, '2024-01-06', 3, 'Sin cebolla (solo una)', 'pagado')
insertarPedido(3, 6, '2024-01-06', 6, '', 'pagado')
insertarPedido(4, 5, '2024-01-06', 5, 'Con chiles en vinagre extra', 'pagado')
insertarPedido(5, 2, '2024-01-06', 2, 'Sin cebolla (solo una)', 'pagado')
insertarPedido(6, 6, '2024-01-06', 6, 'Con chiles en vinagre (todas)', 'pagado')
insertarPedido(7, 7, '2024-01-06', 7, 'Sin aguacate (solo tres), de las que no tienen aguacate algunas no llevan cebolla (solo dos)', 'pagado')
insertarPedido(8, 5, '2024-01-06', 1, 'Con chiles en vinagre extra y sin cebolla', 'pagado')
insertarPedido(8, 3, '2024-01-06', 1, 'Sin lechuga', 'cancelado')
insertarPedido(9, 6, '2024-01-06', 6, '', 'pagado')
insertarPedido(10, 5, '2024-01-07', 5, '', 'pagado')
insertarPedido(11, 2, '2024-01-07', 2, 'Sin crema (solo una)', 'cancelado')
insertarPedido(12, 3, '2024-01-07', 3, 'Sin cebolla(solo una)', 'pagado')
insertarPedido(13, 3, '2024-01-07', 3, '', 'pagado')
insertarPedido(14, 7, '2024-01-07', 1, 'Sin aguacate (todas)', 'pagado')
insertarPedido(15, 1, '2024-01-07', 1, 'Con chiles en vinagre extra', 'pagado')
insertarPedido(16, 5, '2024-01-07', 5, 'Sin cebolla (todas)', 'pagado')
insertarPedido(17, 6, '2024-01-07', 6, '', 'pagado')
insertarPedido(18, 6, '2024-01-07', 6, 'Sin frijoles (solo 4), las restantes sin cebolla (solo 2)', 'pagado')
insertarPedido(19, 7, '2024-01-07', 7, '', 'pagado')
insertarPedido(20, 1, '2024-01-07', 1, '', 'pagado')
insertarPedido(20, 2, '2024-01-07', 2, '', 'cancelado')
insertarPedido(21, 2, '2024-01-07', 2, 'Sin lechuga y cebolla (solo una)', 'pagado')
insertarPedido(22, 5, '2024-01-07', 5, '', 'cancelado')
insertarPedido(23, 3, '2024-01-08', 3, 'Sin mayonesa (solo una)', 'pagado')
insertarPedido(24, 6, '2024-01-08', 6, '', 'pagado')
insertarPedido(25, 6, '2024-01-08', 6, 'Sin frijoles (todas) y sin crema (solo 2)', 'pagado')
insertarPedido(26, 7, '2024-01-08', 7, 'Sin aguacate (solo cinco)', 'pagado')
insertarPedido(27, 4, '2024-01-08', 4, '', 'pagado')
insertarPedido(28, 3, '2024-01-08', 3, '', 'pagado')
insertarPedido(29, 1, '2024-01-08', 1, 'Sin jitomate y cebolla', 'pagado')
insertarPedido(30, 3, '2024-01-08', 3, 'Pan tostado (solo uno)', 'pagado')

# Función para seleccionar datos de cualquier tabla
def seleccionarDatos(tabla):
    cursorBD.execute(f'''SELECT * FROM {tabla}''')
    return cursorBD.fetchall()

# Imprimir los datos en cada tabla
print("Tortas:", seleccionarDatos('TORTAS'))
print("Clientes:", seleccionarDatos('CLIENTES'))
print("Pedidos:", seleccionarDatos('PEDIDOS'))