class TablaSimbolos:
    def __init__(self):
        """Inicializa la tabla de símbolos con un alcance (scope) global predeterminado."""
        self.simbolos = {}
        self.alcance_actual = 'global'
        self.historial_alcances = [self.alcance_actual]

    def agregar_simbolo(self, nombre, tipo, alcance=None):
        """
        Agrega un nuevo símbolo a la tabla.

        Args:
        nombre (str): El nombre del símbolo.
        tipo (str): El tipo del símbolo (por ejemplo, 'int', 'float').
        alcance (str, opcional): El alcance del símbolo. Si no se proporciona, se usa el alcance actual.
        """
        if alcance is None:
            alcance = self.alcance_actual
        if nombre in self.simbolos:
            print(f"Advertencia: El símbolo '{nombre}' ya existe y será sobrescrito.")
        self.simbolos[nombre] = {'tipo': tipo, 'alcance': alcance}

    def buscar_simbolo(self, nombre):
        """
        Busca un símbolo por su nombre.

        Args:
        nombre (str): El nombre del símbolo a buscar.

        Returns:
        dict or None: La información del símbolo si se encuentra, None en caso contrario.
        """
        return self.simbolos.get(nombre, None)

    def eliminar_simbolo(self, nombre):
        """
        Elimina un símbolo de la tabla.

        Args:
        nombre (str): El nombre del símbolo a eliminar.
        """
        if nombre in self.simbolos:
            del self.simbolos[nombre]

    def entrar_alcance(self, nuevo_alcance):
        """
        Entra a un nuevo nivel de alcance (scope).

        Args:
        nuevo_alcance (str): El nombre del nuevo alcance.
        """
        self.historial_alcances.append(nuevo_alcance)
        self.alcance_actual = nuevo_alcance

    def salir_alcance(self):
        """
        Sale del nivel de alcance (scope) actual y vuelve al anterior.
        Si no hay un alcance anterior, vuelve al alcance global.
        """
        self.historial_alcances.pop()
        if self.historial_alcances:
            self.alcance_actual = self.historial_alcances[-1]
        else:
            self.alcance_actual = 'global'
