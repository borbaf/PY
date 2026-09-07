from google.cloud import bigquery

client = bigquery.Client(project="coherent-voice-420518")

# 1. Dataset
client.create_dataset("logistics", exists_ok=True)
print("Dataset logistics OK")

# 2. Tabela
schema = [
    bigquery.SchemaField("shipment_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("origin_address", "STRING"),
    bigquery.SchemaField("destination_address", "STRING"),
    bigquery.SchemaField("origin_lat", "FLOAT64"),
    bigquery.SchemaField("origin_lng", "FLOAT64"),
    bigquery.SchemaField("destination_lat", "FLOAT64"),
    bigquery.SchemaField("destination_lng", "FLOAT64"),
    bigquery.SchemaField("scheduled_delivery", "TIMESTAMP"),
    bigquery.SchemaField("actual_delivery", "TIMESTAMP"),
    bigquery.SchemaField("status", "STRING"),
    bigquery.SchemaField("carrier", "STRING"),
]
table_ref = client.dataset("logistics").table("control_tower_shipments")
client.create_table(bigquery.Table(table_ref, schema=schema), exists_ok=True)
print("Tabela control_tower_shipments OK")

# 3. Dados de exemplo (3 no prazo, 2 atrasadas)
rows = [
    ("SHIP-001", "Av. Paulista, 1000 - São Paulo/SP", "Rua da Consolação, 2000 - São Paulo/SP",
     "2026-09-02 10:00:00", "2026-09-02 09:40:00", "DELIVERED_ON_TIME", "TRANSP-X"),
    ("SHIP-002", "Av. Brasil, 500 - Campinas/SP", "Av. Paulista, 1000 - São Paulo/SP",
     "2026-09-02 14:00:00", "2026-09-02 15:30:00", "DELIVERED_LATE", "TRANSP-Y"),
    ("SHIP-003", "Rua XV de Novembro, 800 - São Paulo/SP", "Av. Paulista, 1000 - São Paulo/SP",
     "2026-09-03 09:00:00", "2026-09-03 08:55:00", "DELIVERED_ON_TIME", "TRANSP-X"),
    ("SHIP-004", "Av. Getúlio Vargas, 1500 - Belo Horizonte/MG", "Av. Paulista, 1000 - São Paulo/SP",
     "2026-09-03 18:00:00", "2026-09-03 19:20:00", "DELIVERED_LATE", "TRANSP-Z"),
    ("SHIP-005", "Av. Paulista, 1000 - São Paulo/SP", "Av. Atlântica, 2000 - Rio de Janeiro/RJ",
     "2026-09-04 08:00:00", "2026-09-04 07:50:00", "DELIVERED_ON_TIME", "TRANSP-W"),
]
errors = client.insert_rows_json(
    table_ref,
    [dict(zip(["shipment_id", "origin_address", "destination_address",
                "scheduled_delivery", "actual_delivery", "status", "carrier"], r)) for r in rows],
)
if errors:
    print("Erros ao inserir:", errors)
else:
    print("5 linhas inseridas OK")