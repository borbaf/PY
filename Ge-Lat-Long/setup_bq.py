import os
import random
import datetime
from datetime import timedelta
from google.cloud import bigquery

# ============================================================
# CONFIGURAÇÃO
# ============================================================
PROJECT_ID = "coherent-voice-420518"
DATASET = "logistics"
TABLE = "vw_control_tower_dashboard"

# Caminho da chave de serviço (ajuste se necessário)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "caminho/para/sua-chave.json"

client = bigquery.Client(project=PROJECT_ID)

# ============================================================
# DADOS DAS ENTREGAS (mesmas rotas de sempre)
# ============================================================
# (origem, destino, lat_dest, lng_dest, transportadora)
rotas = [
    ("CD Centro - São Paulo, SP", "Av. Paulista, 1000 - São Paulo, SP", -23.5614, -46.6559, "TransRapida"),
    ("CD Centro - São Paulo, SP", "Rua Augusta, 2500 - São Paulo, SP", -23.5561, -46.6641, "TransRapida"),
    ("CD Sul - Santo André, SP",     "Av. do Estado, 500 - São Paulo, SP", -23.5410, -46.6120, "LogiForte"),
    ("CD Sul - Santo André, SP",     "Rua Vergueiro, 3000 - São Paulo, SP", -23.5880, -46.6330, "LogiForte"),
    ("CD Leste - Guarulhos, SP",     "Av. Tiradentes, 700 - São Paulo, SP", -23.5250, -46.6330, "TransRapida"),
    ("CD Leste - Guarulhos, SP",     "Rua 25 de Março, 800 - São Paulo, SP", -23.5410, -46.6340, "LogiForte"),
]

# ============================================================
# GERA AS ENTREGAS DISTRIBUÍDAS NOS ÚLTIMOS 7 DIAS
# ============================================================
hoje = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

registros = []
for i, (origem, destino, lat, lng, transportadora) in enumerate(rotas):
    # Cada entrega cai num dia diferente dos últimos 7 dias
    dias_atras = i % 7                      # 0,1,2,3,4,5,6
    data_base = hoje - timedelta(days=dias_atras)

    # Horário de agendamento: manhã (08h) ou tarde (14h), alternando
    hora = 8 if i % 2 == 0 else 14
    scheduled = data_base.replace(hour=hora, minute=random.randint(0, 59))

    # Entrega: +2 a +4 horas depois do agendamento
    delivery = scheduled + timedelta(hours=random.randint(2, 4))

    # Status: ~50% on-time, ~50% late (para bater com os scorecards)
    on_time = random.random() > 0.5
    status = "ON_TIME" if on_time else "LATE"
    is_on_time = 1 if on_time else 0
    is_late = 0 if on_time else 1

    # Distância e duração (valores realistas)
    distance_km = round(random.uniform(8, 35), 1)
    duration_min = round(distance_km * random.uniform(1.5, 2.5), 0)

    registros.append({
        "shipment_id": f"SHP-{1000 + i}",
        "origin_address": origem,
        "destination_address": destino,
        "destination_lat": lat,
        "destination_lng": lng,
        "carrier": transportadora,
        "status": status,
        "is_on_time": is_on_time,
        "is_late": is_late,
        "distance_km": distance_km,
        "duration_min": duration_min,
        "scheduled_delivery": scheduled,
        "delivery_date": delivery,
    })

# ============================================================
# INSERE NO BIGQUERY (substitui os dados antigos)
# ============================================================
table_ref = client.dataset(DATASET).table(TABLE)

# Apaga os dados antigos para evitar duplicação
client.query(f"DELETE FROM `{PROJECT_ID}.{DATASET}.{TABLE} WHERE TRUE").result()

# Insere os novos registros
errors = client.insert_rows_json(table_ref, registros)
if errors:
    print(f"ERRO ao inserir: {errors}")
else:
    print(f"✅ Inseridas {len(registros)} entregas distribuídas em {min(7, len(registros))} dias.")
    for r in sorted(registros, key=lambda x: x["delivery_date"]):
        print(f"  {r['delivery_date'].strftime('%d/%m %H:%M')} | {r['shipment_id']} | "
              f"{r['status']} | {r['distance_km']}km | {r['duration_min']}min")