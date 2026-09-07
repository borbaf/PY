#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from datetime import datetime

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    print("Biblioteca 'psycopg2' nao encontrada. Instale com: pip install psycopg2-binary")
    sys.exit(1)


# Configuracoes de conexao com o PostgreSQL
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "db_borbaf",
    "user": "postgres",
    "password": "P$inUca01",
}


def obter_conexao():
    """Cria e retorna uma conexao com o PostgreSQL."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        return conn
    except psycopg2.Error as e:
        print(f"Erro ao conectar no PostgreSQL: {e}")
        sys.exit(1)


def garantir_tabela(conn):
    """Garante que a tabela logistica_teste exista no banco."""
    sql = """
    CREATE TABLE IF NOT EXISTS logistica_teste (
        id SERIAL PRIMARY KEY,
        origem VARCHAR(100) NOT NULL,
        destino VARCHAR(100) NOT NULL,
        produto VARCHAR(150) NOT NULL,
        peso_kg NUMERIC(10,2) NOT NULL,
        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
    except psycopg2.Error as e:
        print(f"Erro ao criar/verificar tabela: {e}")


def inserir_carga(conn):
    """Solicita dados ao usuario e insere uma nova carga."""
    print("\n--- Inserir nova carga ---")
    origem = input("Origem: ").strip()
    if not origem:
        print("Origem nao pode ser vazia.")
        return

    destino = input("Destino: ").strip()
    if not destino:
        print("Destino nao pode ser vazio.")
        return

    produto = input("Produto: ").strip()
    if not produto:
        print("Produto nao pode ser vazio.")
        return

    try:
        peso_kg = float(input("Peso (kg): ").strip().replace(",", "."))
        if peso_kg <= 0:
            print("Peso deve ser maior que zero.")
            return
    except ValueError:
        print("Peso invalido. Use um numero (ex.: 12.5).")
        return

    sql = """
        INSERT INTO logistica_teste (origem, destino, produto, peso_kg, data_cadastro)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (origem, destino, produto, peso_kg, datetime.now()))
            carga_id = cur.fetchone()[0]
            print(f"\nCarga inserida com sucesso! ID: {carga_id}")
    except psycopg2.Error as e:
        print(f"Erro ao inserir carga: {e}")


def listar_cargas(conn):
    """Lista todas as cargas cadastradas na tabela logistica_teste."""
    print("\n--- Cargas cadastradas ---")
    sql = """
        SELECT id, origem, destino, produto, peso_kg, data_cadastro
        FROM logistica_teste
        ORDER BY id ASC;
    """
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(sql)
            registros = cur.fetchall()

            if not registros:
                print("Nenhuma carga cadastrada.")
                return

            print(f"{'ID':<5} {'Origem':<20} {'Destino':<20} {'Produto':<20} {'Peso(kg)':<10} {'Data Cadastro':<20}")
            print("-" * 100)
            for r in registros:
                data_fmt = r["data_cadastro"].strftime("%d/%m/%Y %H:%M:%S") if r["data_cadastro"] else "-"
                print(f"{r['id']:<5} {r['origem']:<20} {r['destino']:<20} {r['produto']:<20} {r['peso_kg']:<10.2f} {data_fmt:<20}")
            print(f"\nTotal de cargas: {len(registros)}")
    except psycopg2.Error as e:
        print(f"Erro ao listar cargas: {e}")


def exibir_menu():
    """Exibe o menu principal."""
    print("\n========== MENU LOGISTICA ==========")
    print("1 - Inserir nova carga")
    print("2 - Listar cargas")
    print("0 - Sair")
    print("====================================")


def main():
    print("Sistema de Logistica - Tabela logistica_teste")
    conn = obter_conexao()
    garantir_tabela(conn)

    try:
        while True:
            exibir_menu()
            opcao = input("Escolha uma opcao: ").strip()

            if opcao == "1":
                inserir_carga(conn)
            elif opcao == "2":
                listar_cargas(conn)
            elif opcao == "0":
                print("Encerrando o programa. Ate logo!")
                break
            else:
                print("Opcao invalida. Tente novamente.")
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuario. Saindo...")
    finally:
        conn.close()
        print("Conexao encerrada.")


if __name__ == "__main__":
    main()