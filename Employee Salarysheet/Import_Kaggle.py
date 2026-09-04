import os
import kagglehub
import sqlite3
import pandas as pd
import sqlite3



from kagglehub import KaggleDatasetAdapter



# O file_path é o nome exato do arquivo dentro do dataset
file_path = "MPI_software employee sallarysheet.csv"

df = kagglehub.load_dataset(
    KaggleDatasetAdapter.PANDAS,
    "mdnurhossen/mpi-software-employee-sallarysheet",
    file_path,
)

#print("Shape:", df.shape)
#print("Columns:", df.columns.tolist())
#print(df.head(10))
#print("\nDtypes:\n", df.dtypes)
#print("\nJob titles únicos:", df["job_title"].nunique())
#print(df["job_title"].value_counts().head(10))


# Criar banco em memória
conn = sqlite3.connect(":memory:")

# Carregar o DataFrame do Kaggle diretamente para uma tabela SQLite
df.to_sql("Employee", conn, index=False, if_exists="replace")

# Renomear a coluna "sallary" para "salary" para ficar consistente com as queries
conn.execute("ALTER TABLE Employee RENAME COLUMN sallary TO salary;")





# ──────────────────────────────────────────────
# Q1: Segundo maior salário (usando DENSE_RANK para lidar com empates)
# ──────────────────────────────────────────────



# cria uma CTE (Common Table Expression), que é como uma tabela temporária que só existe durante esta query.
# # para cada linha, atribui um rank baseado no salário em ordem decrescente. A diferença crucial do DENSE_RANK é que ele não pula números em caso de empate. Por exemplo, se dois funcionários têm o maior salário, ambos receberão rank 1, e o próximo salário mais alto receberá rank 2.

q1 = """
WITH ranked AS ( 
    SELECT salary,    
           DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk   
    FROM Employee
)
SELECT DISTINCT salary AS second_highest_salary 
FROM ranked
WHERE rnk = 2; 
"""
#DISTINCT garante que o resultado é um valor único.
#filtra apenas as linhas com rank 2.

print("Q1 — Segundo maior salário:")
print(pd.read_sql(q1, conn))


#--->>> Se todos os funcionários ganham o mesmo salário, a query retorna vazio (nenhuma linha), não NULL
# q1_1 = """
# SELECT max(salary) AS second_highest_salary_
# FROM employee
# WHERE salary < (SELECT max(salary) FROM employee);
# """
# print("Q1.1 — Segundo maior salário:***")
# print(pd.read_sql(q1_1, conn))



# q1_2 = """
# SELECT DISTINCT salary AS second_highest_salary__
# FROM Employee
# ORDER BY salary DESC
# LIMIT 1 OFFSET 1;
# """
# print("Q1.2 — Segundo maior salário:****")
# print(pd.read_sql(q1_2, conn))



#print(df.info())

# ──────────────────────────────────────────────
# Q2: Comparar RANK, DENSE_RANK e ROW_NUMBER
# ──────────────────────────────────────────────
q2 = """
SELECT
    employe_id,
    job_title,
    salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num,
    RANK()       OVER (ORDER BY salary DESC) AS rnk,
    DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rnk
FROM Employee
ORDER BY salary DESC
LIMIT 15;
"""
print("\nQ2 — RANK vs DENSE_RANK vs ROW_NUMBER:")
print(pd.read_sql(q2, conn))

# ──────────────────────────────────────────────
# Q3: Running total de salários agrupado por cargo
# ──────────────────────────────────────────────
q3 = """
SELECT
    job_title,
    employe_id,
    salary,
    SUM(salary) OVER (
        PARTITION BY job_title
        ORDER BY employe_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total
FROM Employee
ORDER BY job_title, employe_id
LIMIT 20;
"""
print("\nQ3 — Running total por cargo:")
print(pd.read_sql(q3, conn))

# ──────────────────────────────────────────────
# Q4: Remover duplicatas sem DISTINCT (usando ROW_NUMBER)
# ──────────────────────────────────────────────
# q4 = """
# WITH cte AS (
#     SELECT
#         *,
#         ROW_NUMBER() OVER (
#             PARTITION BY job_title, salary
#             ORDER BY employe_id
#         ) AS rn
#     FROM Employee
# )
# SELECT employe_id, job_title, salary
# FROM cte
# WHERE rn = 1
# ORDER BY job_title, salary;
# """
# print("\nQ4 — Sem duplicatas (job_title + salary):")
# print(pd.read_sql(q4, conn))
# print(f"Original: {len(df)} linhas | Sem dup: {len(pd.read_sql(q4, conn))} linhas")

# ──────────────────────────────────────────────
# Q5: Funcionários ganhando acima da média de seu cargo
# ──────────────────────────────────────────────
# q5 = """
# WITH with_avg AS (
#     SELECT
#         employe_id,
#         job_title,
#         salary,
#         AVG(salary) OVER (PARTITION BY job_title) AS title_avg
#     FROM Employee
# )
# SELECT
#     employe_id,
#     job_title,
#     salary,
#     ROUND(title_avg, 2) AS title_average,
#     ROUND(salary - title_avg, 2) AS above_average_by
# FROM with_avg
# WHERE salary > title_avg
# ORDER BY job_title, salary DESC
# LIMIT 20;
# """
# print("\nQ5 — Acima da média do cargo:")
# print(pd.read_sql(q5, conn))

# conn.close()
