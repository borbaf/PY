"""
Acesso aos dados proprietários de logística no BigQuery.
Simula a 'torre de controle': entregas, clientes, CDs e cadastro de endereços.
"""
import os
import uuid
from datetime import datetime, timezone
from typing import Dict, List

from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv()

PROJECT = os.getenv("GCP_PROJECT_ID", "coherent-voice-420518")
DATASET = os.getenv("BQ_DATASET", "logistics")
TABLE = os.getenv("BQ_TABLE_CONTROL_TOWER", "control_tower_shipments")
ADDRESS_TABLE = os.getenv("BQ_TABLE_ADDRESS_BOOK", "address_book")

class BigQueryError(Exception):
    """Erro de acesso ao BigQuery."""

class BigQueryClient:
    """Camada de acesso aos dados proprietários."""

    def __init__(self, project: str = PROJECT):
        if not project:
            raise BigQueryError(
                "GCP_PROJECT_ID não configurado no .env. "
                "Use o ID do projeto (coherent-voice-420518)."
            )
        self.client = bigquery.Client(project=project)

    def get_shipments_by_client(self, client_name: str, limit: int = 20) -> List[Dict]:
        """Retorna entregas recentes de um cliente, com origem, destino e status."""
        query = f"""
        SELECT
            shipment_id,
            client_name,
            origin_address,
            destination_address,
            status,
            scheduled_delivery
        FROM `{PROJECT}.{DATASET}.{TABLE}`
        WHERE LOWER(client_name) LIKE LOWER(@client)
        ORDER BY scheduled_delivery DESC
        LIMIT @limit
        """
        job = self.client.query(
            query,
            job_config=bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("client", "STRING", f"%{client_name}%"),
                    bigquery.ScalarQueryParameter("limit", "INT64", limit),
                ]
            ),
        )
        return [dict(row) for row in job.result()]

    def get_control_tower_kpis(self) -> Dict:
        """KPIs agregados da torre de controle (entregas, atrasos)."""
        query = f"""
        SELECT
            COUNT(*)                              AS total_shipments,
            COUNTIF(status = 'LATE')             AS delayed_shipments,
            COUNTIF(status = 'ON_TIME')          AS on_time_shipments,
            ROUND(SAFE_DIVIDE(
                COUNTIF(status = 'ON_TIME'), COUNT(*)) * 100, 1) AS on_time_pct
        FROM `{PROJECT}.{DATASET}.{TABLE}`
        """
        job = self.client.query(query)
        row = next(job.result())
        return dict(row)

    def get_shipments_for_routes(self) -> List[Dict]:
        """Retorna todas as entregas com origem/destino para calcular rotas reais."""
        query = f"""
        SELECT
            shipment_id,
            client_name,
            origin_address,
            destination_address,
            origin_lat,
            origin_lng,
            destination_lat,
            destination_lng,
            status
        FROM `{PROJECT}.{DATASET}.{TABLE}`
        ORDER BY shipment_id
        """
        job = self.client.query(query)
        return [dict(row) for row in job.result()]

    def update_shipment_route_metrics(
        self, shipment_id: str, distance_km: float, duration_min: float
    ) -> str:
        """Grava a rota real (Google Maps) na entrega: distance_km e duration_min."""
        query = f"""
        UPDATE `{PROJECT}.{DATASET}.{TABLE}`
        SET distance_km = @dist,
            duration_min = @dur
        WHERE shipment_id = @id
        """
        job = self.client.query(
            query,
            job_config=bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("dist", "FLOAT64", distance_km),
                    bigquery.ScalarQueryParameter("dur", "FLOAT64", duration_min),
                    bigquery.ScalarQueryParameter("id", "STRING", shipment_id),
                ]
            ),
        )
        job.result()
        return (
            f"{shipment_id}: {distance_km:.2f} km | "
            f"{duration_min:.1f} min (com trânsito)"
        )

    def insert_address(
        self,
        address: str,
        lat: float,
        lng: float,
        address_type: str,
        client_name: str = "",
    ) -> str:
        """Insere um novo endereço na tabela de cadastro (address_book)."""
        rows = [
            {
                "address_id": f"ADR-{uuid.uuid4().hex[:6].upper()}",
                "address": address,
                "lat": lat,
                "lng": lng,
                "address_type": address_type,
                "client_name": client_name or None,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        ]
        errors = self.client.insert_rows_json(
            f"{PROJECT}.{DATASET}.{ADDRESS_TABLE}", rows
        )
        if errors:
            return f"Erro ao inserir endereço: {errors}"
        return (
            f"Endereço cadastrado com sucesso: {rows[0]['address_id']} | "
            f"{address} | tipo={address_type} | lat={lat}, lng={lng}"
        )