# Aggregation Report (506)
- Tests (latest runs): **90**
- Incidents with any deltas: **30**

## Mean scores by context level
### L0 (n=30)
- mean runtime: 4.692466666666666
- mean R/H/S/D/K: 4.033333333333333/4.033333333333333/3.2/4.033333333333333/4.933333333333334
- flags (rate): safety_first=0.87, escalation_present=1.00, offline_workflow_mentioned=0.00, hallucination_suspected=0.00
### L2 (n=30)
- mean runtime: 5.050299999999999
- mean R/H/S/D/K: 4.933333333333334/4.9/4.566666666666666/4.8/4.1
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.27, hallucination_suspected=0.00
### L2B (n=30)
- mean runtime: 5.413133333333334
- mean R/H/S/D/K: 5.0/5.0/4.666666666666667/5.0/5.0
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.60, hallucination_suspected=0.00

## Mean scores by strategy
### S0 (n=30)
- mean runtime: 4.692466666666666
- mean R/H/S/D/K: 4.033333333333333/4.033333333333333/3.2/4.033333333333333/4.933333333333334
### S1 (n=30)
- mean runtime: 5.050299999999999
- mean R/H/S/D/K: 4.933333333333334/4.9/4.566666666666666/4.8/4.1
### S2 (n=30)
- mean runtime: 5.413133333333334
- mean R/H/S/D/K: 5.0/5.0/4.666666666666667/5.0/5.0

## Top missing elements (max 20)
- Offline-Workflow bei spotty connectivity: 5
- Offline-Workflow nicht explizit ausformuliert (nur 'keine Ferndiagnose möglich'): 2
- Offline-Workflow bei spotty connectivity nicht erwähnt: 2
- Offline-Workflow (lokal dokumentieren, später synchronisieren): 1
- Keine Sicherheitsmaßnahmen für Nacht/schlechte Sicht erwähnt (Kontext fehlt): 1
- Severity-Einschätzung fehlt (nur 'unsicher' erwähnt): 1
- Keine Priorisierung der Eskalation erkennbar: 1
- Offline-Workflow nicht erwähnt (connectivity=offline, device_state=low_battery): 1
- Keine Anweisung zu lokaler Speicherung/Synchronisation: 1
- Offline-Dokumentation nicht explizit betont trotz spotty connectivity: 1
- Keine Erwähnung der Umweltbedingungen (nicht im Context verfügbar): 1
- Severity-Einschätzung fehlt (nur aus User-Text 'unsicher' ableitbar): 1
- Konkrete Absicherungsmaßnahmen bei hoher Verkehrsexposition weniger detailliert: 1
- Keine Erwähnung von Foto-Workflow (photo_available nicht im Context): 1
- Device-State (low_battery) nicht als Geräte-Constraint erklärt: 1
- Keine Anpassung an Umgebungsbedingungen (Zeit/Wetter unbekannt): 1
- Konkrete Sicherheitsmaßnahmen bei Nacht/schlechter Sicht nicht erkennbar (Kontext fehlt): 1
- Severity-Einschätzung fehlt (keine Priorisierung erkennbar): 1
- Zeitliche Dringlichkeit nicht adressiert: 1
- Keine Offline-Workflow-Erwähnung (aber CONTEXT zeigt nur asset_osm, keine connectivity-Info, daher kein Fehler): 1
