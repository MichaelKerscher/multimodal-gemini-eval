# Gemini API Notes - Technische Grundlagen & Plattformüberblick

Dieses Dokument fasst die wichtigsten technischen Informationen zur Verwendung der Gemini-Modelle von Google zusammen - einschließlich der verschiedenen APIs, SDKs, Plattformen und Tools. Grundlage sind offizielle Quellen.

---

## 1. Einstieg: Gemini für Entwickler und Unternehmen

Gemini 2.5-Modelle gehören zur Familie der **Thinking Models** - sie können durch interne Denkprozesse schlussfolgern, bevor sie Antworten geben.
Mehr: https://cloud.google.com/ai/gemini?hl=de

---

## 2. Tools und Plattformen im Überblick

### Google AI Studio

**https://ai.google.dev/**

Ein webbasiertes Tool zum Experimentieren, Erstellen und Testen von Prompts mit Gemini-Modellen.

- Schnellster Einstieg für Entwickler, Studierende und Forscher
- Verwendung der **Gemini Developer API**
- Kostenlose API-Schlüssel: https://aistudio.google.com/apikey
- Prompt-Testumgebung: https://aistudio.google.com/prompts/new_chat
- Quickstart-Doku: https://ai.google.dev/gemini-api/docs/quickstart?hl=de

---

### Vertex AI (Google Cloud)

**https://cloud.google.com/vertex-ai/generative-ai**

Zentrale Plattform zur Entwicklung produktionsreifer, generativer KI-Anwendungen:

- Nutzung der leistungsstärksten Gemini-Modelle via **Vertex AI Gemini API**
- Anbindung an BigQuery, Looker, GCP Security, Datenbanken etc.
- Beispiel-Prompts: https://cloud.google.com/vertex-ai/generative-ai/docs/prompt-gallery
- Quickstart-Anleitung: https://cloud.google.com/vertex-ai/generative-ai/docs/start/quickstart?usertype=apikey

> Empfohlen für produktive, unternehmensweite Anwendungen

---

## 3. Gemini in Google Cloud (Anwendungsbereiche)

| Bereich               | Link |
|----------------------|------|
| Gemini Code Assist (IDE)     | https://codeassist.google/ |
| Setup für GCP-Projekte       | https://cloud.google.com/gemini/docs/discover/set-up-gemini |
| IDE-Unterstützung            | https://codeassist.google/#available-in-your-favorite-ides-and-platforms |
| Observability & Monitoring   | https://www.youtube.com/watch?v=2qMMcX2kYhs&t=143s |
| Sicherheit & Security Center | https://cloud.google.com/gemini/docs/security-command-center/overview |
| BigQuery Integration         | https://cloud.google.com/gemini/docs/bigquery/set-up-gemini |
| Looker Integration           | https://cloud.google.com/blog/products/data-analytics/introducing-gemini-in-looker-at-next24?hl=en |
| Datenbankunterstützung       | https://cloud.google.com/gemini/docs |
| Startup-Programm             | https://cloud.google.com/startup/apply?hl=en |

---

## 4. Gemini SDK & APIs

### Installation der neuen SDK

```bash
pip install -U "google-genai"
```

```python
from google import genai
```

### Authentifizierung

| API-Zugang            | Methode |
|----------------------|------|
| Developer API         | API-Key aus Google AI Studio (GEMINI_API_KEY oder GOOGLE_API_KEY) |
| Vertex AI API         | Google Cloud Dienstkonto + Projekt-ID |

Dokumentation: https://ai.google.dev/gemini-api/docs/migrate-to-cloud?hl=de


### API-Struktur mit Client-Objekt

```python
client = genai.Client(...)  # vertexai=True, project=..., location=...

response = client.models.generate_content(...)
chat = client.chats.create(...)
file = client.files.upload(...)
tuning = client.tunings.tune(...)
```


### API-Vergleich: Developer API vs. Vertex AI API

| Kriterium         | Developer API                             | Vertex AI API                                      |
|-------------------|--------------------------------------------|----------------------------------------------------|
| **Zielgruppe**    | Entwickler, Prototypen                     | Unternehmen, produktive Systeme                    |
| **Authentifizierung** | API-Key (Google AI Studio)             | GCP-Projekt + Dienstkonto                          |
| **Plattformzugang** | [ai.google.dev](https://ai.google.dev)  | [cloud.google.com/vertex-ai](https://cloud.google.com/vertex-ai/generative-ai) |
| **SDK**           | `google-genai`                             | `google-genai`                                     |
| **Client-Erstellung** | `genai.Client()`                       | `genai.Client(vertexai=True, project=..., location=...)` |
| **Einsatzbereich** | Schnell, lokal testen                     | Produktionsreif, skalierbar, GCP-integriert        |

---

#### Beispiel: Developer API

```python
from google import genai

genai.configure(api_key="YOUR_API_KEY")

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI works in a few words"
)

print(response.text)
```

#### Beispiel: Vertex AI Gemini API

```python
from google import genai

genai.configure(api_key="YOUR_API_KEY")

client = genai.Client(
    vertexai=True,
    project="your-project-id",
    location="europe-west4"
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI works in a few words"
)

print(response.text)
```


## 5. Migration: Alte vs. neue SDKs

| Sprache           | Alt (Legacy)                          | Neu (Gen AI SDK)                          |
|-------------------|---------------------------------------|-------------------------------------------|
| Python            | google-generativeai                   | google-genai                              |
| JavaScript        | @google/generativeai                  | @google/genai                             |
| Go                | google.golang.org/generative-ai       | google.golang.org/genai                   |
| Dart/Flutter      | google-generative-ai                  | firebase_ai / REST                        |
| Swift             | generative-ai-swift                   | Gemini in Firebase                        |
| Android           | generative-ai-android                 | Gemini in Firebase                        |

Support für alte Libraries endet im September 2025
Quellen: https://ai.google.dev/gemini-api/docs/libraries?hl=de


## 6. Fazit

- Die neue Google Gen AI SDK ist zukunftssicher und zentraler Einstiegspunkt
- Vertex AI Gemini API ist klar die richtige Wahl - skalierbar, sicher, multimodal
- Alle Tools und Dokumentationen stehen frei zur Verfügung 




