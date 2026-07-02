import matplotlib.pyplot as plt

plt.plot([1, 2, 3], [1, 4, 9])
plt.show()


#Dados
x = ["Uva", "Banana", "Cereja", "Banana", "Laranja"]
y = [10, 20, 15, 25, 30]

plt.Color = 'green'
plt.bar(x, y)


#Add Rotulos
plt.xlabel("Frutas")    
plt.ylabel("Quantidade")
plt.title("Quantridade de Frutas")
plt.show()
