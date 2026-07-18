# DachAssist AI

KI-Kundenassistent für Handwerksbetriebe.

## Projektstruktur

```
dachassist-ai/
├── backend/              # Python/FastAPI Backend
│   └── app/
│       ├── api/          # API-Endpunkte
│       ├── domain/       # Datenmodelle
│       ├── services/     # Business-Logik
│       ├── storage/      # Persistierung
│       ├── infrastructure/  # Externe APIs
│       └── core/         # Konfiguration
├── customers/            # Mandanten-Daten
│   └── <company_id>/
│       ├── config.json   # Unternehmensdaten
│       ├── prompts/      # System-Prompts
│       ├── knowledge/    # Wissensdatenbank
│       └── leads/        # Kundengespräche
└── README.md
```

## Setup

### 1. Umgebung vorbereiten

```bash
cd backend
python -m venv venv
source venv/bin/activate  # oder: venv\Scripts\activate (Windows)
pip install -r requirements.txt
```

### 2. .env erstellen

```bash
cp .env.example .env
# .env öffnen und OPENAI_API_KEY eintragen
```

### 3. Server starten

```bash
uvicorn app.main:app --reload
```

Server läuft unter: http://localhost:8000

## API testen

### Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{"status": "ok"}
```

### Chat - Erste Anfrage (new session)

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "company_id": "dachtechnik-wolf",
    "message": "Mein Dach ist undicht."
  }'
```

Response:
```json
{
  "reply": "...",
  "session_id": "session_abc123...",
  "lead_id": "lead_..."
}
```

### Chat - Follow-up (existing session)

Kopiere die `session_id` aus der vorherigen Response:

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "company_id": "dachtechnik-wolf",
    "message": "Können Sie morgen vorbeikommen?",
    "session_id": "session_abc123..."
  }'
```

## Lead-Daten anschauen

Nach dem Chat sind die Daten gespeichert unter:

```
customers/dachtechnik-wolf/leads/lead_*.json
```

JSON-Struktur:
```json
{
  "id": "lead_...",
  "company_id": "dachtechnik-wolf",
  "created_at": "2024-07-18T10:00:00",
  "updated_at": "2024-07-18T10:05:00",
  "contact": {
    "name": null,
    "phone": null,
    "email": null,
    "address": null
  },
  "inquiry": {
    "type": null,
    "summary": null,
    "urgency": null,
    "is_emergency": false
  },
  "conversation": [
    {
      "timestamp": "2024-07-18T10:00:00",
      "role": "user",
      "message": "Mein Dach ist undicht."
    },
    {
      "timestamp": "2024-07-18T10:00:05",
      "role": "assistant",
      "message": "..."
    }
  ]
}
```

## Nächste Schritte

- [ ] Feature 5: Kontaktdaten-Erfassung (Regex + LLM)
- [ ] Feature 6: Zusammenfassung für Mitarbeiter
- [ ] Feature 7: Frontend Chat-Widget
- [ ] Feature 8: Leads-Dashboard
