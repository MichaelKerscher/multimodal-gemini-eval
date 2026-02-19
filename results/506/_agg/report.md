# Aggregation Report (506)
- Tests (latest runs): **90**
- Incidents with any deltas: **30**

## Mean scores by context level
### L0 (n=30)
- mean runtime: 4.8767
- mean R/H/S/D/K: 4.033333333333333/4.033333333333333/3.1666666666666665/4.033333333333333/4.866666666666666
- flags (rate): safety_first=0.90, escalation_present=1.00, offline_workflow_mentioned=0.00, hallucination_suspected=0.00
### L2 (n=30)
- mean runtime: 5.533066666666667
- mean R/H/S/D/K: 5.0/5.0/4.633333333333334/4.966666666666667/4.3
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.33, hallucination_suspected=0.03
### L2B (n=30)
- mean runtime: 5.552933333333333
- mean R/H/S/D/K: 5.0/5.0/4.633333333333334/4.966666666666667/5.0
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.63, hallucination_suspected=0.00

## Mean scores by strategy
### S0 (n=30)
- mean runtime: 4.8767
- mean R/H/S/D/K: 4.033333333333333/4.033333333333333/3.1666666666666665/4.033333333333333/4.866666666666666
### S1 (n=30)
- mean runtime: 5.533066666666667
- mean R/H/S/D/K: 5.0/5.0/4.633333333333334/4.966666666666667/4.3
### S2 (n=30)
- mean runtime: 5.552933333333333
- mean R/H/S/D/K: 5.0/5.0/4.633333333333334/4.966666666666667/5.0

## Top missing elements (max 20)
- Offline-Workflow bei spotty connectivity: 4
- Offline-Workflow (lokal dokumentieren/Foto lokal speichern): 1
- Keine Online-Schritte bei connectivity=offline: 1
- Keine Umgebungsinformationen verfügbar, daher keine spezifischen Sicherheitshinweise für Nacht/Nebel: 1
- Severity-Einschätzung fehlt (nur 'unsicher' vom User, keine Priorisierung): 1
- Offline-Workflow nicht erwähnt (connectivity=offline, device_state=low_battery): 1
- Offline-Workflow nur erwähnt ('Keine Ferndiagnose möglich'), aber nicht operativ ausgearbeitet (lokale Speicherung, spätere Synchronisation): 1
- Keine Berücksichtigung der Umgebungsbedingungen (nicht im Context verfügbar): 1
- Offline-Workflow bei spotty connectivity nicht erwähnt: 1
- Konkrete Absicherungsmaßnahmen (Warnweste, Warnblinkanlage) fehlen bei 'unsicher' + minimal Context: 1
- Keine Erwähnung von Dämmerung/schlechter Sicht trotz plausiblem Kontext 'dunkler Abschnitt': 1
- Konkrete Sicherheitsmaßnahmen bei Nacht/schlechter Sicht nicht erkennbar: 1
- Konkrete Sicherheitsmaßnahmen (Warnweste, Absicherung) nicht explizit genannt: 1
- Keine Berücksichtigung der Nachtsituation (nur minimal Context): 1
- Severity-Einschätzung fehlt (bei L0 nicht erwartbar): 1
- Severity-Einschätzung fehlt (nur aus User-Text 'unsicher' ableitbar): 1
- Offline-Workflow (lokal dokumentieren/später synchronisieren): 1
- Konkrete Zeitangabe (20 Min) nicht aufgegriffen: 1
- Keine Priorisierung wegen 'Bereich wirkt unsicher': 1
- Keine Offline-Workflow-Erwähnung (aber CONTEXT zeigt kein connectivity-Problem, daher kein Fehler): 1
