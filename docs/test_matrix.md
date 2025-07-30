# Testmatrix - Multimodale Evaluation mit Gemini (Vertex AI)

Diese Matrix beschreibt alle geplanten Testszenarien zur Evaluierung der Fähigkeiten der Gemini-Modelle (v. a. Gemini 1.5/2.5) in Bezug auf Multimodalität und Kontextsensitivität.

----

## T01 – Text Only

**Modalität(en):** Text

**Kontextdaten:** -

**Beschreibung:** Reiner Text-Input ohne Kontextinformationen.

**Ziel:** Textverständnis, Antwortqualität

**Eingabe:**
```text
Was ist künstliche Intelligenz und wie funktioniert sie in einfachen Worten?
```

---

## T02 – Bild Only

**Modalität(en):** Bild

**Kontextdaten:** -

**Beschreibung:** Analyse eines einzelnen Bildes ohne Zusatzinformationen.

**Ziel:** Bildinhaltsverständnis ohne Kontext

**Eingabe:**
```text
Bild: data/transformator.jpg
Prompt: Was ist auf diesem Bild zu sehen?
```

---

## T03 – Audio Only

**Modalität(en):** Audio (Originaldatei)

**Kontextdaten:** -  

**Beschreibung:** Gesprochene Sprache als Audiodatei wird direkt gesendet. Keine manuelle Transkription.  

**Ziel:** Direkte Audioverarbeitung im Modell (falls unterstützt)  

**Eingabe:**
```text
Audio-Datei: data/aufnahme_zaehlerproblem.wav  
Prompt: Um was geht es in der Audio?
```

---

## T04 – Text + Bild

**Modalität(en):** Text + Bild

**Kontextdaten:** -

**Beschreibung:** Das Modell erhält einen Prompt + das Transformator-Bild.

**Ziel:** Multimodales Verständnis (Prompt + Bild kombiniert)

**Eingabe:**
```text
Bild: data/transformator.jpg
Prompt: Dieses Bild zeigt ein Bauteil aus einem Schaltschrank. Was genau ist das und wofür wird es typischerweise verwendet?
```

---

## T05 – Bild + Kontext (Standort)

**Modalität(en):** Bild

**Kontextdaten:** GPS-Koordinaten

**Beschreibung:** Foto kombiniert mit Standortdaten.

**Ziel:** Kontextbezogene Antwort anhand des Ortsbezugs

**Eingabe:**
```text
Bild: data/transformator.jpg
Prompt: Ich befinde mich an der Trafostation West (47.8571, 12.1285). Was zeigt dieses Bild?
```

---

## T06 – Text + Kontext (Zeit & Gerät)

**Modalität(en):** Text

**Kontextdaten:** Zeit + Gerätedaten

**Beschreibung:** Textbeschreibung mit Zeitstempel und Gerätetyp.

**Ziel:** Antwortverhalten in Abhängigkeit von Gerätekontext und Zeit

**Eingabe:**
```text
Prompt: Mein Gerät (Pixel 7) zeigt seit 13:45 Uhr einen schwarzen Bildschirm. Was könnte die Ursache sein? Zeitpunkt: 13.07.2025, 14:00 Uhr.
```

---

## T07 – Bild + Text + Kontext

**Modalität(en):** Text + Bild

**Kontextdaten:** Standort + Zeit + Netzwerkstatus

**Beschreibung:** Multimodale Eingabe mit realitätsnahem mobilem Kontext.

**Ziel:** Bewertung der Modellleistung bei vollständigem Realwelt-Szenario

**Eingabe:**
```text
Bild: data/netzwerkschrank.jpg
Prompt: Ich bin gerade vor dem Netzwerkschrank an Standort Nord (47.8560, 12.1250), es ist 18:30 Uhr, ich habe keinen Empfang. Was könnte hier das Problem sein?
```

---

## T08 – QR/Barcode

**Modalität(en):** Bild ODER Text (Barcode-Zeichenfolge)  

**Kontextdaten:** -  

**Beschreibung:** QR-Code als Bild ODER bereits erkannter Barcode-Text (z. B. „ASSET-1234-XY“) wird übergeben.  

**Ziel:** Interpretation von strukturierten Daten aus Bild oder String  

**Eingabe:**
```text
Variante A (Bild):  
Bild: data/qrcode_asset123.jpg  
Prompt: Was steht in diesem QR-Code? Wozu gehört dieses Bauteil?

Variante B (Text):  
Prompt: Der gescannte Barcode lautet: ASSET-1234-XY. Was kann man daraus ableiten?
```

---

## T09 – Video only

**Modalität(en):** Video  

**Kontextdaten:** -  

**Beschreibung:** Video wird direkt übergeben. Keine Zerlegung in Bilder.  

**Ziel:** Analyse bewegter Szenen, Geräusche oder Ablauf  

**Eingabe:**
```text
Video-Datei: data/störung_kabelschacht.mp4  
Prompt: Was passiert in diesem Video? Was ist möglicherweise das Problem?
```

---

## T10 – Irreführender Kontext

**Modalität(en):** Bild + Text

**Kontextdaten:** Falscher Standort

**Beschreibung:** Test auf Kontextrobustheit durch absichtlich falsche Metadaten.

**Ziel:** Prüfung auf Überanpassung an Kontextdaten

**Eingabe:**
```text
Bild: data/transformator.jpg
Prompt: Ich bin im Heizraum (obwohl Bild eine Trafostation zeigt). Was ist auf diesem Bild zu sehen?
```

---

## T11 – Prompt-Optimierung

**Modalität(en):** Text

**Kontextdaten:** -

**Beschreibung:** Vergleich verschiedener Formulierungen zur gleichen Frage.

**Ziel:** Untersuchung des Einflusses der Promptstruktur

**Eingabe:**
```text
Prompt A: Erkläre kurz, wie ein Trafo funktioniert.
Prompt B: Du bist ein Technikexperte. Erkläre mir bitte, wie ein Transformator funktioniert.
```

---

## T12 – Fehlerhafte Daten

**Modalität(en):** Bild + Text

**Kontextdaten:** Unvollständig

**Beschreibung:** Test mit beschädigtem Bild. PS: Set-Content -Path data\corrupted_image.jpg -Value "ABC123"

**Ziel:** Fehlerverhalten, Stabilität

**Eingabe:**
```text
Bild: data/corrupted_image.jpg
Prompt: Dieses Gerät funktioniert nicht. Was könnte los sein?
```

