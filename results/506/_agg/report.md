# Aggregation Report (506)
- judge_version filter: **judge_v1_1**
- Tests (latest runs): **90**
- Incidents with any deltas: **30**

## Mean scores by context level (snapshot)
### L0 (n=30)
- mean runtime: 5.093533333333334
- mean R/H/S/D/K: 3.5/3.533333333333333/3.2/3.8333333333333335/2.8666666666666667
- mean overall (avg R/H/S/D/K): 3.3866666666666663
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.00, hallucination_suspected=0.03
### L2 (n=30)
- mean runtime: 5.418433333333334
- mean R/H/S/D/K: 4.566666666666666/4.433333333333334/4.366666666666666/4.4/3.8
- mean overall (avg R/H/S/D/K): 4.3133333333333335
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.27, hallucination_suspected=0.07
### L2B (n=30)
- mean runtime: 5.632433333333333
- mean R/H/S/D/K: 4.9/4.866666666666666/4.533333333333333/4.866666666666666/5.0
- mean overall (avg R/H/S/D/K): 4.833333333333333
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.60, hallucination_suspected=0.00

## Mean scores by strategy (snapshot)
### S0 (n=30)
- mean runtime: 5.093533333333334
- mean R/H/S/D/K: 3.5/3.533333333333333/3.2/3.8333333333333335/2.8666666666666667
- mean overall (avg R/H/S/D/K): 3.3866666666666663
### S1 (n=30)
- mean runtime: 5.418433333333334
- mean R/H/S/D/K: 4.566666666666666/4.433333333333334/4.366666666666666/4.4/3.8
- mean overall (avg R/H/S/D/K): 4.3133333333333335
### S2 (n=30)
- mean runtime: 5.632433333333333
- mean R/H/S/D/K: 4.9/4.866666666666666/4.533333333333333/4.866666666666666/5.0
- mean overall (avg R/H/S/D/K): 4.833333333333333

## Top missing elements (max 20)
- Keine Kontextnutzung (nur Asset-ID vorhanden): 3
- Offline-Workflow (spotty connectivity): 2
- Kein expliziter Offline-Workflow trotz connectivity=spotty: 2
- Offline-Workflow nicht erwartbar (kein Signal im Context): 1
- Kontext minimal genutzt (nur Asset-ID übernommen): 1
- Offline-Workflow fehlt (connectivity=offline, device_state=low_battery): 1
- Keine explizite Anweisung zu lokaler Speicherung/Synchronisation: 1
- Keine Nutzung der Asset-ID im Text: 1
- Keine Erwähnung des intermittierenden Charakters: 1
- Standortangabe (GPS/Name) aus CONTEXT nutzen: 1
- Offline-Workflow nicht erwartbar (kein Signal): 1
- Halluzination: 'solar-/akkubetrieben' nicht im CONTEXT: 1
- Keine Priorisierung bei high severity erkennbar: 1
- Offline-Workflow (nicht erwartbar, da kein Signal im Context): 1
- Wetter-/Verkehrskontext (nicht erwartbar): 1
- Offline-Workflow explizit (connectivity=offline): 1
- Keine Spekulation über Asset-Defekt: 1
- Offline-Workflow (lokal dokumentieren/Foto lokal speichern): 1
- Offline-Workflow (kein Signal im CONTEXT): 1
- Keine Priorisierung bei severity=high erkennbar: 1
