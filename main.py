# Proyecto 2 / Analizador Semantico
# Estructuras de Datos

# Estudiantes
# Cristopher Chanto Chavarria / 402480221 / 6pm
# Isaac Mendez Rodriguez / 118090020 / 6pm
# Ignacio Ledezma Hidalgo / 402520080 / 8pm

from analizador_codigo import AnalizadorCodigo
from utilidades import UtilidadesArchivo


def main():
    # Se puede cambiar el nombre del archivo a cualquiera existente para mostrar su funcionalidad
    archivo = "Funcion4.txt"

    # Este metodo es solo para mostrar el contenido del archivo y determinar que se lee correctamente
    UtilidadesArchivo.mostrar_contenido_archivo(archivo)

    # Programa de analizador de codigo
    analizador = AnalizadorCodigo()
    analizador.analizar_codigo_fuente(archivo)

    analizador.tabla_simbolos.mostrar_tabla()


if __name__ == "__main__":
    main()
