# Aggregation Report (506)
- Tests (latest runs): **90**
- Incidents with any deltas: **30**

## Mean scores by context level
### L0 (n=30)
- mean runtime: 3.6137333333333332
- mean R/H/S/D/K: 4.066666666666666/4.066666666666666/3.1666666666666665/4.066666666666666/5.0
- flags (rate): safety_first=0.97, escalation_present=1.00, offline_workflow_mentioned=0.00, hallucination_suspected=0.00
### L2 (n=30)
- mean runtime: 3.7607
- mean R/H/S/D/K: 4.766666666666667/4.766666666666667/4.433333333333334/4.566666666666666/4.0
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.23, hallucination_suspected=0.07
### L2B (n=30)
- mean runtime: 4.421133333333334
- mean R/H/S/D/K: 5.0/5.0/4.6/5.0/5.0
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.67, hallucination_suspected=0.00

## Mean scores by strategy
### S0 (n=30)
- mean runtime: 3.6137333333333332
- mean R/H/S/D/K: 4.066666666666666/4.066666666666666/3.1666666666666665/4.066666666666666/5.0
### S1 (n=30)
- mean runtime: 3.7607
- mean R/H/S/D/K: 4.766666666666667/4.766666666666667/4.433333333333334/4.566666666666666/4.0
### S2 (n=30)
- mean runtime: 4.421133333333334
- mean R/H/S/D/K: 5.0/5.0/4.6/5.0/5.0

## Top missing elements (max 20)
- Offline-Workflow bei spotty connectivity: 2
- Offline-Workflow bei spotty connectivity nicht explizit erwähnt: 2
- Offline-Workflow nicht vollständig ausgearbeitet (nur Hinweis, keine konkreten Schritte für lokale Speicherung): 1
- Batterie-Hinweis bezieht sich fälschlich auf Asset statt Techniker-Gerät: 1
- Konkrete Sicherheitsmaßnahmen bei Nacht/schlechter Sicht fehlen (nur allgemein erwähnt): 1
- Keine Offline-Workflow-Erwähnung (aber CONTEXT zeigt keine Offline-Situation): 1
- Offline-Workflow nicht erwähnt (CONTEXT zeigt connectivity=offline): 1
- Keine Anweisung zur lokalen Dokumentation/Synchronisation: 1
- Offline-Workflow explizit erwähnen (lokal dokumentieren, später synchronisieren): 1
- Severity-Einschätzung fehlt (bei L0 nicht erwartbar): 1
- Keine Warnweste erwähnt trotz unsicherem Bereich: 1
- Keine Priorisierung bei akuter Gefährdung: 1
- Warnweste nicht explizit erwähnt: 1
- Offline-Workflow nur implizit (Foto 'sobald möglich'): 1
- Keine Erwähnung von Leuchtmittel-/Sicherungsprüfung als konkrete Diagnoseschritte: 1
- Severity-Einschätzung fehlt (User erwähnt 'unsicher', aber keine explizite Priorisierung): 1
- Zeitkritische Maßnahmen könnten stärker betont werden: 1
- Severity-Einschätzung fehlt (im CONTEXT nicht vorhanden, daher kein Abzug): 1
- Offline-Workflow nicht erwähnt (connectivity=spotty erfordert lokale Dokumentation): 1
- Batterie-Status bezieht sich auf Techniker-Gerät, nicht Asset (Missverständnis): 1
