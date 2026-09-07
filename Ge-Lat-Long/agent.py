"""
Agente de IA com contexto geográfico.

Combina dados proprietários (BigQuery) com dados reais do Google Maps
através de function calling do Gemini. O modelo decide, em linguagem
natural, quando consultar rotas, geocodificação ou a torre de controle.
"""
import os
from typing import Callable

from dotenv import load_dotenv
from google import genai
from google.genai import types

from bigquery_client import BigQueryClient
from maps_client import MapsClient

load_dotenv()

TOOLS = [
    types.Tool(
        function_declarations=[
            {
                "name": "route_metrics",
                "description": (
                    "Calcula distância e tempo de viagem entre dois "
                    "endereços usando o Google Maps, com trânsito atual."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "origin": {"type": "string"},
                        "destination": {"type": "string"},
                    },
                    "required": ["origin", "destination"],
                },
            },
            {
                "name": "geocode_address",
                "description": "Converte um endereço em coordenadas.",
                "parameters": {
                    "type": "object",
                    "properties": {"address": {"type": "string"}},
                    "required": ["address"],
                },
            },
            {
                "name": "shipments_by_client",
                "description": (
                    "Lista entregas de um cliente na torre de controle. Consulta somente-leitura "
                    "na tabela logistics.control_tower_shipments. Colunas disponíveis: "
                    "shipment_id STRING, client_name STRING (ex.: FarmaPlus), origin_address STRING, "
                    "destination_address STRING, origin_lat FLOAT64, origin_lng FLOAT64, "
                    "destination_lat FLOAT64, destination_lng FLOAT64, scheduled_delivery TIMESTAMP, "
                    "actual_delivery TIMESTAMP, status STRING ('ON_TIME' | 'LATE'), carrier STRING. "
                    "Use APENAS estas colunas. NÃO invente nomes fora desta lista."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {"client_name": {"type": "string"}},
                    "required": ["client_name"],
                },
            },
            {
                "name": "control_tower_kpis",
                "description": "Retorna KPIs agregados de desempenho das entregas.",
                "parameters": {"type": "object", "properties": {}},
            },
        ]
    )
]

SYSTEM_INSTRUCTION = (
    "Você é um agente de operações logísticas que responde com dados reais "
    "do Google Maps (rotas) e do BigQuery (torre de controle). "
    "REGRAS OBRIGATÓRIAS: "
    "1) Sempre que a pergunta exigir dados, chame as ferramentas — nunca invente números. "
    "2) Quando a tarefa envolver calcular rota para VÁRIAS entregas, chame route_metrics "
    "UMA vez para CADA entrega, em iterações sucessivas, até ter o tempo de viagem de todas. "
    "3) Só produza a resposta final em texto DEPOIS de executar todas as chamadas necessárias. "
    "4) Quando o usuário pedir todas as entregas, calcule TODAS — não pergunte qual ele quer."
)

class LogisticsAgent:
    """Agente orquestrador: Gemini + Maps + BigQuery."""

    def __init__(self, model: str = "gemini-2.5-flash"):
        self.maps = MapsClient()
        self.bq = BigQueryClient()
        self.client = genai.Client(
            vertexai=True,
            project="coherent-voice-420518",
            location="us-central1",
        )
        self.model = model

        self.handlers: dict[str, Callable] = {
            "route_metrics": self.maps.route,
            "geocode_address": self.maps.geocode,
            "shipments_by_client": self.bq.get_shipments_by_client,
            "control_tower_kpis": self.bq.get_control_tower_kpis,
        }

    def _run_function(self, call) -> str:
        """Executa a função solicitada pelo modelo e serializa o resultado."""
        name = call.name
        args = call.args or {}
        handler = self.handlers.get(name)
        if not handler:
            return f"Função desconhecida: {name}"
        try:
            result = handler(**args)
        except Exception as exc:  # noqa: BLE001 - repassa erro ao modelo
            return f"Erro ao executar {name}: {exc}"
        return str(result)

    def ask(self, user_prompt: str, max_iterations: int = 12) -> str:
        """Envia a pergunta ao Gemini e resolve as chamadas de função."""
        messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

        for _ in range(max_iterations):
            response = self.client.models.generate_content(
                model=self.model,
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=TOOLS,
                    system_instruction=SYSTEM_INSTRUCTION,
                ),
            )
            if not response.function_calls:
                return response.text

            # Turno do modelo: todas as chamadas de função em UMA mensagem
            messages.append(
                types.Content(
                    role="model",
                    parts=[types.Part(function_call=call) for call in response.function_calls],
                )
            )

            # Turno da ferramenta: TODAS as respostas agrupadas em UMA mensagem,
            # uma parte function_response por chamada (exigência da API)
            messages.append(
                types.Content(
                    role="tool",
                    parts=[
                        types.Part(
                            function_response={
                                "name": call.name,
                                "response": {"result": self._run_function(call)},
                            }
                        )
                        for call in response.function_calls
                    ],
                )
            )
        return "Número máximo de iterações atingido."