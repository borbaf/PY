import seaborn as sns
import matplotlib.pyplot as plt

titanic = sns.load_dataset('titanic')
# Exemplo de gráfico de dispersão com Seaborn

df_por_sexo = titanic.groupby('sex')['survived'].sum().reset_index()

plt.figure(figsize=(8, 6))
sns.barplot(data=df_por_sexo, x='sex', y='survived')
plt.title("Sobrevivência por Sexo")
plt.xlabel("Sexo")
plt.ylabel("Número de Sobreviventes")
plt.show()      