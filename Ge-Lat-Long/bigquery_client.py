"""
Acesso aos dados proprietários de logística no BigQuery.
Simula a 'torre de controle': entregas, clientes e CDs da empresa.
"""
import os
from typing import Dict, List

from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv()

PROJECT = os.getenv("GCP_PROJECT_ID", "coherent-voice-420518")
DATASET = os.getenv("BQ_DATASET", "logistics")
TABLE = os.getenv("BQ_TABLE_CONTROL_TOWER", "control_tower_shipments")

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