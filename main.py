# Proyecto 2 / Analizador Semantico
# Estructuras de Datos

# Estudiantes
# Cristopher Chanto Chavarria / / 6pm
# Isaac Mendez Rodriguez / / 6pm
# Ignacio Ledezma Hidalgo / 402520080 / 8pm

# Primer paso, leer el archivo
def leer_archivo(file_name):
    with open(file_name, 'r') as file:
        contenido = file.read()
    return contenido