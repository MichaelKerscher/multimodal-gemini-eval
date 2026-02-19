# Aggregation Report (506)
- Tests (latest runs): **90**
- Incidents with any deltas: **30**

## Mean scores by context level
### L0 (n=30)
- mean runtime: 4.7176
- mean R/H/S/D/K: 4.033333333333333/4.033333333333333/3.1/4.033333333333333/4.933333333333334
- flags (rate): safety_first=0.90, escalation_present=1.00, offline_workflow_mentioned=0.00, hallucination_suspected=0.00
### L2 (n=30)
- mean runtime: 5.203733333333333
- mean R/H/S/D/K: 4.933333333333334/4.933333333333334/4.533333333333333/4.866666666666666/4.066666666666666
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.20, hallucination_suspected=0.00
### L2B (n=30)
- mean runtime: 5.648033333333333
- mean R/H/S/D/K: 5.0/5.0/4.633333333333334/5.0/5.0
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.67, hallucination_suspected=0.00

## Mean scores by strategy
### S0 (n=30)
- mean runtime: 4.7176
- mean R/H/S/D/K: 4.033333333333333/4.033333333333333/3.1/4.033333333333333/4.933333333333334
### S1 (n=30)
- mean runtime: 5.203733333333333
- mean R/H/S/D/K: 4.933333333333334/4.933333333333334/4.533333333333333/4.866666666666666/4.066666666666666
### S2 (n=30)
- mean runtime: 5.648033333333333
- mean R/H/S/D/K: 5.0/5.0/4.633333333333334/5.0/5.0

## Top missing elements (max 20)
- Offline-Workflow bei spotty connectivity: 4
- Offline-Workflow (lokal dokumentieren, später synchronisieren): 3
- Offline-Workflow könnte expliziter sein (nur kurz erwähnt): 2
- Keine Umwelt-/Zeitkontext-Anpassung (Minimalkontext): 1
- Severity-Einschätzung fehlt (medium im Context): 1
- Zeitpunkt der Meldung nicht erwähnt: 1
- Offline-Workflow nicht explizit erwähnt trotz spotty connectivity: 1
- Offline-Workflow (lokal dokumentieren/Foto lokal speichern): 1
- Offline-Workflow nicht konsequent umgesetzt (Fernabfrage erwähnt, aber bei spotty connectivity sollte lokale Dokumentation priorisiert werden): 1
- Keine Erwähnung von Umgebungsbedingungen (da L0-Kontext minimal): 1
- Offline-Workflow bei spotty connectivity nicht explizit erwähnt: 1
- Konkrete Sicherheitsmaßnahmen (Warnweste, Absicherung) nicht explizit genannt: 1
- Keine Priorisierung aufgrund poor_visibility/night erkennbar: 1
- Konkrete Sicherheitsmaßnahmen (Warnweste, Absperrung) bei 'Bereich wirkt unsicher': 1
- Priorisierung der Eskalation bei Gefahrenlage: 1
- Keine Sicherheitsmaßnahmen für Nacht/schlechte Sicht erwähnt (CONTEXT fehlt): 1
- Umweltbedingungen (Nacht, Nebel) nicht berücksichtigt: 1
- Severity-Einschätzung fehlt (bei L0 nicht erwartbar): 1
- Offline-Workflow (Gerät offline → lokale Dokumentation/Foto-Speicherung): 1
- Severity-Einschätzung fehlt (nur aus User message 'wirkt unsicher' ableitbar): 1
