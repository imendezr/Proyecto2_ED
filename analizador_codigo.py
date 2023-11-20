import re

from tabla_simbolos import TablaSimbolos
from utilidades import UtilidadesArchivo


class AnalizadorCodigo:
    tipos_variables = {'void', 'int', 'float', 'string'}

    def __init__(self):
        self.errores = []
        self.tabla_simbolos = TablaSimbolos()
        self.numero_linea = 0
        self.en_funcion = False
        self.tipo_retorno_funcion_actual = None
        self.lineas_funcion_actual = []

    def analizar_codigo_fuente(self, file_name):  # Analisis semantico del archivo a leer
        self.analizar_declaraciones(file_name)

        if not self.errores:
            print("No hay errores en el codigo fuente.")
        else:
            print("Errores encontrados en el codigo:")
            for error in self.errores:
                print(error)

    def reportar_error(self, mensaje):  # Metodo que muestra cada linea de error que contiene un codigo provisto en formato .txt
        error_completo = f"Error – Linea {self.numero_linea}: {mensaje}"
        self.errores.append(error_completo)
        print(error_completo)  # Muestra la linea de errores como si fuera un stringstream

    def obtener_tipo_funcion(self, file_name):  # Obtiene el tipo de dato de la funcion general (basado en los 4 datos pre-establecidos)
        try:
            contenido = UtilidadesArchivo.leer_archivo(file_name)  # Lee el contenido del archivo de texto
            match = re.search(r'\b(\w+)\s+\w+\([^)]*\)\s*{', contenido)  # Expresion regular para capturar el tipo de retorno
            if match:
                return match.group(1)  # Devuelve el contenido de la primera parte del codigo, que coincide con el tipo de dato de la funcion
            else:
                return "No se pudo determinar el tipo de funcion"
        except FileNotFoundError:  # En caso de que no exista un archivo con ese nombre
            return f"El archivo '{file_name}' no existe en este contexto"
        except Exception as e:
            return f"No se pudo leer correctamente el archivo: {e}"

    def analizar_declaraciones(self, file_name):  # Lee y analiza cada linea individualmente utilizando un split, utiliza el metodo analizar_linea
        try:
            contenido = UtilidadesArchivo.leer_archivo(file_name)
            lineas = contenido.split('\n')
            for linea in lineas:
                self.analizar_linea(linea)
        except Exception as e:
            print(f"Error al tratar de analizar el archivo: {e}")

    # Metodo principal, encargado de revisar linea por linea del archivo que se le pasa en el main
    def analizar_linea(self, linea):
        self.numero_linea += 1

        if not linea.strip() or linea.strip().startswith('#'):  # Si la linea es un comentario o si esta en blanco
            return

        if self.en_funcion:  # Verificar si se encuentra en el cuerpo de una funcion
            self.lineas_funcion_actual.append(linea.strip())
            if re.match(r'^\}', linea):  # Si encuentra una llave cerrada, significa que llego al final de la funcion
                self.finalizar_funcion()
                self.en_funcion = False
                self.tipo_retorno_funcion_actual = None
                self.lineas_funcion_actual = []
            else:
                self.analizar_estructura_control(linea)
                self.analizar_asignacion(linea)
        else:  # Si no esta en el cuerpo de una funcion, esta leyendo fuera de una funcion (ejemplo para variables globales)
            tipo_retorno = self.analizar_declaracion_funcion(linea)
            if tipo_retorno:
                self.en_funcion = True
                self.tipo_retorno_funcion_actual = tipo_retorno  # Almacena el tipo de dato de la funcion
                self.lineas_funcion_actual = [linea.strip()]

            self.analizar_declaracion_variable(linea)  # Analiza las variables existentes en el codigo

    def analizar_estructura_control(self, linea):
        """Analiza las estructuras de control (if y while), que son sentencias condicionales reservadas
        La variable condicion_match determina si existen las palabras reservadas if, while, y de ser asi
        extrae la informacion.
        El ciclo determina si existe un simbolo inexistente o que no ha sido declarado en el codigo"""
        condicion_match = re.search(r'if\s*\((.*)\)\s*{', linea) or re.search(r'while\s*\((.*)\)\s*{', linea)
        if condicion_match:
            condicion = condicion_match.group(1)
            for var in condicion.split():
                if var.isidentifier() and not self.tabla_simbolos.buscar_simbolo(var):
                    self.reportar_error(f"La variable '{var}' no ha sido declarada")

    def analizar_declaracion_variable(self, linea):
        """Analiza las variables que se encuentren en el texto y determina si coinciden con lo que se encuentra guardado
        en la tabla de simbolos.
        Si reconoce la variable, lo agrega a la tabla de simbolos"""
        match_var = re.match(r'\b(\w+)\s+(\w+);', linea)
        if match_var:
            tipo, nombre = match_var.groups()
            if tipo in self.tipos_variables:
                self.tabla_simbolos.agregar_simbolo(nombre, tipo)
            else:
                self.reportar_error(f"El tipo '{tipo}' no se reconoce '{nombre}'.")

    def analizar_asignacion(self, linea):
        match = re.match(r'\b(\w+)\s*=\s*(.+);', linea)
        if match:
            nombre, valor = match.groups()
            # Buscar primero en el alcance actual, luego en el global
            simbolo = self.tabla_simbolos.buscar_simbolo(nombre, alcance=self.tabla_simbolos.alcance_actual) or \
                      self.tabla_simbolos.buscar_simbolo(nombre, alcance='global')
            if simbolo:
                tipo_esperado = simbolo['tipo']
                tipo_valor = self.determinar_tipo(valor)
                if tipo_valor != tipo_esperado:
                    self.reportar_error(
                        f"Tipo incorrecto en asignación para '{nombre}'. Esperado: {tipo_esperado}, encontrado: {tipo_valor}")
            else:
                self.reportar_error(f"Variable '{nombre}' no declarada.")

    def analizar_declaracion_funcion(self, linea):
        match_func = re.search(r'\b(\w+)\s+(\w+)\(([^)]*)\)\s*{', linea)
        if match_func:
            tipo_retorno, nombre_funcion, parametros = match_func.groups()
            if tipo_retorno in self.tipos_variables:
                if not self.tabla_simbolos.buscar_simbolo(nombre_funcion):
                    self.tabla_simbolos.agregar_simbolo(nombre_funcion, {'tipo': tipo_retorno, 'es_funcion': True},
                                                        alcance=nombre_funcion)
                    self.validar_parametros_funcion(parametros, alcance=nombre_funcion)
                    self.tabla_simbolos.entrar_alcance(nombre_funcion)
                else:
                    self.tabla_simbolos.agregar_simbolo(nombre_funcion, {'tipo': tipo_retorno, 'es_funcion': True})
                    self.validar_parametros_funcion(parametros)
                    self.tabla_simbolos.entrar_alcance(nombre_funcion)
                    self.en_funcion = True
                    self.tipo_retorno_funcion_actual = tipo_retorno  # Guarda el tipo de retorno de la función actual
            else:
                self.reportar_error(f"Tipo de retorno de función '{tipo_retorno}' no reconocido.")
            return tipo_retorno  # Devuelve el tipo de retorno
        return None  # Devuelve None si no se encontró una declaración de función

    def validar_parametros_funcion(self, parametros, alcance):
        for param in parametros.split(','):
            if param.strip():
                tipo, nombre = [p.strip() for p in param.split()]
                if tipo in self.tipos_variables:
                    self.tabla_simbolos.agregar_simbolo(nombre, tipo, alcance)
                else:
                    self.reportar_error(f"Tipo de parámetro '{tipo}' no reconocido en la función.")

    def verificar_retorno_funcion(self):
        if self.tipo_retorno_funcion_actual != 'void':
            sentencia_retorno_encontrada = False
            for linea in self.lineas_funcion_actual:
                if linea.startswith('return'):
                    sentencia_retorno_encontrada = True
                    match_retorno = re.match(r'return\s+(.+);', linea)
                    if match_retorno:
                        valor_retorno = match_retorno.group(1)
                        tipo_valor = self.determinar_tipo(valor_retorno)
                        if tipo_valor != self.tipo_retorno_funcion_actual:
                            self.reportar_error(
                                f"Tipo de retorno no coincide con la declaración de la función. Esperado: {self.tipo_retorno_funcion_actual}, encontrado: {tipo_valor}")
            if not sentencia_retorno_encontrada and self.tipo_retorno_funcion_actual != 'void':
                self.reportar_error("Función debería retornar un valor pero no se encontró una sentencia 'return'")

    def finalizar_funcion(self):
        # Verifica el retorno de la función si es necesario
        if self.tipo_retorno_funcion_actual != 'void':
            self.verificar_retorno_funcion()

        # Salir del alcance actual
        self.tabla_simbolos.salir_alcance()

    # Métodos de Auxiliares para Análisis
    def determinar_tipo(self, valor):
        valor = valor.strip()

        # Manejo de números enteros y flotantes
        if valor.isdigit():
            return 'int'
        elif re.match(r'^\d+\.\d+$', valor):
            return 'float'

        # Manejo de cadenas de texto
        elif re.match(r'^".*"$', valor) or re.match(r"^'.*'$", valor):
            return 'string'

        # Manejo de expresiones aritméticas
        if any(op in valor for op in ['+', '-', '*', '/']):
            # Analiza cada token en la expresión
            tokens = re.findall(r'\b\w+\b', valor)
            tipos = []
            for token in tokens:
                if token.isdigit():
                    tipos.append('int')
                elif re.match(r'^\d+\.\d+$', token):
                    tipos.append('float')
                else:
                    simbolo = self.tabla_simbolos.buscar_simbolo(token)
                    if simbolo:
                        tipos.append(simbolo['tipo'])

            # Determina el tipo de la expresión basado en los tipos de los operandos
            if 'float' in tipos:
                return 'float'
            elif 'int' in tipos:
                return 'int'
            else:
                return 'desconocido'

        # Manejo de variables
        simbolo = self.tabla_simbolos.buscar_simbolo(valor)
        if simbolo:
            return simbolo['tipo']

        return 'desconocido'

    def verificar_uso_variable(self, nombre):
        simbolo = self.tabla_simbolos.buscar_simbolo(nombre)
        if not simbolo or simbolo['alcance'] != self.tabla_simbolos.alcance_actual:
            self.reportar_error(f"Variable '{nombre}' no declarada o fuera de alcance.")

    def verificar_tipo_variable(self, nombre, tipo):
        simbolo = self.tabla_simbolos.buscar_simbolo(nombre)
        if simbolo and simbolo['tipo'] != tipo:
            self.reportar_error(
                f"Tipo incorrecto para la variable '{nombre}'. Esperado: {tipo}, encontrado: {simbolo['tipo']}.")