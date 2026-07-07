x = int(input("inicio do Intervalo: "))
y = int(input("fim do Intervalo: "))


print(f"\nListando os números pares entre {x} e {y}:")


for i in range(x, y+1):
    if i % 2 == 0:
        print(i, end=" ") 