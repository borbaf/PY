"""
Demo de agente com contexto geográfico.

Uso:
    python main.py            # roda os exemplos fixos
    python main.py --chat     # modo interativo (chat no terminal)
"""
import sys

from agent import LogisticsAgent

EXEMPLOS = [
    # Contexto geográfico real (Maps)
    "Qual a distância e o tempo de viagem do CD de Guarulhos até "
    "a Av. Paulista, 1000, São Paulo, considerando o trânsito atual?",

    # Dados proprietários (BigQuery)
    "Quais são os KPIs de desempenho das entregas hoje?",

    # Combinado: dados proprietários + contexto geográfico
    "Liste as entregas do cliente 'FarmaPlus' e, para cada uma, "
    "calcule o tempo de viagem do CD de origem até o destino.",
]

def run_exemplos():
    agent = LogisticsAgent()
    for pergunta in EXEMPLOS:
        print("\n" + "=" * 60)
        print("PERGUNTA:", pergunta)
        print("=" * 60)
        print(agent.ask(pergunta))

def run_chat():
    agent = LogisticsAgent()
    print("Torre de Controle IA - modo chat. Digite 'sair' para encerrar.\n")
    while True:
        pergunta = input("> ").strip()
        if pergunta.lower() in ("sair", "exit", "quit"):
            break
        print(agent.ask(pergunta))
        print()

if __name__ == "__main__":
    if "--chat" in sys.argv:
        run_chat()
    else:
        run_exemplos()