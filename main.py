import mysql.connector
import tkinter as tk
from tkinter import ttk

# Configuración de la base de datos
config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'PEPE',
    'password': 'PEPE',
    'database': 'bdsuperbowl'
}

# Función para obtener los datos de la tabla "matchs"
def obtener_datos():
    # Conexión a la base de datos
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Ejecutar consulta
    query = "SELECT equipe1, equipe2, jour, debut, fin FROM matchs"
    cursor.execute(query)

    # Obtener los resultados
    results = cursor.fetchall()

    # Cerrar el cursor y la conexión
    cursor.close()
    conn.close()

    return results

# Crear ventana de aplicación
ventana = tk.Tk()
ventana.title("Matchs")

# Crear árbol de datos
table_matchs = ttk.Treeview(ventana)
table_matchs["columns"] = ("equipo1", "equipo2", "jour", "debut", "fin")

# Definir encabezados de columnas
table_matchs.heading("equipo1", text="Equipe 1")
table_matchs.heading("equipo2", text="Equipe 2")
table_matchs.heading("jour", text="Jour")
table_matchs.heading("debut", text="Debut")
table_matchs.heading("fin", text="Fin")

# Obtener datos de la tabla "matchs"
datos = obtener_datos()

# Insertar los datos en el árbol de datos
for row in datos:
    table_matchs.insert("", tk.END, values=row)

# Empacar el árbol de datos
table_matchs.pack()

# Iniciar bucle de eventos de la aplicación
ventana.mainloop()
