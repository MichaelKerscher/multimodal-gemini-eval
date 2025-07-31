# Multimodale Evaluation mit Google Gemini (Vertex AI)

Dieses Projekt evaluiert die Fähigkeiten der Gemini-Modelle von Google Cloud im Kontext multimodaler mobiler Applikationen. Fokus liegt auf realitätsnahen Szenarien mit Bild, Text, Spracheingabe und kontextsensitiven Informationen.

## Zielarchitektur
Flutter App ↔ Python Backend ↔ Gemini Vertex AI API

## Aufbau
- `scripts/`: einzelne Tests
- `lib/`: wiederverwendbare API-Helfer
- `docs/`: technische Dokumentation und Analysen
- .env: Authentifizierung mit GOOGLE_APPLICATION_CREDENTIALS, GOOGLE_GENAI_USE_VERTEXAI, GCP_PROJECT_ID, GCP_LOCATION

## Setup
```bash
pip install -r requirements.txt
python scripts/test_01_text_only.py
```