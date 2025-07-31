# Vergleich der geplanten Zielarchitektur mit den Ergebnissen der Evaluation

Zusammenfassung der Ergebnisse der Evaluation von **gemini-2.5-flash** und Vergleich mit der geplanten Zielarchitektur für die mobile, multimodale Support-App.  
Zudem werden Handlungsempfehlungen für die produktive Nutzung abgeleitet und der noch ausstehende Integrationsschritt zwischen App und Backend erläutert.

---

## 1. Geplante Zielarchitektur

**Ziel:**  
Eine mobile App (Flutter) soll multimodale Eingaben von Außendienstmitarbeitenden entgegennehmen und kontextsensitive Antworten generieren.

**Architektur:**

[Flutter App (UI, Kontext)] <-> [Python-Backend] <-> [Vertex AI Gemini API]

1. Flutter App
- Eingaben: Text, Bild, Audio, Video, QR/Barcode
- Kontextdaten: GPS, Zeit, Geräteinfos
- Rolle: Schlanke UI + Sensorintegration

2. Python Backend
- Schnittstelle zu Gemini (google-genai SDK)
- Kontextverarbeitung & Anreicherung
- Logging aller Ein-/Ausgaben
- Ziel: Docker-fähig, für Cloud- oder On-Prem-Deployment

3. Vertex AI Gemini API
- Multimodal (Text, Bild, Audio, Video)
- Nutzung von Gemini 2.5 Flash (schnell) oder Pro/Pro-Vision (präziser)


---

## 2. Ergebnisse aus der Evaluation

**Getestete Modalitäten:**  
- Text, Bild, Audio, Video (inkl. QR/Barcode-Test)

**Stärken:**
- **Hohe Antwortqualität**: Meist korrekt, hilfreich und verständlich (Ø 2.5 von 3)  
- **Sehr gutes Modalitätsverständnis**: Bild-, Audio- und Video-Inputs werden sauber verarbeitet (Ø 2.8 von 3)  
- **Klarer Antwortstil**: Verständliche und gut strukturierte Antworten

**Schwächen:**
- **Kontextsensitivität**: Kontextinformationen (z. B. Standort) werden oft ignoriert oder nicht reflektiert (Ø 1.6 von 3)  
- **Robustheit**: Unsicherheit bei fehlerhaften Eingaben oder QR-Code-Interpretation (Ø 2.0 von 3)  
- **Verständlichkeit bei langen Antworten**: Manche Antworten sind für mobile Nutzer zu ausführlich

**Beispiele:**
- **T05**: Standort ignoriert  
- **T08**: QR-Code erkannt, aber URL halluziniert  
- **T12**: Fehlerhafte Eingabe erkannt, aber schwach kommuniziert

---

## 3. Abgleich mit Zielarchitektur

| Komponente            | Ziel                                     | Evaluationsergebnis                        | Bewertung |
|-----------------------|-----------------------------------------|-------------------------------------------|----------|
| **Flutter App**       | Text, Bild, Audio, Video, QR/Barcode     | Alle Modalitäten unterstützt, QR-Code unsicher | 4/5 |
| **Kontextdaten**      | Nutzung von GPS, Zeit, Gerät             | Kontext meist ignoriert                 | 2/5 |
| **Python Backend**    | Schnittstelle + Logging + Routing        | Stabil und funktionsfähig                | 5/5 |
| **Vertex AI Gemini**  | Multimodalität & Reaktionsgeschwindigkeit | Sehr gute Performance                    | 5/5 |
| **Robustheit**        | Fehler- und Halluzinationsresistenz      | Schwächen bei QR & fehlerhaften Inputs   | 2/5 |

---

## 4. Interpretation für produktive Nutzung

1. **Machbarkeit:**  
   - Die geplante Architektur ist **technisch realisierbar**, da `gemini-2.5-flash` multimodale Eingaben zuverlässig verarbeitet.  
   - Integration mit Python-Backend und Flutter-Frontend ist unproblematisch.

2. **Risikobereiche:**  
   - **Kontextnutzung schwach** → Kontext muss in Prompts **explizit betont** werden.  
   - **Robustheit begrenzt** → Backend sollte Plausibilitätsprüfungen und Postprocessing implementieren.

3. **Empfehlungen:**  
   - **Prompt-Engineering**: Kontextinformationen verstärkt einbinden; lange Antworten unterbinden.  
   - **Backend-Validierung**: z. B. QR-Codes verifizieren, ungültige URLs erkennen. 
   - **Antwortverkürzung in der App**: Lange Antworten ggf. zusammenfassen oder staffeln.

---

## 5. Noch offene Aufgaben: Kopplung von App und Backend

Aktuell:
- Die Flutter-App kann multimodale Daten und Kontext aufnehmen.
- Die Python-Skripte laufen lokal in der CMD und sind nicht als Server angebunden.

**Offene Schritte:**
1. **Backend als REST- oder WebSocket-Server aufsetzen**
   - Empfehlung: **FastAPI** für asynchrone Requests & File Uploads
   - Endpunkte:
     - `POST /api/evaluate` → Nimmt Prompt, Kontext, Datei entgegen
     - `GET /api/status` → Optional für Healthcheck

2. **App-seitige Integration**
   - Sende Eingaben per HTTP-POST (JSON oder Multipart-Form für Dateien)
   - Empfange JSON-Response mit Modellantwort und Metadaten

3. **Logging & Auswertung**
   - Backend speichert Antworten weiterhin als JSON in `results/`
   - Optional: Speicherung in DB für spätere Auswertung

4. **Deployment**
   - Docker-Container für Backend vorbereiten
   - Später: Deployment in GCP, VM oder lokal im Unternehmensnetz

---

## 6. Fazit

Die **Evaluation bestätigt** die technische Machbarkeit der geplanten Zielarchitektur.  
Für die produktive Nutzung sind jedoch folgende Maßnahmen notwendig:

- Kontext stärker im Prompt nutzen  
- Plausibilitätsprüfungen und Postprocessing im Backend   
- Aufbau eines stabilen REST-Backends für die App-Anbindung  

Damit kann die App perspektivisch produktiv eingesetzt werden, um multimodale Unterstützung für Stadtwerke-Mitarbeitende zu bieten.

---
