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

    # Obtener fecha actual
    date_actuelle = date.today()

    # Ejecutar consulta
    query = "SELECT id, equipe1, equipe2, jour, debut, fin FROM matchs WHERE jour = %s"
    cursor.execute(query, (date_actuelle,))

    # Obtener los resultados
    results = cursor.fetchall()

    # Cerrar el cursor y la conexión
    cursor.close()
    conn.close()

    return results

# Función para obtener los datos de apuestas para un partido específico
def obtenir_mises(id_match):
    # Conexión a la base de datos
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Ejecutar consulta
    query = "SELECT cote1, cote2, id_utilisateur FROM mises WHERE id_match = %s"
    cursor.execute(query, (id_match,))

    # Obtener los resultados
    results = cursor.fetchall()

    # Cerrar el cursor y la conexión
    cursor.close()
    conn.close()

    return results

# Función para guardar los comentarios y el score de un partido
def commentaires_et_score(id_match, commentaires, score):
    # Conexión a la base de datos
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Actualizar el partido con los comentarios y el score
    query = "UPDATE matchs SET commentaires = %s, score = %s WHERE id = %s"
    cursor.execute(query, (commentaires, score, id_match))

    # Guardar los cambios en la base de datos
    conn.commit()

    # Cerrar el cursor y la conexión
    cursor.close()
    conn.close()

# Función para manejar la selección de un partido
def seleccionar_partido(event):
    item = table_matchs.selection()[0]
    id_match = table_matchs.item(item, 'text')
    values = table_matchs.item(item, 'values')

    # Obtener los datos de apuestas para el partido seleccionado
    donnees_mises = obtenir_mises(id_match)

    # Imprimir los datos de apuestas
    print("Partido seleccionado:", values)
    for donnees in donnees_mises:
        cote1, cote2, id_utilisateur = donnees
        print("Cote 1:", cote1)
        print("Cote 2:", cote2)
        print("ID utilisateur:", id_utilisateur)

    # Pedir comentarios y score al usuario
    commentaires = input("Ingrese los comentarios del partido: ")
    score = input("Ingrese el score del partido: ")

    # Guardar los comentarios y el score en la base de datos
    commentaires_et_score(id_match, commentaires, score)

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
table_matchs.bind("<Button-1>", seleccionar_partido)

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
    partido_id, *values = row
    table_matchs.insert("", tk.END, text=partido_id, values=values[:5])  # 5 valores

# Empacar el árbol de datos
table_matchs.pack()

# Iniciar bucle de eventos de la aplicación
fenetre.mainloop()
