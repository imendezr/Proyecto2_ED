# Proyecto 2 / Analizador Semantico
# Estructuras de Datos

# Estudiantes
# Cristopher Chanto Chavarria / 402480221 / 6pm
# Isaac Mendez Rodriguez / / 6pm
# Ignacio Ledezma Hidalgo / 402520080 / 8pm

import ast

# Primer paso, leer el archivo
def leer_archivo(file_name):
    with open(file_name, 'r') as file:
        contenido = file.read()
    return contenido

# Creacion de los diccionarios
datos_funcion = {} # Diccionario que guarda la informacion de las funciones
tipos_variables = {} # Diccionario que guarda la informacion de los nombres de los tipos de variables

nombre_funcion = "mi_funcion"
tipo_retorno = "int"

datos_funcion[nombre_funcion] = tipo_retorno

# Guardar tipos de datos de variables
tipos_variables['variable1'] = 'int'
tipos_variables['variable2'] = 'string'
tipos_variables['variable3'] = 'float'
tipos_variables['variable4'] = 'void'

codigo_fuente = leer_archivo('Funcion1.txt')