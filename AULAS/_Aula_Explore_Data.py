import seaborn as sns
import matplotlib.pyplot as plt

voos = sns.load_dataset('flights')
voos = voos.pivot(index="month", columns="year", values="passengers")

plt.figure(figsize=(10, 6))

sns.heatmap(data=voos, annot=True, cmap="coolwarm", fmt="d", linewidths=0.5, linecolor="black")

plt.show()      