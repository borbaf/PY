import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def format_currency(value, pos=None):
    """Formata um número como moeda brasileira (R$)."""
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def main():
    # Dados de salários específicos
    names = ["João", "Ronaldo", "Maria", "Ana", "Carlos"]
    salaries = [3200.50, 7150.00, 5400.75, 2800.00, 4600.25]

    # Cores destacadas para João e Ronaldo
    colors = ["#1f77b4"] * len(names)
    highlight = {"João", "Ronaldo"}
    for i, name in enumerate(names):
        if name in highlight:
            colors[i] = "#ff7f0e"

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(names, salaries, color=colors)

    # Aplica a formatação de moeda no eixo Y usando FuncFormatter
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_currency))

    # Adiciona os valores formatados acima de cada barra
    formatter = ticker.FuncFormatter(format_currency)
    for bar, salary in zip(bars, salaries):
        height = bar.get_height()
        ax.annotate(
            formatter(salary),
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )

    ax.set_title("Salários dos Funcionários", fontsize=14, fontweight="bold")
    ax.set_ylabel("Salário")
    ax.set_xlabel("Funcionário")
    ax.set_ylim(0, max(salaries) * 1.15)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()