# Aggregation Report (506)
- Tests (latest runs): **90**
- Incidents with any deltas: **30**

## Mean scores by context level
### L0 (n=30)
- mean runtime: 3.5110666666666663
- mean R/H/S/D/K: 3.8666666666666667/3.8666666666666667/3.033333333333333/3.8666666666666667/4.733333333333333
- flags (rate): safety_first=0.90, escalation_present=0.93, offline_workflow_mentioned=0.00, hallucination_suspected=0.00
### L2 (n=30)
- mean runtime: 3.9544333333333332
- mean R/H/S/D/K: 4.433333333333334/4.433333333333334/4.0/4.4/3.6
- flags (rate): safety_first=0.93, escalation_present=0.93, offline_workflow_mentioned=0.17, hallucination_suspected=0.03
### L2B (n=30)
- mean runtime: 4.133766666666667
- mean R/H/S/D/K: 4.733333333333333/4.733333333333333/4.266666666666667/4.733333333333333/4.7
- flags (rate): safety_first=0.93, escalation_present=0.93, offline_workflow_mentioned=0.70, hallucination_suspected=0.00

## Mean scores by strategy
### S0 (n=30)
- mean runtime: 3.5110666666666663
- mean R/H/S/D/K: 3.8666666666666667/3.8666666666666667/3.033333333333333/3.8666666666666667/4.733333333333333
### S1 (n=30)
- mean runtime: 3.9544333333333332
- mean R/H/S/D/K: 4.433333333333334/4.433333333333334/4.0/4.4/3.6
### S2 (n=30)
- mean runtime: 4.133766666666667
- mean R/H/S/D/K: 4.733333333333333/4.733333333333333/4.266666666666667/4.733333333333333/4.7

## Top missing elements (max 20)
- judge_block_missing_fallback: 6
- Offline-Workflow nicht erwähnt trotz connectivity=spotty: 3
- Offline-Workflow bei spotty connectivity: 3
- Keine Offline-Workflow-Erwähnung (aber CONTEXT zeigt keine Offline-Situation): 2
- Severity-Einschätzung fehlt (bei L0 nicht erwartbar): 2
- Offline-Workflow nicht explizit erwähnt (Gerät offline, low_battery): 1
- Keine Umgebungsinformationen verfügbar, daher generisch gehalten: 1
- Offline-Workflow bei spotty connectivity nicht erwähnt: 1
- Keine Erwähnung von Wetter/Sicht (nicht im Context): 1
- Keine Priorisierung bei 'unsicher' (User erwähnt): 1
- Offline-Workflow fehlt (connectivity=spotty): 1
- Severity=high nicht explizit priorisiert: 1
- Keine Erwähnung von Umgebungsbedingungen (nicht im Context verfügbar): 1
- Batterie-Warnung erwähnt, aber keine Handlungsempfehlung dazu: 1
- Offline-Workflow (Gerät offline): 1
- Batteriewechsel-Spekulation (device_state bezieht sich auf Techniker-Gerät, nicht Asset): 1
- Offline-Workflow nur angedeutet, nicht explizit als Constraint formuliert: 1
- Offline-Workflow nicht erwähnt (CONTEXT zeigt connectivity=offline, aber nicht in L0 sichtbar): 1
- Keine explizite Priorisierung der Verkehrssicherheit bei dunklem Abschnitt: 1
- Konkrete Absicherungsmaßnahmen bei Dunkelheit/Verkehrsgefahr unklar: 1
