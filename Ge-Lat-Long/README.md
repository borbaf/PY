# Ge-Lat-Long — Agente de IA para Torre de Controle Logística

Agente conversacional que combina **dados proprietários (BigQuery)** com **dados reais do Google Maps** por meio de **function calling do Gemini (Vertex AI)**. O modelo decide, em linguagem natural, quando consultar rotas, geocodificação ou a torre de controle — entregando respostas com dados reais, sem alucinação.

> Projeto de portfólio — Engenharia de Dados + IA Generativa aplicada a logística.

---

## 🧭 Funcionalidades

| Ferramenta | Descrição |
|------------|-----------|
| `route_metrics(origin, destination)` | Distância e tempo de viagem com **trânsito atual** (Google Maps). |
| `geocode_address(address)` | Converte um endereço em coordenadas (lat/lng). |
| `shipments_by_client(client_name)` | Lista entregas de um cliente na torre de controle (BigQuery). |
| `control_tower_kpis()` | KPIs agregados: total, no prazo, atrasadas, % on-time. |
| `register_address(address, address_type, client_name?)` | Geocodifica e **cadastra um novo endereço** (origem/destino) na tabela `address_book`. |

---

## 🏗️ Como funciona

1. O usuário faz uma pergunta em linguagem natural.
2. O Gemini interpreta e decide **qual ferramenta chamar** (function calling).
3. O Google Maps calcula rotas / geocodifica endereços.
4. O BigQuery responde KPIs, entregas e cadastros.
5. O agente consolida tudo e responde com **dados reais**.

A resposta em texto só é produzida **depois** de executar todas as chamadas necessárias (garantido via `SYSTEM_INSTRUCTION`).

---

## 🛠️ Stack técnica

- **Python 3.11+**
- **Google Gemini** (Vertex AI, modelo configurável — default `gemini-2.5-flash`)
- **Google BigQuery** — torre de controle e cadastro de endereços
- **Google Maps API** — rotas com trânsito e geocodificação
- **Function Calling** — decisão autônoma do modelo
- **python-dotenv**, **google-cloud-bigquery**, **google-genai**, **googlemaps**

---

## 📁 Estrutura do projeto
```
Ge-Lat-Long/
├── main.py               # Perguntas de exemplo (run_exemplos)
├── agent.py              # TOOLS, SYSTEM_INSTRUCTION, LogisticsAgent, loop ask()
├── bigquery_client.py    # BigQueryClient: KPIs, entregas por cliente, insert de endereço
├── maps_client.py        # MapsClient: route() e geocode()
├── setup_bq.py           # Cria/recria tabelas + seeds (idempotente)
├── .env                  # Chaves e configurações (não versionar!)
└── README.md
```

---

## ✅ Pré-requisitos

- Python 3.11+
- Conta no **Google Cloud** com **BigQuery** e **Vertex AI** habilitados
- Chave da **Google Maps API** (Directions/Distance Matrix + Geocoding)
- `gcloud` instalado e autenticado (para ADC)

---

## ⚙️ Instalação
```bash
# 1. Criar e ativar o ambiente virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/macOS

# 2. Instalar dependências
pip install google-genai google-cloud-bigquery googlemaps python-dotenv
```

---

## 🔑 Configuração (`.env`)
```env
GOOGLE_MAPS_API_KEY=SUA_CHAVE_AQUI
GCP_PROJECT_ID=coherent-voice-420518
BQ_DATASET=logistics
BQ_TABLE_CONTROL_TOWER=control_tower_shipments
BQ_TABLE_ADDRESS_BOOK=address_book
```

### Autenticação

- **Vertex AI + BigQuery:** usam **ADC** (Application Default Credentials) — rode `gcloud auth application-default login` ou defina `GOOGLE_APPLICATION_CREDENTIALS`.
- **Google Maps:** usa a `GOOGLE_MAPS_API_KEY` do `.env`.

---

## 🗄️ Setup do BigQuery
```bash
python setup_bq.py
```

O script é **idempotente**: apaga e recria as tabelas a cada execução.

- `control_tower_shipments` → 6 entregas seed (3 da FarmaPlus), status `ON_TIME`/`LATE`, datas de hoje.
- `address_book` → 3 endereços seed (origens/destinos).

### Schema — `control_tower_shipments`

| Campo | Tipo |
|-------|------|
| shipment_id | STRING |
| client_name | STRING |
| origin_address / destination_address | STRING |
| origin_lat / origin_lng / destination_lat / destination_lng | FLOAT64 |
| scheduled_delivery / actual_delivery | TIMESTAMP |
| status | STRING (`ON_TIME` \| `LATE`) |
| carrier | STRING |

### Schema — `address_book`

| Campo | Tipo |
|-------|------|
| address_id | STRING |
| address | STRING |
| lat / lng | FLOAT64 |
| address_type | STRING (`ORIGEM` \| `DESTINO`) |
| client_name | STRING |
| created_at | TIMESTAMP |

---

## 🚀 Uso
```bash
python main.py
```

### Perguntas de exemplo

1. *"Qual a distância e o tempo de viagem do CD de Guarulhos até a Av. Paulista, 1000, São Paulo, considerando o trânsito atual?"*
2. *"Quais são os KPIs de desempenho das entregas hoje?"*
3. *"Liste as entregas do cliente 'FarmaPlus' e, para cada uma, calcule o tempo de viagem do CD de origem até o destino."*
4. *"Cadastre um novo endereço de origem 'CD Campinas, SP' e um novo endereço de destino 'Shopping Eldorado, Av. Rebouças, 3970, São Paulo, SP' para o cliente FarmaPlus."*

### Exemplo de saída (ilustrativo)
```
PERGUNTA: Qual a distância e o tempo de viagem do CD de Guarulhos até a Av. Paulista, 1000, São Paulo...
A distância é de 23.34 km e o tempo de viagem estimado com trânsito atual é de 62.5 minutos.

PERGUNTA: Quais são os KPIs de desempenho das entregas hoje?
Total de Entregas: 6 | Atrasadas: 3 | No Prazo: 3 | Percentual no Prazo: 50%
```

---

## 📊 Analytics (Looker Studio)

Os mesmos dados do BigQuery alimentam um dashboard no Looker Studio via VIEW modelada:
```sql
CREATE OR REPLACE VIEW `coherent-voice-420518.logistics.vw_control_tower_dashboard` AS
SELECT
  shipment_id, client_name, origin_address, destination_address,
  origin_lat, origin_lng, destination_lat, destination_lng,
  scheduled_delivery, actual_delivery, status, carrier,
  DATE(scheduled_delivery) AS delivery_date,
  CAST(scheduled_delivery AS TIME) AS scheduled_time,
  TIMESTAMP_DIFF(actual_delivery, scheduled_delivery, MINUTE) AS delay_minutes,
  CASE WHEN status = 'ON_TIME' THEN 1 ELSE 0 END AS is_on_time,
  CASE WHEN status = 'LATE'   THEN 1 ELSE 0 END  AS is_late
FROM `coherent-voice-420518.logistics.control_tower_shipments`;
```

Conecte a VIEW como fonte de dados no [Looker Studio](https://lookerstudio.google.com) e monte os painéis (visão executiva, geografia & rotas, clientes, detalhe operacional).

---

## 🗺️ Roadmap

- [x] Rotas com trânsito em tempo real (Maps)
- [x] KPIs da torre de controle (BigQuery)
- [x] Entregas por cliente com cálculo de rota
- [x] Cadastro de novos endereços (origem/destino) com geocodificação
- [x] Dashboard no Looker Studio (VIEW + fonte de dados)
- [ ] Persistência de rotas calculadas (`distance_km`, `duration_min`) na tabela
- [ ] Alertas automáticos de atraso
- [ ] Deploy em Cloud Run / API REST

---

## 📝 Licença

MIT — uso livre para fins de estudo e portfólio. Dados e chaves são ilustrativos.