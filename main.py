
import mysql.connector
import tkinter as tk
from tkinter import ttk
from datetime import date
from ttkthemes import ThemedTk

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
fenetre = ThemedTk(theme="default")
fenetre.title("Matchs")

# Crear árbol de datos con estilo mejorado
style = ttk.Style(fenetre)
style.configure("Custom.Treeview", highlightthickness=0, bd=0)
style.configure("Custom.Treeview.Heading", font=('Helvetica', 10, 'bold'))
table_matchs = ttk.Treeview(fenetre, columns=("equipo1", "equipo2", "jour", "debut", "fin"), style="Custom.Treeview")
table_matchs["columns"] = ("equipo1", "equipo2", "jour", "debut", "fin")

table_matchs["show"] = "headings"

# Desactivar redimensionamiento de columnas
table_matchs.bind("<Button-1>", lambda e: "break")

# Definir encabezados de columnas
table_matchs.heading("equipo1", text="Equipe 1")
table_matchs.heading("equipo2", text="Equipe 2")
table_matchs.heading("jour", text="Jour")
table_matchs.heading("debut", text="Debut")
table_matchs.heading("fin", text="Fin")


# Configurar columnas para que sean fijas y no modificables
column_widths = {"equipo1": 100, "equipo2": 100, "jour": 100, "debut": 100, "fin": 100}
for column, width in column_widths.items():
    table_matchs.column(column, width=width, anchor=tk.CENTER)



# Obtener datos de la tabla "matchs"
donnees_matchs_actuelles = obtenir_donnees_du_jour()

# Insertar los datos en el árbol de datos
for row in donnees_matchs_actuelles:
    table_matchs.insert("", tk.END, values=row[:5]) # 5 valeurs

# Empacar el árbol de datos
table_matchs.pack()

# Iniciar bucle de eventos de la aplicación
fenetre.mainloop()