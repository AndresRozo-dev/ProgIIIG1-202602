

class CriptoAritm:
  def __init__(self, palabras, dominio):
    # Excluir los caracteres '+' e '=' del string para obtener las letras únicas
    self.variables = set(c for c in palabras if c not in ('+', '='))
    self.dominio = dominio.copy()
    self.VarDom = {k: dominio.copy() for k in self.variables}
    self.Constraints = []

  def copy(self):
    "copia rápida clonando únicamente los dominios que cambian."""
    nueva = CriptoAritm("", self.dominio)
    nueva.variables = self.variables
    nueva.VarDom = {k: v.copy() for k, v in self.VarDom.items()}
    nueva.Constraints = self.Constraints
    return nueva

  def setConstraint(self, constraint):
    self.Constraints.append(constraint)

  def LT_constraintValue(self, variables, valor):
    AnyChange = False
    for var in variables:
      OldDom = self.VarDom[var].copy()
      self.VarDom[var].difference_update(set(range(valor, 10)))
      if self.VarDom[var] != OldDom:
        AnyChange = True
    return AnyChange

  def LTE_constraintValue(self, variables, valor):
    AnyChange = False
    for var in variables:
      OldDom = self.VarDom[var].copy()
      self.VarDom[var].difference_update(set(range(valor + 1, 10)))
      if self.VarDom[var] != OldDom:
        AnyChange = True
    return AnyChange

  def GTE_constraintValue(self, variables, valor):
    """Restringe var >= valor eliminando los números menores a valor."""
    AnyChange = False
    for var in variables:
      OldDom = self.VarDom[var].copy()
      self.VarDom[var].difference_update(set(range(0, valor)))
      if self.VarDom[var] != OldDom:
        AnyChange = True
    return AnyChange

  def LT_constraint(self, variables):
    # Implementación bidireccional de var1 < var2 (consistencia de arco)
    AnyChange = False
    var1, var2 = variables[0], variables[1]

    # Evitar error si algún dominio ya quedó vacío por otra restricción
    if not self.VarDom[var1] or not self.VarDom[var2]:
      return False

    # 1. Podar var1: no puede ser >= al máximo valor posible de var2
    max_var2 = max(self.VarDom[var2])
    OldDom1 = self.VarDom[var1].copy()
    self.VarDom[var1].difference_update(set(range(max_var2, 10)))
    if self.VarDom[var1] != OldDom1:
      AnyChange = True

    # Verificar que var1 no haya quedado vacío tras la primera poda
    if not self.VarDom[var1]:
      return AnyChange

    # 2. Podar var2: no puede ser <= al mínimo valor posible de var1
    min_var1 = min(self.VarDom[var1])
    OldDom2 = self.VarDom[var2].copy()
    self.VarDom[var2].difference_update(set(range(0, min_var1 + 1)))
    if self.VarDom[var2] != OldDom2:
      AnyChange = True

    return AnyChange

  def AllDifferentConstraint(self):
    """Si una variable tiene asignado un único valor, lo remueve de las demás."""
    AnyChange = False
    valores_asignados = {}
    for var in self.variables:
      if len(self.VarDom[var]) == 1:
        valores_asignados[var] = list(self.VarDom[var])[0]

    for var in self.variables:
      if len(self.VarDom[var]) > 1:
        OldDom = self.VarDom[var].copy()
        self.VarDom[var].difference_update(valores_asignados.values())
        if self.VarDom[var] != OldDom:
          AnyChange = True
    return AnyChange

  def GlobalConsistens(self):
    while True:
      AnyChange = False
      # Primero aplicamos la restricción implícita de que todos los dígitos son diferentes
      AnyChange = self.AllDifferentConstraint() or AnyChange

      # Evaluamos las restricciones explícitas añadidas con setConstraint
      for constraint in self.Constraints:
        metodo_nombre = constraint[0]
        parametros = constraint[1:]

        metodo = getattr(self, metodo_nombre, None)
        if metodo:
          AnyChange = metodo(*parametros) or AnyChange

      if not AnyChange:
        break

  def SeleccionarVariable(self):
    # Heurística MRV (Minimum Remaining Values): selecciona la variable con el dominio más pequeño
    mejor_var = None
    min_tam = 11
    for var in self.variables:
      tam = len(self.VarDom[var])
      if 1 < tam < min_tam:
        min_tam = tam
        mejor_var = var
    return mejor_var

  def isConsistent(self):
    for var in self.variables:
      if len(self.VarDom[var]) == 0:
        return False

    valores_unicos = []
    for var in self.variables:
      if len(self.VarDom[var]) == 1:
        val = list(self.VarDom[var])[0]
        if val in valores_unicos:
          return False
        valores_unicos.append(val)
    return True

  def isFullSolution(self):
    for var in self.variables:
      if len(self.VarDom[var]) != 1:
        return False
    return True

  def isValid(self):
    LetraValor = {k: list(self.VarDom[k])[0] for k in self.variables}

    SEND = (LetraValor["S"]*1000) + (LetraValor["E"]*100) + (LetraValor["N"]*10) + (LetraValor["D"]*1)
    MORE = (LetraValor["M"]*1000) + (LetraValor["O"]*100) + (LetraValor["R"]*10) + (LetraValor["E"]*1)
    MONEY = (LetraValor["M"]*10000) + (LetraValor["O"]*1000) + (LetraValor["N"]*100) + (LetraValor["E"]*10) + (LetraValor["Y"]*1)

    return SEND + MORE == MONEY

  def backtracking(self):
    #se verifica si ya se encontró una solucion completa y valida
    if self.isFullSolution():
      if self.isValid():
        return self.VarDom
      return None

    #seleccionamos la mejor variable para empezar a recorrer
    varSel = self.SeleccionarVariable()
    if varSel is None:
      return None

    #Se define el estado actual y se aplica consistencia global
    for valor in sorted(list(self.VarDom[varSel])):
      estadoActual = self.copy()
      estadoActual.VarDom[varSel] = {valor}

      estadoActual.GlobalConsistens()

      if estadoActual.isConsistent():
        resultado = estadoActual.backtracking()
        if resultado is not None:
          return resultado

    return None

  def contarCombinaciones(self):
    """Calcula el producto del tamaño de los dominios de todas las variables."""
    total = 1
    for var in self.variables:
      total *= len(self.VarDom[var])
    return total

  def mostrarResumenDominios(self, titulo):
    """Imprime cada variable con su dominio actual y el total de combinaciones."""
    print(f"\n=== {titulo} ===")
    for var in sorted(self.variables):
      dom_ordenado = sorted(list(self.VarDom[var]))
      print(f"  {var} ({len(dom_ordenado)} opciones): {dom_ordenado}")
    print(f"-> Combinaciones máximas posibles: {self.contarCombinaciones():,}")
  
# Instanciamos el CSP para el problema SEND + MORE = MONEY
problema = CriptoAritm("SEND+MORE=MONEY", set(range(10)))

# 1. Dominio base (sin restricciones de orden ni acarreos)
comb_sin_restringir = problema.contarCombinaciones()

# Regla básica: las letras iniciales no pueden ser 0
problema.VarDom['S'].discard(0)
problema.VarDom['M'].discard(0)

# 2. restricciones
problema.setConstraint(["LTE_constraintValue", ['M'], 1])   # M <= 1
problema.setConstraint(["LT_constraint", ['O', 'M']])       # O < M
problema.setConstraint(["LT_constraint", ['M', 'S']])       # M < S
problema.setConstraint(["LT_constraint", ['O', 'S']])       # O < S
problema.setConstraint(["GTE_constraintValue", ['S'], 8])   # S >= 8
problema.setConstraint(["LT_constraint", ['E', 'N']])       # E < N

# Mostramos el estado ANTES de propagar las restricciones
problema.mostrarResumenDominios("ANTES DE GlobalConsistens()")
comb_antes = problema.contarCombinaciones()

# Ejecutamos la propagación de restricciones
problema.GlobalConsistens()

# Mostramos el estado DESPUÉS de propagar las restricciones
problema.mostrarResumenDominios("DESPUÉS DE GlobalConsistens()")
comb_despues = problema.contarCombinaciones()

# Comparativa de reducción
reduccion = (1 - (comb_despues / comb_sin_restringir)) * 100
print(f"\n--- RESUMEN DE PODA ---")
print(f"Sin ninguna restricción:      {comb_sin_restringir:,} combinaciones")
print(f"Solo quitando ceros iniciales: {comb_antes:,} combinaciones")
print(f"Tras aplicar restricciones:    {comb_despues:,} combinaciones")
print(f"Espacio de búsqueda eliminado: {reduccion:.4f}%")

# Ejecutamos el backtracking
solucion = problema.backtracking()
print("\n--- SOLUCIÓN ENCONTRADA ---")
if solucion:
  for letra in sorted(solucion):
    print(f"  {letra}: {list(solucion[letra])[0]}")
else:
  print("No se encontró solución con las restricciones dadas.")