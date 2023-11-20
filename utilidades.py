class UtilidadesArchivo:
    @staticmethod
    def leer_archivo(file_name):
        """
        Lee el contenido de un archivo.

        Args:
        file_name (str): El nombre del archivo a leer.

        Returns:
        str: El contenido del archivo.
        """
        with open(file_name, 'r', encoding='utf-8') as file:  # Especificar la codificación aquí
            contenido = file.read()
        return contenido

    @staticmethod
    def mostrar_contenido_archivo(file_name):
        """
        Imprime el contenido de un archivo especificado.

        Args:
        file_name (str): El nombre del archivo a mostrar.
        """
        try:
            contenido = UtilidadesArchivo.leer_archivo(file_name)
            print(contenido)
        except FileNotFoundError:
            print(f"El archivo '{file_name}' no fue encontrado.")
        except Exception as e:
            print(f"No se pudo leer correctamente el archivo: {e}")
