import re

from tabla_simbolos import TablaSimbolos
from utilidades import UtilidadesArchivo


class AnalizadorCodigo:
    tipos_variables = {'void', 'int', 'float', 'string'}

    def __init__(self):
        """Inicializa el analizador de código con su propia tabla de símbolos."""
        self.tabla_simbolos = TablaSimbolos()

    def obtener_tipo_funcion(self, file_name):
        """
        Determina el tipo de la función principal en un archivo de código fuente.

        Args:
        file_name (str): El nombre del archivo de código fuente.

        Returns:
        str: El tipo de la función principal o un mensaje de error si no se encuentra.
        """
        try:
            contenido = UtilidadesArchivo.leer_archivo(file_name)
            match = re.search(r'\b(\w+)\s+\w+\([^)]*\)\s*{', contenido)
            if match:
                return match.group(1)
            else:
                return "No se encontro el tipo de funcion"
        except FileNotFoundError:
            return f"El archivo '{file_name}' no existe en este contexto"
        except Exception as e:
            return f"No se pudo leer correctamente el archivo: {e}"

    def analizar_declaraciones(self, file_name):
        """
        Analiza las declaraciones en el archivo de código fuente.

        Args:
        file_name (str): El nombre del archivo de código fuente.
        """
        try:
            contenido = UtilidadesArchivo.leer_archivo(file_name)
            lineas = contenido.split('\n')
            for linea in lineas:
                self.analizar_linea(linea)
        except Exception as e:
            print(f"Error al analizar el archivo: {e}")

    def analizar_linea(self, linea):
        """
        Analiza una línea de código para identificar declaraciones y funciones.

        Args:
        linea (str): La línea de código fuente a analizar.
        """
        match_var = re.match(r'\b(\w+)\s+(\w+)', linea)
        if match_var and match_var.group(1) in self.tipos_variables:
            tipo, nombre = match_var.groups()
            self.tabla_simbolos.agregar_simbolo(nombre, tipo)

        match_func = re.search(r'\b(\w+)\s+(\w+)\([^)]*\)\s*{', linea)
        if match_func:
            tipo, nombre = match_func.groups()
            self.tabla_simbolos.agregar_simbolo(nombre, {'tipo': tipo, 'es_funcion': True})
