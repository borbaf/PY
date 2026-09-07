"""
Setup do BigQuery: cria/recria as tabelas da torre de controle logística.
Idempotente: apaga e recria as tabelas a cada execução.
"""
import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv()

PROJECT = os.getenv("GCP_PROJECT_ID", "coherent-voice-420518")
DATASET = os.getenv("BQ_DATASET", "logistics")
TABLE = os.getenv("BQ_TABLE_CONTROL_TOWER", "control_tower_shipments")
ADDRESS_TABLE = os.getenv("BQ_TABLE_ADDRESS_BOOK", "address_book")

client = bigquery.Client(project=PROJECT)

# --- Dataset ---
dataset_ref = f"{PROJECT}.{DATASET}"
client.create_dataset(dataset_ref, exists_ok=True)
print(f"Dataset {DATASET} OK")

# --- Tabela de entregas (control_tower_shipments) ---
print("Removendo tabela antiga (idempotente)...")
client.delete_table(f"{dataset_ref}.{TABLE}", not_found_ok=True)

schema = [
    bigquery.SchemaField("shipment_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("client_name", "STRING"),
    bigquery.SchemaField("origin_address", "STRING"),
    bigquery.SchemaField("destination_address", "STRING"),
    bigquery.SchemaField("origin_lat", "FLOAT64"),
    bigquery.SchemaField("origin_lng", "FLOAT64"),
    bigquery.SchemaField("destination_lat", "FLOAT64"),
    bigquery.SchemaField("destination_lng", "FLOAT64"),
    bigquery.SchemaField("scheduled_delivery", "TIMESTAMP"),
    bigquery.SchemaField("actual_delivery", "TIMESTAMP"),
    bigquery.SchemaField("status", "STRING"),  # 'ON_TIME' | 'LATE'
    bigquery.SchemaField("carrier", "STRING"),
    # --- NOVO: dados reais de rota (preenchidos pelo enrich_routes.py) ---
    bigquery.SchemaField("distance_km", "FLOAT64"),
    bigquery.SchemaField("duration_min", "FLOAT64"),
]
table = bigquery.Table(f"{dataset_ref}.{TABLE}", schema=schema)
client.create_table(table)
print(f"Tabela {TABLE} recriada OK")

# Seed: 6 entregas (3 da FarmaPlus), datas de hoje
today = datetime.now(timezone.utc).date()
rows = [
    {
        "shipment_id": "SHIP-001",
        "client_name": "FarmaPlus",
        "origin_address": "CD Guarulhos, SP",
        "destination_address": "Av. Paulista, 1000, São Paulo, SP",
        "origin_lat": -23.4655, "origin_lng": -46.5324,
        "destination_lat": -23.5614, "destination_lng": -46.6559,
        "scheduled_delivery": f"{today}T09:00:00",
        "actual_delivery": f"{today}T09:12:00",
        "status": "ON_TIME",
        "carrier": "TransRapida",
    },
    {
        "shipment_id": "SHIP-002",
        "client_name": "MercadoVita",
        "origin_address": "CD Guarulhos, SP",
        "destination_address": "Rua Augusta, 500, São Paulo, SP",
        "origin_lat": -23.4655, "origin_lng": -46.5324,
        "destination_lat": -23.5545, "destination_lng": -46.6493,
        "scheduled_delivery": f"{today}T10:00:00",
        "actual_delivery": f"{today}T10:55:00",
        "status": "LATE",
        "carrier": "TransRapida",
    },
    {
        "shipment_id": "SHIP-003",
        "client_name": "FarmaPlus",
        "origin_address": "CD Guarulhos, SP",
        "destination_address": "Av. Paulista, 1000, São Paulo, SP",
        "origin_lat": -23.4655, "origin_lng": -46.5324,
        "destination_lat": -23.5614, "destination_lng": -46.6559,
        "scheduled_delivery": f"{today}T11:00:00",
        "actual_delivery": f"{today}T11:08:00",
        "status": "ON_TIME",
        "carrier": "LogiForte",
    },
    {
        "shipment_id": "SHIP-004",
        "client_name": "AtacadoDia",
        "origin_address": "CD Guarulhos, SP",
        "destination_address": "Rua da Consolação, 900, São Paulo, SP",
        "origin_lat": -23.4655, "origin_lng": -46.5324,
        "destination_lat": -23.5520, "destination_lng": -46.6590,
        "scheduled_delivery": f"{today}T13:00:00",
        "actual_delivery": f"{today}T13:45:00",
        "status": "LATE",
        "carrier": "LogiForte",
    },
    {
        "shipment_id": "SHIP-005",
        "client_name": "FarmaPlus",
        "origin_address": "CD Guarulhos, SP",
        "destination_address": "Av. Paulista, 1000, São Paulo, SP",
        "origin_lat": -23.4655, "origin_lng": -46.5324,
        "destination_lat": -23.5614, "destination_lng": -46.6559,
        "scheduled_delivery": f"{today}T14:00:00",
        "actual_delivery": f"{today}T14:50:00",
        "status": "LATE",
        "carrier": "TransRapida",
    },
    {
        "shipment_id": "SHIP-006",
        "client_name": "MercadoVita",
        "origin_address": "CD Guarulhos, SP",
        "destination_address": "Rua Augusta, 500, São Paulo, SP",
        "origin_lat": -23.4655, "origin_lng": -46.5324,
        "destination_lat": -23.5545, "destination_lng": -46.6493,
        "scheduled_delivery": f"{today}T15:00:00",
        "actual_delivery": f"{today}T15:05:00",
        "status": "ON_TIME",
        "carrier": "LogiForte",
    },
]
errors = client.insert_rows_json(f"{dataset_ref}.{TABLE}", rows)
if errors:
    raise RuntimeError(f"Erro ao inserir entregas: {errors}")
print("6 linhas inseridas OK (distance_km/duration_min aguardando enrich_routes.py)")

# --- Tabela de cadastro de endereços (address_book) ---
print("Removendo tabela antiga address_book (idempotente)...")
client.delete_table(f"{dataset_ref}.{ADDRESS_TABLE}", not_found_ok=True)

address_schema = [
    bigquery.SchemaField("address_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("address", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("lat", "FLOAT64"),
    bigquery.SchemaField("lng", "FLOAT64"),
    bigquery.SchemaField("address_type", "STRING", mode="REQUIRED"),  # 'ORIGEM' | 'DESTINO'
    bigquery.SchemaField("client_name", "STRING"),
    bigquery.SchemaField("created_at", "TIMESTAMP"),
]
address_table = bigquery.Table(f"{dataset_ref}.{ADDRESS_TABLE}", schema=address_schema)
client.create_table(address_table)
print(f"Tabela {ADDRESS_TABLE} recriada OK")

seed_addresses = [
    ("ADR-001", "CD Guarulhos, SP", None, None, "ORIGEM", None),
    ("ADR-002", "Av. Paulista, 1000, São Paulo, SP", None, None, "DESTINO", "FarmaPlus"),
    ("ADR-003", "Rua Augusta, 500, São Paulo, SP", None, None, "DESTINO", "MercadoVita"),
]
errors = client.insert_rows_json(
    f"{dataset_ref}.{ADDRESS_TABLE}",
    [
        {
            "address_id": a[0], "address": a[1], "lat": a[2], "lng": a[3],
            "address_type": a[4], "client_name": a[5],
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        for a in seed_addresses
    ],
)
if errors:
    raise RuntimeError(f"Erro ao inserir endereços seed: {errors}")
print("Endereços seed inseridos OK")
print("Setup concluído.")