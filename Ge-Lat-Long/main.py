"""
Demonstração do agente Ge-Lat-Long.
Executa perguntas em linguagem natural, cronometra cada consulta e exibe
o tempo de resposta (2º critério avaliado pelo cliente).
"""
import statistics
import time

from agent import LogisticsAgent

def run_exemplos():
    agent = LogisticsAgent()

    perguntas = [
        (
            "Qual a distância e o tempo de viagem do CD de Guarulhos até a "
            "Av. Paulista, 1000, São Paulo, considerando o trânsito atual?"
        ),
        "Quais são os KPIs de desempenho das entregas hoje?",
        (
            "Liste as entregas do cliente 'FarmaPlus' e, para cada uma, "
            "calcule o tempo de viagem do CD de origem até o destino."
        ),
        (
            "Cadastre um novo endereço de origem 'CD Campinas, SP' e um novo "
            "endereço de destino 'Shopping Eldorado, Av. Rebouças, 3970, "
            "São Paulo, SP' para o cliente FarmaPlus, usando register_address."
        ),
    ]

    tempos = []
    for pergunta in perguntas:
        print("=" * 60)
        print(f"PERGUNTA: {pergunta}")
        print("=" * 60)
        inicio = time.perf_counter()
        resposta = agent.ask(pergunta)
        decorrido = time.perf_counter() - inicio
        tempos.append(decorrido)
        print(resposta)
        print(f"\n[Tempo de resposta: {decorrido:.2f} s]")
        print()

    print("=" * 60)
    print("RESUMO DE DESEMPENHO (critério avaliado pelo cliente)")
    print("=" * 60)
    for pergunta, t in zip(perguntas, tempos):
        rotulo = " ".join(pergunta.split())[:65]
        print(f"  {rotulo}... -> {t:.2f} s")
    print(
        f"\nMínimo: {min(tempos):.2f} s | Máximo: {max(tempos):.2f} s | "
        f"Média: {statistics.mean(tempos):.2f} s"
    )

if __name__ == "__main__":
    run_exemplos()