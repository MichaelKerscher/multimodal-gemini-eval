# Architekturübersicht - Projekt: Multimodale KI-Evaluation mit Gemini

## Zielsetzung

Dieses Projekt untersucht die technische Machbarkeit und Leistungsfähigkeit multimodaler, kontextsensitiver mobiler Anwendungen mit Hilfe von Googles Vertex AI Gemini API. Im Fokus steht nicht ein konkreter Geschäftsprozess, sondern die systematische Erprobung der aktuellen KI-Fähigkeiten für reale, mobile Nutzungsszenarien.

---

## Zielarchitektur

[Flutter App (UI, Kontext)] <-> [Python-Backend] <-> [Google Vertex AI Gemini API]

### 1. Flutter App
- Eingabemöglichkeiten: Text, Bild, Audio, Video, QR/Barcode
- Kontextdaten: GPS-Standort, Zeit, Geräteinformationen
- Rolle: Einfache UX, Weiterleitung an Backend (REST/HTTP)

### 2. Python-Backend
- Zentrale API-Schnittstelle zu Gemini
- Kontextverarbeitung und Anreicherung
- Logging aller Eingaben und Ausgaben (zur Evaluierung)
- Tests: Direkt in Python-Skripten durchführbar
- Deployment-Ziel: Docker-kompatibel

### 3. Vertex AI Gemini API
- Zugang zur Gemini 2.5 Modellfamilie
- Unterstützt Multimodalität (Text, Bild, Audio, Video)
- API-Zugriff via Google Gen AI SDK
- Genutzt wird Vertex AI (nicht Developer API), da:
    - Produktionstauglich
    - Unternehmenssteuerung & GCP-Integration
    - Hinweis: Die Legacy-Bibliotheken (z. B. `google-generativeai`) werden bis Ende September 2025 abgelöst. Google empfiehlt die Migration auf das neue **Google Gen AI SDK**, das sowohl die Gemini Developer API als auch die Vertex AI Gemini API unterstützt. Somit bleibt der Zugang zu beiden APIs zentralisiert und zukunftssicher.

### Technologiewahl - Begründung
| Komponente    | Technologie | Begründung                                  |
|---------------|-------------|---------------------------------------------|
| App-Frontend  | Flutter     | Plattformunabhängigkeit, gute Sensoranbindung |
| Backend       | Python      | Schnelle Tests, gute Gemini-SDK-Unterstützung |
| KI-Plattform  | Vertex AI   | Multimodalität, Skalierbarkeit, GCP-native    |
| Deployment    | Docker      | Portabel, standardisiert, CI/CD-ready         |

## Entwicklungsstrategie
1. Start ohne App: Alle Eingaben (Bild, Audio, Video, Kontext) werden in Python simuliert
2. Modulare Tests: Jedes Szenario als separates Skript
3. Testmatrix: systematisch alle Kombinationen aus Modalitäten und Kontextinformationen prüfen
4. Flutter-App: Wird später zur realistischen UI-Einbindung entwickelt.

## Projektstruktur - technisch
multimodal-gemini-eval/
|-- docs/               <-- Architektur, API-Infos, Tests
|-- scripts/            <-- Testszenarien (Python)
|-- lib/                <-- Wiederverwendbare Helfer (z.B. Gemini-Client)
|-- data/               <-- Testdaten (Bilder, Audio, Video, JSON)
|-- results/            <-- Logs und Antworten
|-- .env                <-- API-Keys & Konfig (lokal, nicht ins Repo einchecken)
|-- requirements.txt    <-- Python-Abhängigkeiten
|-- Dockerfile          <-- Deployment (später)
|-- README.md           <-- Einstieg & Übersicht

