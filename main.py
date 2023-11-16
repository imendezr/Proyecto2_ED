# Proyecto 2 / Analizador Semantico
# Estructuras de Datos

# Estudiantes
# Cristopher Chanto Chavarria / 402480221 / 6pm
# Isaac Mendez Rodriguez / 118090020 / 6pm
# Ignacio Ledezma Hidalgo / 402520080 / 8pm

from analizador_codigo import AnalizadorCodigo
from utilidades import UtilidadesArchivo


def imprimir_tabla_simbolos(tabla_simbolos):
    """
    Imprime el contenido de la tabla de símbolos con un formato mejorado.

    Args:
    tabla_simbolos (TablaSimbolos): La tabla de símbolos a imprimir.
    """
    print("\nContenido de la tabla de símbolos:")
    for nombre, info in tabla_simbolos.simbolos.items():
        alcance = info['alcance']
        if isinstance(info['tipo'], dict):
            # Es una función
            tipo_funcion = info['tipo']['tipo']
            print(f"Función: {nombre}, Tipo: {tipo_funcion}, Alcance: {alcance}")
        else:
            # Es una variable
            tipo_variable = info['tipo']
            print(f"Variable: {nombre}, Tipo: {tipo_variable}, Alcance: {alcance}")


def imprimir_resultado_busqueda(nombre, resultado):
    """
    Imprime el resultado de la búsqueda de un símbolo en la tabla de símbolos.

    Args:
    nombre (str): El nombre del símbolo buscado.
    resultado (dict): El resultado de la búsqueda.
    """
    if resultado:
        if isinstance(resultado['tipo'], dict):
            tipo_funcion = resultado['tipo']['tipo']
            print(f"Encontrado: Función '{nombre}', Tipo: {tipo_funcion}, Alcance: {resultado['alcance']}")
        else:
            tipo_variable = resultado['tipo']
            print(f"Encontrado: Variable '{nombre}', Tipo: {tipo_variable}, Alcance: {resultado['alcance']}")
    else:
        print(f"No se encontró el símbolo '{nombre}'.")


def main():
    """
    Función principal del programa.

    Lee un archivo de código fuente, muestra su contenido, determina el tipo de la función principal, realiza un
    análisis de las declaraciones en el archivo y luego prueba la tabla de símbolos.
    """
    nombre_archivo = "Funcion3.txt"

    # Mostrar contenido para verificar la lectura correcta del archivo
    UtilidadesArchivo.mostrar_contenido_archivo(nombre_archivo)

    # Crear una instancia del AnalizadorCodigo
    analizador = AnalizadorCodigo()

    # Obtener el tipo de función del archivo y realizar análisis de declaraciones
    tipo_funcion = analizador.obtener_tipo_funcion(nombre_archivo)
    print("\nTipo de variable de la funcion:", tipo_funcion)

    # Realizar análisis de declaraciones en el archivo
    analizador.analizar_declaraciones(nombre_archivo)

    # Imprimir el contenido de la tabla de símbolos con formato mejorado
    imprimir_tabla_simbolos(analizador.tabla_simbolos)

    # Ejemplo de búsqueda de un símbolo
    simbolo_buscado = 'funcion'
    resultado = analizador.tabla_simbolos.buscar_simbolo(simbolo_buscado)
    imprimir_resultado_busqueda(simbolo_buscado, resultado)


if __name__ == "__main__":
    main()
