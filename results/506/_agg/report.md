# Aggregation Report (506)
- Tests (latest runs): **90**
- Incidents with any deltas: **30**

## Mean scores by context level
### L0 (n=30)
- mean runtime: 5.142033333333333
- mean R/H/S/D/K: 4.066666666666666/4.066666666666666/3.2666666666666666/4.066666666666666/4.833333333333333
- flags (rate): safety_first=0.93, escalation_present=1.00, offline_workflow_mentioned=0.00, hallucination_suspected=0.00
### L2 (n=30)
- mean runtime: 6.513766666666667
- mean R/H/S/D/K: 4.966666666666667/4.966666666666667/4.633333333333334/4.9/4.1
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.27, hallucination_suspected=0.03
### L2B (n=30)
- mean runtime: 5.525033333333334
- mean R/H/S/D/K: 5.0/5.0/4.766666666666667/5.0/5.0
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.60, hallucination_suspected=0.00

## Mean scores by strategy
### S0 (n=30)
- mean runtime: 5.142033333333333
- mean R/H/S/D/K: 4.066666666666666/4.066666666666666/3.2666666666666666/4.066666666666666/4.833333333333333
### S1 (n=30)
- mean runtime: 6.513766666666667
- mean R/H/S/D/K: 4.966666666666667/4.966666666666667/4.633333333333334/4.9/4.1
### S2 (n=30)
- mean runtime: 5.525033333333334
- mean R/H/S/D/K: 5.0/5.0/4.766666666666667/5.0/5.0

## Top missing elements (max 20)
- Offline-Workflow bei spotty connectivity: 4
- Offline-Workflow (connectivity=offline): 2
- Offline-Workflow (lokal dokumentieren, später synchronisieren): 1
- Severity-Einschätzung fehlt (nur aus User-Text 'wirkt unsicher' ableitbar): 1
- Offline-Workflow fehlt (connectivity=offline im CONTEXT): 1
- Keine Anweisung zu lokaler Datenspeicherung/Synchronisation: 1
- Hinweis auf lokale Dokumentation/Synchronisation: 1
- Keine Erwähnung von Warnweste/persönlicher Schutzausrüstung: 1
- Keine konkrete Anweisung zur Verkehrssicherung bei Nacht: 1
- Keine explizite Priorisierung wegen 'Bereich wirkt unsicher' im User-Text: 1
- Severity-Einschätzung fehlt (nur Asset-ID gegeben): 1
- Offline-Workflow bei spotty connectivity nicht erwähnt: 1
- Keine Erwähnung von Offline-Workflow (nicht erwartbar bei L0_minimal ohne connectivity-Info): 1
- Severity-Einstufung fehlt (User erwähnt 'unsicher', aber keine explizite Priorisierung): 1
- Keine Erwähnung von Zeitkritikalität trotz Sicherheitsbedenken: 1
- Offline-Workflow könnte expliziter sein (lokal speichern, später synchronisieren): 1
- Keine Priorisierung bei minimaler Kontextlage erkennbar: 1
- Absicherungsmaßnahmen bleiben vage ('falls möglich'): 1
- Lokale Dokumentation/Synchronisation: 1
- Konkrete Sicherheitsmaßnahmen bei Dämmerung/schlechter Sicht nicht erwähnt: 1
