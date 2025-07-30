# Bewertungskriterien – Multimodale Tests mit Gemini (Vertex AI)

---

## Herleitung der Bewertungskriterien

Die Bewertungskriterien wurden nicht willkürlich gewählt, sondern deduktiv hergeleitet:

1. **Aus den Anforderungen des Use-Cases:**
   Ziel ist die realitätsnahe Evaluation eines multimodalen, kontextsensitiven KI-Systems in mobilen Anwendungsszenarien. Dafür muss das Modell:
   - nützliche Antworten liefern,
   - mit verschiedenen Eingabeformen umgehen,
   - kontextbezogen reagieren,
   - robust bei Fehlern sein,
   - und verständlich kommunizieren.

2. **Abgleich mit wissenschaftlicher Literatur:**
   Die Kriterien wurden anschließend mit gängigen Benchmarks und Publikationen der KI-Forschung gespiegelt:
   - TruthfulQA - Measuring How Models Mimic Human Falsehoods, https://arxiv.org/abs/2109.07958
   - Multimodal Few-Shot Learning with Frozen Language Models, https://arxiv.org/pdf/2106.13884
   - Language Models are Few-Shot Learners, https://arxiv.org/abs/2005.14165
   - Beyond Accuracy - Behavioral Testing of NLP Models with CheckList, https://arxiv.org/abs/2005.04118
   - Climbing towards NLU - On Meaning, Form, and Understanding in the Age of Data, https://aclanthology.org/2020.acl-main.463.pdf

So ergibt sich ein kompaktes, wissenschaftlich gestütztes Bewertungssystem, das sowohl für technische Evaluation als auch für reale Use-Cases tragfähig ist.

---

## Ziel der Evaluation

Diese Kriterien dienen dazu, die Antworten des Gemini-Modells bei unterschiedlichen Testszenarien fair und nachvollziehbar zu bewerten.  
Sie helfen bei der Einschätzung von:

- Inhaltlicher Qualität
- Kontextverarbeitung
- Modalitätsverstehen
- Robustheit gegenüber Fehlern oder Störungen

---

## Bewertungskriterien

### 1. **Antwortqualität**
- Ist die Antwort sachlich korrekt?
- Wird die ursprüngliche Frage / Intention erfüllt?

> Skala:  
> 0 = unbrauchbar oder falsch  
> 1 = teilweise richtig, aber unklar oder unvollständig  
> 2 = korrekt, aber oberflächlich  
> 3 = korrekt, hilfreich und detailliert

Quelle: TruthfulQA - Measuring How Models Mimic Human Falsehoods

---

### 2. **Multimodales Verständnis**
- Wurden alle Eingaben (Text, Bild, Audio, Video) sinnvoll einbezogen?
- Erkennt das Modell den Zusammenhang zwischen Modalitäten?

> Skala:  
> 0 = Modalitäten ignoriert  
> 1 = Ein Modalität erkannt  
> 2 = Modalitäten unabhängig behandelt  
> 3 = Modalitäten korrekt kombiniert

Quelle: Multimodal Few-Shot Learning with Frozen Language Models

---

### 3. **Kontextsensitivität**
- Reagiert das Modell auf Kontextinformationen wie Ort, Zeit, Gerät, Netz?
- Wird Kontext korrekt interpretiert und verwendet?

> Skala:  
> 0 = Kontext ignoriert  
> 1 = Kontext erwähnt, aber nicht korrekt angewendet  
> 2 = Kontext teilweise berücksichtigt  
> 3 = Kontext vollständig und korrekt integriert

Quelle: Language Models are Few-Shot Learners

---

### 4. **Robustheit & Fehlerverhalten**
- Wie reagiert das Modell auf falsche, unvollständige oder mehrdeutige Eingaben?
- Bleibt die Antwort sinnvoll, auch bei Störungen?

> Skala:  
> 0 = Antwort bricht ab / unbrauchbar  
> 1 = Falsche Interpretation ohne Warnung  
> 2 = Reaktion mit Einschränkung / Unsicherheit  
> 3 = Fehler erkannt oder robust abgefangen

Quelle: Beyond Accuracy - Behavioral Testing of NLP Models with CheckList

---

### 5. **Antwortstil & Verständlichkeit**
- Ist die Antwort klar formuliert?
- Ist der Stil für mobile Nutzer:innen oder Techniker:innen geeignet?

> Skala:  
> 0 = schwer verständlich / verwirrend  
> 1 = formell oder zu komplex  
> 2 = klar, aber technisch anspruchsvoll  
> 3 = einfach, klar und zielgruppengerecht

Quelle: Climbing towards NLU - On Meaning, Form, and Understanding in the Age of Data

---

## Bewertungstabelle 

| Test-ID | Antwortqualität | Modalitätsverständnis | Kontextsensitivität | Robustheit | Verständlichkeit | Kommentar |
|---------|-----------------|-----------------------|---------------------|------------|------------------|----------|
|T01       | ?               | ?                     | ?                   | ?          | ?                | ...           |
| T02       | ?               | ?                     | ?                   | ?          | ?                | ...           |
|T03       | ?               | ?                     | ?                   | ?          | ?                | ...           |
| T04       | ?               | ?                     | ?                   | ?          | ?                | ...           |
|T05       | ?               | ?                     | ?                   | ?          | ?                | ...           |
| T06       | ?               | ?                     | ?                   | ?          | ?                | ...           |
|T07       | ?               | ?                     | ?                   | ?          | ?                | ...           |
| T08       | ?               | ?                     | ?                   | ?          | ?                | ...           |
|T09       | ?               | ?                     | ?                   | ?          | ?                | ...           |
| T10       | ?               | ?                     | ?                   | ?          | ?                | ...           |
|T11       | ?               | ?                     | ?                   | ?          | ?                | ...           |
| T12       | ?               | ?                     | ?                   | ?          | ?                | ...           |

---

