from collections import deque
fila = deque()
fila.append("Alice")
fila.append("Bob")
fila.append("Charlie")
print(fila)

fila.popleft() #Retira o primeiro elemento da fila (FIFO)
print(fila)