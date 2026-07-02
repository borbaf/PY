import matplotlib.pyplot as plt

#Dados
x = ["Joao", "Ronaldo", "Victor", "Bruno", "Domingos"]
y = [10000, 20000, 15000, 25000, 30000]

plt.bar(x, y)


plt.xlim(left=0)
plt.ylim(bottom=0)
plt.Color = 'brown'

#Add Rotulos
plt.xlabel("Nomes")    
plt.ylabel("Salário")
plt.title("Salário dos Funcionários")
plt.show()
