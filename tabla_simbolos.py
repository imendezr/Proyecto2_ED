class TablaSimbolos:
    def __init__(self):
        self.simbolos = {}
        self.alcance_actual = 'global'
        self.historial_alcances = [self.alcance_actual]

    def agregar_simbolo(self, nombre, tipo, alcance=None): # Metodo que agrega un simbolo a la tabla, para mantener el registro de nombres/tipos/funciones
        if alcance is None:
            alcance = self.alcance_actual
        if nombre in self.simbolos and self.simbolos[nombre]['alcance'] == alcance:
            print(f"Ya existe el simbolo '{nombre}' en '{alcance}'")
        self.simbolos[nombre] = {'tipo': tipo, 'alcance': alcance}

    def buscar_simbolo(self, nombre, alcance=None): # Busca el simbolo por medio de nombre y alcance
        if alcance is None:
            alcance = self.alcance_actual
            # Buscar en el alcance actual y luego en los globales
        simbolo = self.simbolos.get(nombre, None)
        if simbolo and simbolo['alcance'] == alcance:
            return simbolo
        elif simbolo and alcance != 'global' and simbolo['alcance'] == 'global':
            return simbolo
        return None

    def eliminar_simbolo(self, nombre, alcance=None):
        if alcance is None:
            alcance = self.alcance_actual
        if nombre in self.simbolos and self.simbolos[nombre]['alcance'] == alcance:
            del self.simbolos[nombre]

    def entrar_alcance(self, nuevo_alcance):
        self.historial_alcances.append(nuevo_alcance)
        self.alcance_actual = nuevo_alcance

    def salir_alcance(self):
        self.historial_alcances.pop()
        if self.historial_alcances:
            self.alcance_actual = self.historial_alcances[-1]
        else:
            self.alcance_actual = 'global'
