import re

from tabla_simbolos import TablaSimbolos
from utilidades import UtilidadesArchivo


class AnalizadorCodigo:
    tipos_variables = {'void', 'int', 'float', 'string'}
    palabras_reservadas = {'if', 'else', 'while', 'return'}

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

    def reportar_error(self,
                       mensaje):  # Metodo que muestra cada linea de error que contiene un codigo provisto en formato .txt
        error_completo = f"Error – Linea {self.numero_linea}: {mensaje}"
        self.errores.append(error_completo)

    def obtener_tipo_funcion(self,
                             file_name):  # Obtiene el tipo de dato de la funcion general (basado en los 4 datos pre-establecidos)
        try:
            contenido = UtilidadesArchivo.leer_archivo(file_name)  # Lee el contenido del archivo de texto
            match = re.search(r'\b(\w+)\s+\w+\([^)]*\)\s*{',
                              contenido)  # Expresion regular para capturar el tipo de retorno
            if match:
                return match.group(
                    1)  # Devuelve el contenido de la primera parte del codigo, que coincide con el tipo de dato de la funcion
            else:
                return "No se pudo determinar el tipo de funcion"
        except FileNotFoundError:  # En caso de que no exista un archivo con ese nombre
            return f"El archivo '{file_name}' no existe en este contexto"
        except Exception as e:
            return f"No se pudo leer correctamente el archivo: {e}"

    def analizar_declaraciones(self,
                               file_name):  # Lee y analiza cada linea individualmente utilizando un split, utiliza el metodo analizar_linea
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
                self.verificar_uso_variable_dentro_funcion(
                    linea)  # Verificar el uso de variables no declaradas dentro de la función
                self.analizar_estructura_control(linea)
                self.analizar_asignacion(linea)
        else:  # Si no esta en el cuerpo de una funcion, esta leyendo fuera de una funcion (ejemplo para variables globales)
            self.verificar_uso_variable_global(
                linea)  # Verificar si se usa una variable no declarada antes de su declaración
            tipo_retorno = self.analizar_declaracion_funcion(linea)
            if tipo_retorno:
                self.en_funcion = True
                self.tipo_retorno_funcion_actual = tipo_retorno  # Almacena el tipo de dato de la funcion
                self.lineas_funcion_actual = [linea.strip()]

            self.analizar_declaracion_variable(linea)  # Analiza las variables existentes en el codigo

    def verificar_uso_variable_dentro_funcion(self, linea):
        palabras = linea.split()
        for palabra in palabras:
            if palabra.isidentifier() and palabra not in self.tipos_variables and palabra not in self.palabras_reservadas:
                # Verificar en el alcance actual primero, luego en el global
                simbolo = self.tabla_simbolos.buscar_simbolo(palabra, alcance=self.tabla_simbolos.alcance_actual) or \
                          self.tabla_simbolos.buscar_simbolo(palabra, alcance='global')
                if not simbolo:
                    self.reportar_error(f"Variable '{palabra}' no ha sido declarada en el alcance actual o global")
                    break

    def verificar_uso_variable_global(self, linea):
        palabras = linea.split()
        for palabra in palabras:
            if palabra.isidentifier():
                # Verificar si la palabra es una variable y no una palabra reservada
                if palabra not in self.tipos_variables and not self.tabla_simbolos.buscar_simbolo(palabra,
                                                                                                  alcance='global'):
                    self.reportar_error(f"Variable '{palabra}' no está declarada")
                    break

    def analizar_estructura_control(self, linea):
        """Analiza las estructuras de control (if y while), que son sentencias condicionales reservadas
        La variable condicion_match determina si existen las palabras reservadas if, while, y de ser asi
        extrae la informacion.
        El ciclo determina si existe un simbolo inexistente o que no ha sido declarado en el codigo"""
        condicion_match = re.search(r'if\s*\((.*)\)\s*{', linea) or re.search(r'while\s*\((.*)\)\s*{', linea)
        if condicion_match:
            condicion = condicion_match.group(1)
            for var in condicion.split():
                if var.isidentifier():
                    # Buscar primero en el alcance actual, luego en el global
                    simbolo = self.tabla_simbolos.buscar_simbolo(var, alcance=self.tabla_simbolos.alcance_actual) or \
                              self.tabla_simbolos.buscar_simbolo(var, alcance='global')
                    if not simbolo:
                        self.reportar_error(f"La variable '{var}' no ha sido declarada")

    def analizar_declaracion_variable(self, linea):
        """ Analiza las variables que se encuentren en el texto y determina si coinciden con lo que se encuentra guardado
        en la tabla de símbolos. En otras palabras, lee el nombre y tipo de una variable (ej. int variable).
        Si reconoce la variable, la agrega a la tabla de símbolos.
        reportar_error: Si el tipo de variable leído no está contemplado en la tabla de símbolos o no fue declarado.
        """
        match_var = re.match(r'\b(\w+)\s+(\w+);', linea)
        if match_var:
            tipo, nombre = match_var.groups()
            if tipo in self.tipos_variables:
                # Verificar si la variable ya ha sido declarada en el mismo alcance
                if not self.tabla_simbolos.buscar_simbolo(nombre, alcance=self.tabla_simbolos.alcance_actual):
                    # Agregar la variable con el alcance actual
                    self.tabla_simbolos.agregar_simbolo(nombre, tipo, alcance=self.tabla_simbolos.alcance_actual)
                else:
                    self.reportar_error(f"Variable '{nombre}' ya declarada en el alcance actual.")
            else:
                self.reportar_error(f"El tipo '{tipo}' no se reconoce para '{nombre}'.")

    def analizar_asignacion(self, linea):
        """ Maneja las asignaciones de variables en el código y determina si las variables tienen valores existentes.
        Por ejemplo, en 'string variable = "Birra"', esta línea agarra la información "Birra", porque ya tiene la información del nombre y tipo de variable.

        self.reportar_error: Si la información asignada a la variable no coincide con el tipo de dato.
        """
        match = re.match(r'\b(\w+)\s*=\s*(.+);', linea)
        if match:
            nombre, valor = match.groups()
            # Buscar primero en el alcance actual
            simbolo = self.tabla_simbolos.buscar_simbolo(nombre, alcance=self.tabla_simbolos.alcance_actual)
            # Si no se encuentra en el alcance actual, buscar en el alcance global
            if not simbolo:
                simbolo = self.tabla_simbolos.buscar_simbolo(nombre, alcance='global')

            if simbolo:
                tipo_esperado = simbolo['tipo']
                tipo_valor = self.determinar_tipo(valor)
                if tipo_valor != tipo_esperado:
                    self.reportar_error(
                        f"Tipo incorrecto asignado para '{nombre}'. Se esperaba: {tipo_esperado}, y se encontró: {tipo_valor}")
            else:
                self.reportar_error(f"Variable '{nombre}' no declarada.")

    def analizar_declaracion_funcion(self, linea):
        """Analiza la declaracion de funcion (indicando la primera linea), por ejemplo int funcion(int a).
        En este caso, agarra la informacion del tipo de dato, el nombre de la funcion, y el nombre y tipo de dato de los parametros

        if tipo_retorno in self.tipos_variables: Si el tipo de dato de la funcion fue declarada, guarda y agrega la informacion de la declaracion en la tabla de simbolos"""
        match_func = re.search(r'\b(\w+)\s+(\w+)\(([^)]*)\)\s*{', linea)
        if match_func:
            tipo_retorno, nombre_funcion, parametros = match_func.groups()  # Extrae el tipo de dato, nombre de funcion, e info de parametros
            if tipo_retorno in self.tipos_variables:
                if not self.tabla_simbolos.buscar_simbolo(nombre_funcion):
                    self.tabla_simbolos.agregar_simbolo(nombre_funcion, {'tipo': tipo_retorno, 'es_funcion': True},
                                                        alcance=nombre_funcion)
                    self.validar_parametros_funcion(parametros, alcance=nombre_funcion)
                    self.tabla_simbolos.entrar_alcance(nombre_funcion)
                else:
                    self.validar_parametros_funcion(parametros)  # Valida los parametros de la funcion
                    self.tabla_simbolos.entrar_alcance(nombre_funcion)
                    self.en_funcion = True
                    self.tipo_retorno_funcion_actual = tipo_retorno  # Guarda el tipo de dato de la funcion
            else:
                self.reportar_error(f"Tipo de retorno de funcion '{tipo_retorno}' no se reconoce")
            return tipo_retorno  # Devuelve el tipo de dato de la funcion
        return None  # Si no existe declaracion de funcion

    def validar_parametros_funcion(self, parametros, alcance):
        """Determina si los parametros de la funcion cumplen con un tipo de dato conocido
        Si el tipo de dato existe en la tabla, se agregan estos parametros a la tabla de simbolos;
        de no ser asi, manda un error indicando que no se reconoce el tipo de dato"""
        for param in parametros.split(','):
            if param.strip():
                tipo, nombre = [p.strip() for p in param.split()]
                if tipo in self.tipos_variables:
                    self.tabla_simbolos.agregar_simbolo(nombre, tipo, alcance)
                else:
                    self.reportar_error(f"El tipo de dato '{tipo}' del parametro no se reconoce")

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

    def validar_parametros_retorno(self, parametros):
        # Verifica si la funcion tiene parametros, y de ser asi, determina si el tipo de retorno de la funcion es igual al del parametro
        if parametros.strip():
            tipos_parametros = [param.strip().split()[0] for param in parametros.split(',')]
            for tipo_parametro in tipos_parametros:
                if tipo_parametro != self.tipo_retorno_funcion_actual:
                    self.reportar_error(
                        f"Tipo de retorno no coincide con el tipo de dato del parametro. Esperado: {self.tipo_retorno_funcion_actual}, encontrado: {tipo_parametro}")

    def finalizar_funcion(self):
        """Verifica el final de la funcion (junto con el tipo de retorno)
        if self.tipo_retorno_funcion_actual != 'void': Si el tipo de dato de la funcion no es void, verifique cual es el tipo de dato de retorno"""
        # Verificacion del tipo de retorno de la funcion
        if self.tipo_retorno_funcion_actual != 'void':
            self.verificar_retorno_funcion()

        # Salir del alcance actual
        self.tabla_simbolos.salir_alcance()

    def determinar_tipo(self, valor):
        """Determina el valor de una funcion/variable y determina el tipo de dato asignado a este valor

        if valor.isdigit(): Si el valor es un numero cualquiera, entonces es un entero
        elif re.match(r'^\d+\.\d+$', valor): Si el valor es un numero, pero ademas tiene un . o , en la expresion, entonces es un float
        elif re.match(r'^".*"$', valor) or re.match(r"^'.*'$", valor): Si el valor es una cadena de texto (texto escrito entre comillas "" o '')

        Si el valor incluye cualquier operacion aritmetica (suma, resta, etc..), determina si el valor agregado a este operador es del mismo tipo

        :return: Si existe match de la informacion, devuelve el tipo de dato leido del archivo
        """
        valor = valor.strip()

        if valor.isdigit():
            return 'int'
        elif re.match(r'^\d+\.\d+$', valor):
            return 'float'
        elif re.match(r'^".*"$', valor) or re.match(r"^'.*'$", valor):
            return 'string'

        if any(op in valor for op in ['+', '-', '*', '/']):
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

            if 'float' in tipos:
                return 'float'
            elif 'int' in tipos:
                return 'int'
            else:
                return 'desconocido'  # Cualquier otro dato es desconocido para el analizador semantico
            # No existe un return 'string' porque para efectos de este problema, no se considera la suma de cadenas de texto

        simbolo = self.tabla_simbolos.buscar_simbolo(valor)
        if simbolo:
            return simbolo['tipo']

        return 'desconocido'

    def verificar_uso_variable(self, nombre):
        """Verifica si una variable ha sido declarada y si estáadentro del alcance correcto.
        not simbolo: Si el simbolo no fue encontrado en la tabla, la variable no ha sido declarada
        simbolo['alcance']: Comprueba si el alcance del simbolo es el alcance actual"""
        # Buscar primero en el alcance actual, luego en el global
        simbolo = self.tabla_simbolos.buscar_simbolo(nombre, alcance=self.tabla_simbolos.alcance_actual) or \
                  self.tabla_simbolos.buscar_simbolo(nombre, alcance='global')

        if not simbolo:
            self.reportar_error(f"Variable '{nombre}' no ha sido declarada o se encuentra fuera de alcance.")

    def verificar_tipo_variable(self, nombre, tipo):
        """Determina si el tipo de dato de la variable coincide para esta. En otras palabras, determina si la variable
        fue declarada en la tabla de simbolos"""
        # Buscar primero en el alcance actual, luego en el global
        simbolo = self.tabla_simbolos.buscar_simbolo(nombre, alcance=self.tabla_simbolos.alcance_actual) or \
                  self.tabla_simbolos.buscar_simbolo(nombre, alcance='global')

        if simbolo and simbolo['tipo'] != tipo:
            self.reportar_error(
                f"Tipo incorrecto para la variable '{nombre}'. Esperado: {tipo}, encontrado: {simbolo['tipo']}")
