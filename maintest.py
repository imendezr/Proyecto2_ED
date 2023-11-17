from analizador_codigo import AnalizadorCodigo
from tabla_simbolos import TablaSimbolos
from utilidades import UtilidadesArchivo

def main():
    # Nombre del archivo a analizar
    archivo_codigo = "Funcion3.txt"

    # Crea instancias de las clases
    analizador = AnalizadorCodigo()
    tabla_simbolos = TablaSimbolos()

    try:
        # Obtén y muestra el tipo de la función principal
        tipo_funcion_principal = analizador.obtener_tipo_funcion(archivo_codigo)
        print(f"Tipo de la función principal: {tipo_funcion_principal}")

        # Analiza las declaraciones en el archivo de código
        analizador.analizar_declaraciones(archivo_codigo)

        # Muestra la tabla de símbolos antes de entrar al nuevo alcance
        print("\nTabla de Símbolos (antes de entrar al nuevo alcance):")
        for nombre, info in tabla_simbolos.simbolos.items():
            print(f"{nombre}: {info}")

        # Agrega un símbolo en el alcance actual
        tabla_simbolos.agregar_simbolo("nueva_variable", "int")

        # Busca un símbolo y muestra su información
        simbolo_buscado = tabla_simbolos.buscar_simbolo("nueva_variable")
        print(f"\nInformación del símbolo buscado: {simbolo_buscado}")

        # Elimina un símbolo y muestra la tabla de símbolos después de la eliminación
        tabla_simbolos.eliminar_simbolo("nueva_variable")
        print("\nTabla de Símbolos (después de eliminar un símbolo):")
        for nombre, info in tabla_simbolos.simbolos.items():
            print(f"{nombre}: {info}")

        # Entra a un nuevo alcance y agrega un símbolo
        tabla_simbolos.entrar_alcance("nuevo_alcance")
        tabla_simbolos.agregar_simbolo("otra_variable", "float")

        # Muestra la tabla de símbolos después de entrar al nuevo alcance y agregar un símbolo
        print("\nTabla de Símbolos (después de entrar al nuevo alcance y agregar un símbolo):")
        for nombre, info in tabla_simbolos.simbolos.items():
            print(f"{nombre}: {info}")

        # Sale del alcance actual y muestra la tabla de símbolos después de salir del alcance
        tabla_simbolos.salir_alcance()
        print("\nTabla de Símbolos (después de salir del alcance):")
        for nombre, info in tabla_simbolos.simbolos.items():
            print(f"{nombre}: {info}")

    except Exception as e:
        print(f"Error en el análisis: {e}")

if __name__ == "__main__":
    main()
