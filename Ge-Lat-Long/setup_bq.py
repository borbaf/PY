from google.cloud import bigquery

PROJECT = "coherent-voice-420518"
client = bigquery.Client(project=PROJECT)
TABLE = f"{PROJECT}.logistics.control_tower_shipments"

client.delete_table(TABLE, not_found_ok=True)
print("Tabela antiga removida (idempotente)")

client.create_dataset("logistics", exists_ok=True)
print("Dataset logistics OK")

schema = [
    bigquery.SchemaField("shipment_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("client_name", "STRING", mode="REQUIRED"),
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
client.create_table(bigquery.Table(table_ref, schema=schema))
print("Tabela control_tower_shipments recriada OK")

COLS = ["shipment_id", "client_name", "origin_address", "destination_address",
        "scheduled_delivery", "actual_delivery", "status", "carrier"]
rows = [
    ("SHIP-001", "FarmaPlus",   "Av. Paulista, 1000 - São Paulo/SP",      "Rua da Consolação, 2000 - São Paulo/SP",  "2026-09-04 10:00:00", "2026-09-04 09:40:00", "ON_TIME", "TRANSP-X"),
    ("SHIP-002", "MercadoVita", "Av. Brasil, 500 - Campinas/SP",          "Av. Paulista, 1000 - São Paulo/SP",      "2026-09-04 14:00:00", "2026-09-04 15:30:00", "LATE",    "TRANSP-Y"),
    ("SHIP-003", "FarmaPlus",   "Rua XV de Novembro, 800 - São Paulo/SP", "Av. Paulista, 1000 - São Paulo/SP",      "2026-09-04 09:00:00", "2026-09-04 08:55:00", "ON_TIME", "TRANSP-X"),
    ("SHIP-004", "AtacadoDia",  "Av. Getúlio Vargas, 1500 - BH/MG",       "Av. Paulista, 1000 - São Paulo/SP",      "2026-09-04 18:00:00", "2026-09-04 19:20:00", "LATE",    "TRANSP-Z"),
    ("SHIP-005", "FarmaPlus",   "Av. Paulista, 1000 - São Paulo/SP",      "Av. Atlântica, 2000 - Rio de Janeiro/RJ","2026-09-04 08:00:00", "2026-09-04 07:50:00", "ON_TIME", "TRANSP-W"),
    ("SHIP-006", "MercadoVita", "Rua Augusta, 500 - São Paulo/SP",        "Av. Paulista, 1000 - São Paulo/SP",      "2026-09-04 15:00:00", "2026-09-04 16:10:00", "LATE",    "TRANSP-Y"),
]
errors = client.insert_rows_json(
    table_ref,
    [dict(zip(COLS, r)) for r in rows],
)
if errors:
    print("Erros ao inserir:", errors)
else:
    print("6 linhas inseridas OK")