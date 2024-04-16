from graphviz import Digraph
import pandas as pd

# Define la tabla de analisis aqui
tabla = pd.read_csv("Tabla.csv", index_col=0)

class node_stack:
  def __init__(self, symbol, lexeme):
    global count
    self.symbol = symbol
    self.lexeme = lexeme
    self.id = count
    count += 1

class node_tree:
  def __init__(self, id, symbol, lexeme):
    self.id = id
    self.symbol = symbol
    self.lexeme = lexeme
    self.children = []
    self.father = None

count = 1
stack = []

# init stack
symbol_E = node_stack('E', None)
symbol_dollar = node_stack('$', None)
stack.append(symbol_dollar)
stack.append(symbol_E)

# init tree
root = node_tree(symbol_E.id, symbol_E.symbol, symbol_E.lexeme)

entrada = [
  {
      "simbolo": "(",
      "lexema": "4",
      "nroline": 2,
      "col": 2
  },
  {
      "simbolo": "int",
      "lexema": "4",
      "nroline": 2,
      "col": 2
  },
  {
      "simbolo": "*",
      "lexema": "*",
      "nroline": 2,
      "col": 4
  },
  {
      "simbolo": "int",
      "lexema": "5",
      "nroline": 2,
      "col": 4
  },
  {
      "simbolo": ")",
      "lexema": "1",
      "nroline": 2,
      "col": 4
  },
  {
      "simbolo": "$",
      "lexema": "$",
      "nroline": 0,
      "col": 0
  },
]




# Funcion para buscar un nodo en el arbol
def buscar_nodo(id, nodo):
  if nodo.id == id:
    return nodo
  else:
    for hijo in nodo.children:
      resultado = buscar_nodo(id, hijo)
      if resultado is not None:
        return resultado
    return None

index_entrada = 0
simbolo_entrada = None

while len(stack) > 0 and (simbolo_entrada is None or simbolo_entrada != "$"):
  simbolo_entrada = entrada[index_entrada]["simbolo"]

  # Comparar la cima de la pila con el simbolo de entrada
  if stack[-1].symbol == simbolo_entrada:
    print("Terminal:", stack[-1].symbol)
    stack.pop()
    index_entrada += 1
  else:
    # Obtener la produccion de la tabla de analisis
    produccion = tabla.loc[stack[-1].symbol, simbolo_entrada]

    # Manejar errores de sintaxis
    if isinstance(produccion, float):
      print("-----------------Error en el proceso sintactico-----------------")
      break

    # Aplicar la produccion en la pila y el arbol
    if produccion != 'e':
      print("Pila antes de aplicar produccion:", [n.symbol for n in stack])
      print("Produccion:", produccion)
      padre = buscar_nodo(stack[-1].id, root)
      stack.pop()
      for simbolo in reversed(str(produccion).split()):
        nodo_p = node_stack(simbolo, entrada[index_entrada]["lexema"])
        stack.append(nodo_p)
        hijo = node_tree(nodo_p.id, nodo_p.symbol,
                         nodo_p.lexeme)  # Utiliza el lexema
        padre.children.append(hijo)
      print("Pila despues de aplicar produccion:", [n.symbol for n in stack])
    else:
      print("Pila antes de eliminar simbolo epsilon:",
            [n.symbol for n in stack])
      stack.pop()
      print("Pila despues de eliminar simbolo epsilon:",
            [n.symbol for n in stack])

print("Analisis sintactico finalizado.")

#generar dot
dot = Digraph(comment='Árbol de Derivación', format='png')
dot.node(str(root.id), root.symbol, style='filled', fillcolor='aqua')

def generar_nodos_aristas(nodo, padre_id):
  for hijo in nodo.children:
    dot.node(str(hijo.id), hijo.symbol, style='filled', fillcolor='aqua')
    dot.edge(str(padre_id), str(hijo.id))
    generar_nodos_aristas(hijo, hijo.id)

generar_nodos_aristas(root, root.id)
dot.render('CotArbol', format='png', cleanup=True)
