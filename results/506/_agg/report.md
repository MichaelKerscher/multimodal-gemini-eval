# Aggregation Report (506)
- Tests (latest runs): **90**
- Incidents with any deltas: **30**

## Mean scores by context level
### L0 (n=30)
- mean runtime: 4.8357
- mean R/H/S/D/K: 4.066666666666666/4.066666666666666/3.2333333333333334/4.066666666666666/4.933333333333334
- flags (rate): safety_first=0.90, escalation_present=1.00, offline_workflow_mentioned=0.00, hallucination_suspected=0.00
### L2 (n=30)
- mean runtime: 5.2806999999999995
- mean R/H/S/D/K: 4.933333333333334/4.933333333333334/4.666666666666667/4.933333333333334/4.2
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.30, hallucination_suspected=0.03
### L2B (n=30)
- mean runtime: 6.1619
- mean R/H/S/D/K: 5.0/5.0/4.666666666666667/5.0/5.0
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.60, hallucination_suspected=0.00

## Mean scores by strategy
### S0 (n=30)
- mean runtime: 4.8357
- mean R/H/S/D/K: 4.066666666666666/4.066666666666666/3.2333333333333334/4.066666666666666/4.933333333333334
### S1 (n=30)
- mean runtime: 5.2806999999999995
- mean R/H/S/D/K: 4.933333333333334/4.933333333333334/4.666666666666667/4.933333333333334/4.2
### S2 (n=30)
- mean runtime: 6.1619
- mean R/H/S/D/K: 5.0/5.0/4.666666666666667/5.0/5.0

## Top missing elements (max 20)
- Offline-Workflow bei spotty connectivity: 6
- Offline-Workflow fehlt (connectivity=offline): 1
- Verwechslung device_state mit Asset-Zustand: 1
- Keine Erwähnung von Warnweste/PSA: 1
- Keine Priorisierung bei severity=high erkennbar: 1
- Offline-Workflow bei connectivity=spotty nicht explizit erwähnt: 1
- Keine Erwähnung von Offline-Workflow (nicht erwartbar bei L0_minimal): 1
- Offline-Workflow nur angedeutet ('manuell auslesen'), nicht explizit als Offline-Dokumentation beschrieben: 1
- Keine Offline-Workflow-Erwähnung (aber CONTEXT zeigt keine connectivity-Info, daher kein Abzug): 1
- Offline-Workflow nur implizit ('keine Ferndiagnose möglich'), nicht explizit als Handlungsanweisung: 1
- Severity-Einschätzung fehlt (User erwähnt 'unsicher', aber keine explizite Priorisierung): 1
- Keine explizite Priorisierung der Absicherung bei unbekannten Umgebungsbedingungen: 1
- Keine Berücksichtigung der Umgebungsbedingungen (Nacht/Nebel nicht im Context): 1
- Severity-Einschätzung fehlt (bei L0 nicht erwartbar): 1
- Severity-Einschätzung fehlt (im Kontext nicht vorhanden, aber aus User-Message 'wirkt unsicher' ableitbar): 1
- Konkrete Zeitangabe zur Eskalation fehlt: 1
- Offline-Workflow (lokal dokumentieren/synchronisieren): 1
