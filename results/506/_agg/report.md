# Aggregation Report (506)
- judge_version filter: **judge_v1_1**
- Tests (latest runs): **90**
- Incidents with any deltas: **30**

## Mean scores by context level (snapshot)
### L0 (n=30)
- mean runtime: 4.829166666666667
- mean R/H/S/D/K: 3.566666666666667/3.566666666666667/3.2/3.6666666666666665/2.7
- mean overall (avg R/H/S/D/K): 3.3400000000000003
- flags (rate): safety_first=0.93, escalation_present=1.00, offline_workflow_mentioned=0.00, hallucination_suspected=0.00
### L2 (n=30)
- mean runtime: 5.689166666666667
- mean R/H/S/D/K: 4.666666666666667/4.533333333333333/4.366666666666666/4.466666666666667/4.0
- mean overall (avg R/H/S/D/K): 4.406666666666666
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.33, hallucination_suspected=0.03
### L2B (n=30)
- mean runtime: 5.5254
- mean R/H/S/D/K: 4.933333333333334/4.9/4.6/4.766666666666667/4.933333333333334
- mean overall (avg R/H/S/D/K): 4.826666666666667
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.63, hallucination_suspected=0.00

## Mean scores by strategy (snapshot)
### S0 (n=30)
- mean runtime: 4.829166666666667
- mean R/H/S/D/K: 3.566666666666667/3.566666666666667/3.2/3.6666666666666665/2.7
- mean overall (avg R/H/S/D/K): 3.3400000000000003
### S1 (n=30)
- mean runtime: 5.689166666666667
- mean R/H/S/D/K: 4.666666666666667/4.533333333333333/4.366666666666666/4.466666666666667/4.0
- mean overall (avg R/H/S/D/K): 4.406666666666666
### S2 (n=30)
- mean runtime: 5.5254
- mean R/H/S/D/K: 4.933333333333334/4.9/4.6/4.766666666666667/4.933333333333334
- mean overall (avg R/H/S/D/K): 4.826666666666667

## Top missing elements (max 20)
- Keine Nutzung der Asset-ID im Kontext: 2
- Keine Anpassung an Umgebungsbedingungen: 2
- Offline-Workflow bei spotty connectivity nicht explizit erwähnt: 2
- Safety-first nicht als Schritt 1 priorisiert: 2
- Kontextnutzung minimal (nur Asset-ID): 2
- Offline-Workflow nicht erwartbar (kein Signal im Kontext): 1
- Kontextnutzung minimal (nur Asset-ID vorhanden): 1
- Offline-Workflow fehlt (connectivity=offline im Kontext): 1
- Halluzination: 'Gerät meldet low_battery' suggeriert Asset-Problem, obwohl device.* das Techniker-Gerät beschreibt: 1
- Keine Anpassung an intermittent fault_type: 1
- Keine Erwähnung vorhandener Foto-Dokumentation: 1
- Keine explizite Priorisierung bei medium severity: 1
- Keine Kontextnutzung erkennbar (minimaler Context): 1
- Generische Schritte ohne Fallspezifik: 1
- Offline-Workflow nur implizit (spotty connectivity erwähnt, aber kein klarer 'lokal speichern'-Hinweis): 1
- Offline-Workflow nicht erwähnt (aber auch nicht erwartbar bei minimalem Context): 1
- Keine explizite Priorisierung bei severity=high sichtbar: 1
- Keine Anweisung zu lokaler Datenspeicherung/Synchronisation: 1
- Keine klare Eskalations-Trigger-Logik bei severity=high: 1
- Offline-Workflow nicht erwähnt (connectivity=offline im CONTEXT): 1
