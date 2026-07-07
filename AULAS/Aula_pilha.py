from collections import deque


fila = []
fila.append("Banana")
fila.append("Abacaxi")
fila.append("Laranja")
fila.append("Maçã")
#print(fila)

while len(fila) > 2:
  fila.pop(0)
  if len(fila) < 3: print(fila)

