# Proyecto 2 / Analizador Semantico
# Estructuras de Datos

# Estudiantes
# Cristopher Chanto Chavarria / 402480221 / 6pm
# Isaac Mendez Rodriguez / 118090020 / 6pm
# Ignacio Ledezma Hidalgo / 402520080 / 8pm

from analizador_codigo import AnalizadorCodigo
from utilidades import UtilidadesArchivo


def main():
    # Cambiar nombre del archivo para probar diferentes casos
    archivo = "Funcion4.txt"

    # Imprimir archivo para verificar la lectura correcta del archivo
    UtilidadesArchivo.mostrar_contenido_archivo(archivo)

    # Analizador Semántico
    analizador = AnalizadorCodigo()
    analizador.analizar_codigo_fuente(archivo)


if __name__ == "__main__":
    main()
