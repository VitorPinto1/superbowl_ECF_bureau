
import mysql.connector
import tkinter as tk
from tkinter import ttk
from datetime import date

# Configuración de la base de datos
config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'PEPE',
    'password': 'PEPE',
    'database': 'bdsuperbowl'
}

# Función para obtener los datos de la tabla "matchs"
def obtenir_donnees_du_jour():
    # Conexión a la base de datos
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # obtenir date
    date_actuelle = date.today()

    # Ejecutar consulta
    query = "SELECT equipe1, equipe2, jour, debut, fin FROM matchs WHERE jour = %s"
    cursor.execute(query, (date_actuelle,))

    # Obtener los resultados
    results = cursor.fetchall()

    # Cerrar el cursor y la conexión
    cursor.close()
    conn.close()

    return results

# Crear ventana de aplicación
fenetre = tk.Tk()
fenetre.title("Matchs")

# Crear árbol de datos
table_matchs = ttk.Treeview(fenetre)
table_matchs["columns"] = ("equipo1", "equipo2", "jour", "debut", "fin")

# Definir encabezados de columnas
table_matchs.heading("equipo1", text="Equipe 1")
table_matchs.heading("equipo2", text="Equipe 2")
table_matchs.heading("jour", text="Jour")
table_matchs.heading("debut", text="Debut")
table_matchs.heading("fin", text="Fin")

# Obtener datos de la tabla "matchs"
donnees_matchs_actuelles = obtenir_donnees_du_jour()

# Insertar los datos en el árbol de datos
for row in donnees_matchs_actuelles:
    table_matchs.insert("", tk.END, values=row)

# Empacar el árbol de datos
table_matchs.pack()

# Iniciar bucle de eventos de la aplicación
fenetre.mainloop()