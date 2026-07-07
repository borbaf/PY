import random
import string

import pandas as pd


def gerar_nome() -> str:
    nomes = [
        "Ana", "Bruno", "Carla", "Daniel", "Eduarda", "Felipe", "Gabriela",
        "Henrique", "Isabela", "João", "Karen", "Lucas", "Mariana", "Nicolas",
        "Olivia", "Paulo", "Quiteria", "Rafael", "Sofia", "Thiago", "Ursula",
        "Vanessa", "William", "Ximena", "Yasmin", "Zaira",
    ]
    sobrenomes = [
        "Silva", "Santos", "Oliveira", "Souza", "Costa", "Pereira", "Ferreira",
        "Almeida", "Carvalho", "Ribeiro", "Rodrigues", "Gomes", "Martins",
        "Araújo", "Barbosa", "Rocha", "Lima", "Mendes", "Freitas", "Dias",
    ]
    return f"{random.choice(nomes)} {random.choice(sobrenomes)}"


def gerar_matricula() -> str:
    ano = random.choice([2021, 2022, 2023, 2024])
    sufixo = "".join(random.choices(string.digits, k=6))
    return f"{ano}{sufixo}"


def gerar_curso() -> str:
    cursos = [
        "Engenharia Civil",
        "Engenharia de Software",
        "Medicina",
        "Direito",
        "Administração",
        "Ciências Contábeis",
        "Psicologia",
        "Pedagogia",
        "Enfermagem",
        "Arquitetura e Urbanismo",
    ]
    return random.choice(cursos)


def gerar_horas_assistidas() -> int:
    return random.randint(0, 120)


def gerar_nota_geral() -> float:
    return round(random.uniform(0.0, 10.0), 2)


def gerar_base_estudantes(quantidade: int = 100) -> pd.DataFrame:
    dados = {
        "Nome": [gerar_nome() for _ in range(quantidade)],
        "Matricula": [gerar_matricula() for _ in range(quantidade)],
        "Curso": [gerar_curso() for _ in range(quantidade)],
        "Quantidade de horas assistidas": [
            gerar_horas_assistidas() for _ in range(quantidade)
        ],
        "Nota geral": [gerar_nota_geral() for _ in range(quantidade)],
    }
    return pd.DataFrame(dados)


def main() -> None:
    quantidade_estudantes = 380
    arquivo_saida = "base_estudantes.xlsx"

    df = gerar_base_estudantes(quantidade=quantidade_estudantes)
    df.to_excel(arquivo_saida, index=False)

    print(f"Base com {len(df)} estudantes gerada com sucesso!")
    print(f"Arquivo exportado para: {arquivo_saida}")
    print("\nAmostra dos dados gerados:")
    print(df.head(10).to_string(index=False))


if __name__ == "__main__":
    main()