# Aggregation Report (506)
- Tests (latest runs): **90**
- Incidents with any deltas: **30**

## Mean scores by context level
### L0 (n=30)
- mean runtime: 3.8349333333333333
- mean R/H/S/D/K: 4.066666666666666/4.066666666666666/3.1666666666666665/4.033333333333333/5.0
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.00, hallucination_suspected=0.00
### L2 (n=30)
- mean runtime: 4.155233333333333
- mean R/H/S/D/K: 4.933333333333334/4.933333333333334/4.433333333333334/4.766666666666667/4.633333333333334
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.40, hallucination_suspected=0.00
### L2B (n=30)
- mean runtime: 4.324733333333333
- mean R/H/S/D/K: 4.966666666666667/4.966666666666667/4.433333333333334/4.933333333333334/5.0
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.67, hallucination_suspected=0.00

## Mean scores by strategy
### S0 (n=30)
- mean runtime: 3.8349333333333333
- mean R/H/S/D/K: 4.066666666666666/4.066666666666666/3.1666666666666665/4.033333333333333/5.0
### S1 (n=30)
- mean runtime: 4.155233333333333
- mean R/H/S/D/K: 4.933333333333334/4.933333333333334/4.433333333333334/4.766666666666667/4.633333333333334
### S2 (n=30)
- mean runtime: 4.324733333333333
- mean R/H/S/D/K: 4.966666666666667/4.966666666666667/4.433333333333334/4.933333333333334/5.0

## Top missing elements (max 20)
- Offline-Workflow bei spotty connectivity nicht erwähnt: 2
- Keine Spekulation über Asset-Typ (Lampe/Ampel) bei minimalem Context: 1
- Keine Offline-Workflow-Erwähnung (aber auch nicht nötig bei L0-Kontext): 1
- Keine Kontextnutzung erkennbar (nur Asset-ID vorhanden): 1
- Offline-Workflow nicht erwähnt trotz spotty connectivity: 1
- Severity=high nicht ausreichend betont in Eskalation: 1
- Keine Kontextinformationen zu Umgebung/Risiko vorhanden, daher Safety-Maßnahmen generisch: 1
- Offline-Workflow nicht erwähnt trotz spotty connectivity + low_battery: 1
- Hinweis auf device_state bezieht sich auf Gerät, nicht Asset – könnte klarer sein: 1
- Keine explizite Priorisierung trotz 'Bereich wirkt unsicher': 1
- Asset-Typ unklar (Lampe/Ampel) – Antwort spekuliert beide Möglichkeiten: 1
- Keine Erwähnung von Warnweste/persönlicher Schutzausrüstung: 1
- Severity-Einschätzung fehlt (User erwähnt 'unsicher', aber keine explizite Priorisierung): 1
- Offline-Workflow bei spotty connectivity nicht explizit erwähnt: 1
- Keine Umwelt-/Zeitkontext vorhanden, daher Safety-Maßnahmen generisch: 1
- Keine explizite Priorisierung bei Verkehrsgefahr: 1
- Keine Priorisierung erkennbar bei minimalem Kontext: 1
- Rückfrage zu Asset-Typ unnötig spekulativ: 1
- Severity-Einschätzung fehlt (nur aus User message 'unsicher' ableitbar): 1
- Keine Offline-Workflow-Erwähnung (aber CONTEXT zeigt kein connectivity-Problem): 1
