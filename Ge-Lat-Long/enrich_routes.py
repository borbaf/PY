"""
Enriquece a torre de controle com dados REAIS de rota do Google Maps.

Entregável-chave da solução: tempo de viagem estimado COM CONTEXTO DE
TRÂNSITO (departure_time='now'). Para cada entrega cadastrada, consulta a
Distance Matrix API, grava distance_km e duration_min na tabela
control_tower_shipments e recria a VIEW do Looker Studio com os campos
enriquecidos.

Uso:
    python enrich_routes.py
"""
import os
import time
from typing import Dict, List

import googlemaps
from dotenv import load_dotenv

from bigquery_client import BigQueryClient

load_dotenv()

PROJECT = os.getenv("GCP_PROJECT_ID", "coherent-voice-420518")
DATASET = os.getenv("BQ_DATASET", "logistics")
TABLE = os.getenv("BQ_TABLE_CONTROL_TOWER", "control_tower_shipments")
VIEW_NAME = "vw_control_tower_dashboard"
MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")

class EnrichmentError(Exception):
    """Erro no enriquecimento de rotas."""

def _place(row: Dict, kind: str) -> str:
    """Retorna 'lat,lng' quando disponível, senão o endereço textual."""
    lat, lng = row.get(f"{kind}_lat"), row.get(f"{kind}_lng")
    if lat is not None and lng is not None:
        return f"{lat},{lng}"
    addr = row.get(f"{kind}_address")
    if not addr:
        raise EnrichmentError(f"Entrega {row.get('shipment_id')} sem {kind} válido")
    return addr

def _fetch_route(gmaps: googlemaps.Client, origin: str, destination: str) -> Dict:
    """Chama a Distance Matrix com trânsito atual e extrai km/min."""
    matrix = gmaps.distance_matrix(
        origins=[origin],
        destinations=[destination],
        mode="driving",
        units="metric",
        departure_time="now",  # <-- contexto de trânsito atual
    )
    element = matrix["rows"][0]["elements"][0]
    if element["status"] != "OK":
        raise EnrichmentError(
            f"Maps retornou {element['status']} para {origin} -> {destination}"
        )
    distance_km = element["distance"]["value"] / 1000.0
    # Preferência explícita ao tempo COM trânsito (entregável-chave)
    seconds = element.get(
        "duration_in_traffic", element.get("duration", {})
    ).get("value")
    duration_min = seconds / 60.0 if seconds else 0.0
    has_traffic = "duration_in_traffic" in element
    return {
        "distance_km": distance_km,
        "duration_min": duration_min,
        "has_traffic": has_traffic,
    }

def _view_sql() -> str:
    """VIEW modelada para o Looker Studio, com os campos de rota real."""
    return f"""
    CREATE OR REPLACE VIEW `{PROJECT}.{DATASET}.{VIEW_NAME}` AS
    SELECT
      shipment_id,
      client_name,
      origin_address,
      destination_address,
      origin_lat,
      origin_lng,
      destination_lat,
      destination_lng,
      scheduled_delivery,
      actual_delivery,
      status,
      carrier,
      distance_km,
      duration_min,
      DATE(scheduled_delivery)                              AS delivery_date,
      CAST(scheduled_delivery AS TIME)                      AS scheduled_time,
      TIMESTAMP_DIFF(actual_delivery, scheduled_delivery, MINUTE) AS delay_minutes,
      CASE WHEN status = 'ON_TIME' THEN 1 ELSE 0 END        AS is_on_time,
      CASE WHEN status = 'LATE'   THEN 1 ELSE 0 END         AS is_late
    FROM `{PROJECT}.{DATASET}.{TABLE}`
    """

def enrich_routes() -> None:
    if not MAPS_API_KEY:
        raise EnrichmentError(
            "GOOGLE_MAPS_API_KEY não configurada no .env. "
            "Adicione a chave para calcular rotas com trânsito."
        )

    gmaps = googlemaps.Client(key=MAPS_API_KEY)
    bq = BigQueryClient()
    shipments: List[Dict] = bq.get_shipments_for_routes()

    if not shipments:
        print("Nenhuma entrega para enriquecer. Rode setup_bq.py primeiro.")
        return

    print(f"Enriquecendo {len(shipments)} rotas com trânsito atual (Maps API)...\n")
    total_api_ms = 0.0
    results = []
    for row in shipments:
        shipment_id = row["shipment_id"]
        origin = _place(row, "origin")
        destination = _place(row, "destination")

        t0 = time.perf_counter()
        try:
            route = _fetch_route(gmaps, origin, destination)
            elapsed_ms = (time.perf_counter() - t0) * 1000
            total_api_ms += elapsed_ms
            msg = bq.update_shipment_route_metrics(
                shipment_id, route["distance_km"], route["duration_min"]
            )
            flag = "trânsito" if route["has_traffic"] else "sem trânsito (fallback)"
            results.append((shipment_id, elapsed_ms))
            print(f"  [OK] {msg} | {flag} | API {elapsed_ms:.0f} ms")
        except Exception as exc:
            print(f"  [ERRO] {shipment_id}: {exc}")

    # Recria a VIEW para o Looker incluir os campos enriquecidos
    bq.client.query(_view_sql()).result()
    print("\nVIEW vw_control_tower_dashboard recriada com distance_km e duration_min.")

    if results:
        avg_ms = total_api_ms / len(results)
        print(
            f"\nResumo: {len(results)}/{len(shipments)} rotas OK | "
            f"tempo médio por consulta Maps: {avg_ms:.0f} ms"
        )

if __name__ == "__main__":
    enrich_routes()