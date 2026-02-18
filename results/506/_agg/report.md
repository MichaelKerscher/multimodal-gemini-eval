# Aggregation Report (506)
- Tests (latest runs): **90**
- Incidents with any deltas: **30**

## Mean scores by context level
### L0 (n=30)
- mean runtime: 3.5564666666666667
- mean R/H/S/D/K: 3.8666666666666667/3.8666666666666667/2.966666666666667/3.8666666666666667/4.733333333333333
- flags (rate): safety_first=0.93, escalation_present=0.93, offline_workflow_mentioned=0.00, hallucination_suspected=0.00
### L2 (n=30)
- mean runtime: 4.046433333333334
- mean R/H/S/D/K: 4.6/4.533333333333333/4.266666666666667/4.5/3.7333333333333334
- flags (rate): safety_first=0.93, escalation_present=0.93, offline_workflow_mentioned=0.13, hallucination_suspected=0.03
### L2B (n=30)
- mean runtime: 4.3028666666666675
- mean R/H/S/D/K: 4.733333333333333/4.733333333333333/4.366666666666666/4.733333333333333/4.733333333333333
- flags (rate): safety_first=0.93, escalation_present=0.93, offline_workflow_mentioned=0.60, hallucination_suspected=0.00

## Mean scores by strategy
### S0 (n=30)
- mean runtime: 3.5564666666666667
- mean R/H/S/D/K: 3.8666666666666667/3.8666666666666667/2.966666666666667/3.8666666666666667/4.733333333333333
### S1 (n=30)
- mean runtime: 4.046433333333334
- mean R/H/S/D/K: 4.6/4.533333333333333/4.266666666666667/4.5/3.7333333333333334
### S2 (n=30)
- mean runtime: 4.3028666666666675
- mean R/H/S/D/K: 4.733333333333333/4.733333333333333/4.366666666666666/4.733333333333333/4.733333333333333

## Top missing elements (max 20)
- judge_missing_for_test_id: 6
- Offline-Workflow bei spotty connectivity: 4
- Offline-Workflow (Gerät ist offline): 1
- Klarstellung: device_state betrifft Techniker-Gerät, nicht Asset: 1
- Keine Berücksichtigung der Umgebungsbedingungen (nicht im Context): 1
- Keine Kontextanpassung an Umgebungsbedingungen (minimal context): 1
- Offline-Workflow nicht explizit erwähnt trotz spotty connectivity: 1
- Keine explizite Priorisierung wegen 'unsicherer Bereich': 1
- Keine Erwähnung von Verkehrssicherung bei hoher Gefährdung: 1
- Offline-Workflow nicht erwähnt trotz connectivity=offline: 1
- Keine Anleitung für lokale Dokumentation/Synchronisation: 1
- Offline-Workflow unvollständig (nur 'Gerät offline' erwähnt, aber keine explizite lokale Speicherung/Synchronisation): 1
- Keine Erwähnung von Warnweste (bei L0 aber nicht zwingend erwartbar): 1
- Keine explizite Priorisierung der Verkehrssicherheit bei hohem Risiko: 1
- Konkrete Sicherheitsmaßnahmen bei hoher Verkehrsexposition fehlen: 1
- Severity-Einschätzung fehlt (L0 gibt keine severity vor): 1
- Offline-Workflow nicht erwähnt (connectivity=spotty, device_state=low_battery): 1
- Hinweis auf lokale Speicherung/Synchronisation fehlt: 1
- Keine Erwähnung von Dämmerung/schlechter Sicht (nicht im Context): 1
- Keine spezifische Verkehrssicherheitsmaßnahme bei Dunkelheit: 1
