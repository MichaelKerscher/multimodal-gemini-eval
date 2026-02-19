# Aggregation Report (506)
- Tests (latest runs): **90**
- Incidents with any deltas: **30**

## Mean scores by context level
### L0 (n=30)
- mean runtime: 5.0301
- mean R/H/S/D/K: 4.1/4.1/3.3333333333333335/4.1/4.8
- flags (rate): safety_first=0.93, escalation_present=1.00, offline_workflow_mentioned=0.00, hallucination_suspected=0.00
### L2 (n=30)
- mean runtime: 5.584233333333333
- mean R/H/S/D/K: 4.966666666666667/4.966666666666667/4.733333333333333/4.9/4.2
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.30, hallucination_suspected=0.00
### L2B (n=30)
- mean runtime: 6.090533333333334
- mean R/H/S/D/K: 5.0/5.0/4.733333333333333/5.0/5.0
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.70, hallucination_suspected=0.00

## Mean scores by strategy
### S0 (n=30)
- mean runtime: 5.0301
- mean R/H/S/D/K: 4.1/4.1/3.3333333333333335/4.1/4.8
### S1 (n=30)
- mean runtime: 5.584233333333333
- mean R/H/S/D/K: 4.966666666666667/4.966666666666667/4.733333333333333/4.9/4.2
### S2 (n=30)
- mean runtime: 6.090533333333334
- mean R/H/S/D/K: 5.0/5.0/4.733333333333333/5.0/5.0

## Top missing elements (max 20)
- Offline-Workflow bei spotty connectivity: 5
- Offline-Workflow (lokal dokumentieren, später synchronisieren): 1
- Keine Offline-Workflow-Erwähnung (aber CONTEXT zeigt kein connectivity-Feld, daher nicht zwingend erwartbar): 1
- Severity-Einschätzung fehlt (bei L0 nicht erwartbar): 1
- Offline-Workflow bei spotty connectivity nicht erwähnt: 1
- Keine Erwähnung von Warnweste/Warnblinkanlage trotz 'Bereich wirkt unsicher': 1
- Keine konkrete Absicherungsmaßnahme (Pylonen/Warnbake) genannt: 1
- Offline-Workflow nicht explizit erwähnt trotz connectivity='spotty': 1
- Severity-Einschätzung fehlt (im Kontext nicht vorhanden): 1
- Konkrete Verkehrssicherheits-Maßnahmen bei hoher Exposition nicht erkennbar: 1
- Keine Erwähnung von Dämmerung/Sichtverhältnissen (im Kontext nicht vorhanden, daher kein Fehler): 1
- Keine Erwähnung der Umgebungsbedingungen (Nacht, Nebel, schlechte Sicht): 1
- Severity/Dringlichkeit nicht erkennbar (CONTEXT leer): 1
- Keine Priorisierung erkennbar trotz 'Bereich wirkt unsicher': 1
- Keine Hinweise auf Zeitkritikalität: 1
- Keine explizite Priorisierung wegen 'Bereich wirkt unsicher': 1
- Offline-Workflow (lokal dokumentieren/Foto lokal speichern): 1
