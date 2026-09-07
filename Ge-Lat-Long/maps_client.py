"""
Wrapper das APIs do Google Maps Platform (Geocoding, Routes, Places).
Centraliza chamadas REST e normaliza as respostas para o agente.
"""
import os
from typing import Optional

import requests
from dotenv import load_dotenv

load_dotenv()

MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
BASE = "https://maps.googleapis.com/maps/api"

class MapsError(Exception):
    """Erro de configuração ou chamada do Google Maps Platform."""

class MapsClient:
    """Camada de acesso ao Google Maps Platform."""

    def __init__(self, api_key: str = MAPS_API_KEY):
        if not api_key:
            raise MapsError(
                "GOOGLE_MAPS_API_KEY não configurada no .env. "
                "Gere em Cloud Console -> Credentials."
            )
        self.api_key = api_key

    # ---------- Geocoding ----------
    def geocode(self, address: str) -> Optional[dict]:
        """Converte endereço em coordenadas (lat/lng)."""
        resp = requests.get(
            f"{BASE}/geocode/json",
            params={"address": address, "key": self.api_key},
            timeout=10,
        )
        data = resp.json()
        if data.get("status") != "OK" or not data.get("results"):
            self._raise_status(data.get("status"))
        loc = data["results"][0]["geometry"]["location"]
        return {"address": address, "lat": loc["lat"], "lng": loc["lng"]}

    # ---------- Routes (distância / tempo / trânsito) ----------
    def route(self, origin: str, destination: str, traffic: bool = True) -> Optional[dict]:
        """
        Usa a Routes API (v2) para calcular distância e duração.
        Retorna métricas reais, com ou sem trânsito.
        """
        url = "https://routes.googleapis.com/directions/v2:computeRoutes"
        payload = {
            "origin": {"address": origin},
            "destination": {"address": destination},
            "travelMode": "DRIVE",
            "routingPreference": "TRAFFIC_AWARE" if traffic else "TRAFFIC_UNAWARE",
            "units": "METRIC",
        }
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.api_key,
            "X-Goog-FieldMask": (
                "routes.duration,routes.distanceMeters,"
                "routes.polyline.encodedPolyline"
            ),
        }
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        if resp.status_code != 200:
            self._raise_status(f"HTTP {resp.status_code}: {resp.text[:200]}")
        data = resp.json()
        if not data.get("routes"):
            return None
        r = data["routes"][0]
        return {
            "origin": origin,
            "destination": destination,
            "distance_km": round(int(r.get("distanceMeters", 0)) / 1000, 2),
            "duration_min": round(int(r.get("duration", "0s").rstrip("s")) / 60, 1),
            "traffic_aware": traffic,
        }

    # ---------- Places (contexto do local) ----------
    def place_context(self, query: str, lat: float, lng: float) -> Optional[dict]:
        """Busca contexto de um lugar (ex.: posto, cliente, CD) próximo."""
        resp = requests.get(
            f"{BASE}/place/textsearch/json",
            params={
                "query": query,
                "location": f"{lat},{lng}",
                "radius": 5000,
                "key": self.api_key,
            },
            timeout=10,
        )
        data = resp.json()
        if data.get("status") != "OK" or not data.get("results"):
            self._raise_status(data.get("status"))
        p = data["results"][0]
        return {
            "name": p.get("name"),
            "address": p.get("formatted_address"),
            "rating": p.get("rating"),
            "open_now": p.get("opening_hours", {}).get("open_now"),
        }

    @staticmethod
    def _raise_status(status: str):
        """Traduz códigos de erro comuns do Maps em mensagens acionáveis."""
        if status == "REQUEST_DENIED":
            raise MapsError(
                "REQUEST_DENIED: chave inválida OU API não habilitada. "
                "Confira a chave e se Geocoding/Routes/Places estão Enabled."
            )
        if status == "OVER_QUERY_LIMIT":
            raise MapsError("OVER_QUERY_LIMIT: cota mensal gratuita atingida.")
        if status == "ZERO_RESULTS":
            raise MapsError("ZERO_RESULTS: endereço/local não encontrado.")
        raise MapsError(f"Erro do Maps: {status}")