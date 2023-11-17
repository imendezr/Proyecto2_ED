# Proyecto 2 / Analizador Semantico
# Estructuras de Datos

# Estudiantes
# Cristopher Chanto Chavarria / 402480221 / 6pm
# Isaac Mendez Rodriguez / / 6pm
# Ignacio Ledezma Hidalgo / 402520080 / 8pm

import re


# Primer paso, leer el archivo
def leer_archivo(file_name):
    with open(file_name, 'r') as file:
        contenido = file.read()
    return contenido


def mostrar_contenido_archivo(file_name):  # Funcion adicional, para determinar si se esta leyendo correctamente el contenido del archivo
    try:
        with open(file_name, 'r') as file:
            contenido = file.read()
            print(contenido)  # Imprima lo que tiene el archivo
    except FileNotFoundError:
        print(f"El archivo '{file_name}' no fue encontrado.") # Si no existe ningun archivo con ese nombre
    except Exception as e:
        print(f"No se pudo leer correctamente el archivo: {e}") # Si ocurre un error no contemplado


def obtener_tipo_funcion(file_name):  # Funcion para determinar el tipo de variable de la funcion
    try:
        with open(file_name, 'r') as file:
            contenido = file.read()

            match = re.search(r'\b(\w+)\s+\w+\([^)]*\)\s*{', contenido)

            if match:
                tipo_funcion = match.group(1)
                return tipo_funcion
            else:
                return "No se encontro el tipo de funcion"
    except FileNotFoundError:
        return f"El archivo '{file_name}' no existe en este contexto"
    except Exception as e:
        return f"No se pudo leer correctamente el archivo: {e}"


tipos_variables = {'void', 'int', 'float', 'string'}  # Diccionario que almacena los tipos de variables permitidos


nombre_archivo = "Funcion3.txt"
mostrar_contenido_archivo(nombre_archivo)
tipo_funcion = obtener_tipo_funcion(nombre_archivo)
print("\nTipo de variable de la funcion:", tipo_funcion)
