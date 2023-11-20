class TablaSimbolos:
    def __init__(self):
        self.simbolos = {}
        self.alcance_actual = 'global'
        self.historial_alcances = [self.alcance_actual]

    # Metodo que agrega un simbolo a la tabla, para mantener el registro de nombres/tipos/funciones
    def agregar_simbolo(self, nombre, tipo, alcance=None):
        if alcance is None:
            alcance = self.alcance_actual
        self.simbolos[(nombre, alcance)] = {'tipo': tipo, 'alcance': alcance}

    def buscar_simbolo(self, nombre, alcance=None):
        if alcance is None:
            alcance = self.alcance_actual

        # Primero busca en el alcance actual
        simbolo = self.simbolos.get((nombre, alcance))
        if simbolo:
            return simbolo

        # Si no lo encuentra y no está en el alcance global, busca en el alcance global
        if alcance != 'global':
            simbolo_global = self.simbolos.get((nombre, 'global'))
            if simbolo_global:
                return simbolo_global

        return None

    def eliminar_simbolo(self, nombre, alcance=None):
        if alcance is None:
            alcance = self.alcance_actual
        clave = (nombre, alcance)
        if clave in self.simbolos:
            del self.simbolos[clave]

    def entrar_alcance(self, nuevo_alcance):
        self.historial_alcances.append(nuevo_alcance)
        self.alcance_actual = nuevo_alcance

    def salir_alcance(self):
        self.historial_alcances.pop()
        if self.historial_alcances:
            self.alcance_actual = self.historial_alcances[-1]
        else:
            self.alcance_actual = 'global'

    def mostrar_tabla(self):
        print("Tabla de Símbolos:")
        print("{:<20} {:<15} {:<10}".format("Nombre", "Tipo", "Alcance"))
        print("=" * 45)
        for (nombre, alcance), info in self.simbolos.items():
            # Extraer el tipo de forma adecuada, dependiendo de si es una función o no
            tipo = info['tipo'] if isinstance(info['tipo'], str) else f"Función ({info['tipo']['tipo']})"
            print("{:<20} {:<15} {:<10}".format(nombre, tipo, alcance))
