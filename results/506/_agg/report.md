# Aggregation Report (506)
- judge_version filter: **judge_v1_1**
- Tests (latest runs): **90**
- Incidents with any deltas: **30**

## Mean scores by context level (snapshot)
### L0 (n=30)
- mean runtime: 4.5822666666666665
- mean R/H/S/D/K: 3.466666666666667/3.466666666666667/3.2666666666666666/3.6666666666666665/2.7
- mean overall (avg R/H/S/D/K): 3.3133333333333335
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.00, hallucination_suspected=0.00
### L2 (n=30)
- mean runtime: 5.420066666666667
- mean R/H/S/D/K: 4.566666666666666/4.433333333333334/4.466666666666667/4.3/3.8666666666666667
- mean overall (avg R/H/S/D/K): 4.326666666666667
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.30, hallucination_suspected=0.00
### L2B (n=30)
- mean runtime: 5.446466666666667
- mean R/H/S/D/K: 4.966666666666667/4.966666666666667/4.733333333333333/4.866666666666666/4.966666666666667
- mean overall (avg R/H/S/D/K): 4.9
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.70, hallucination_suspected=0.00

## Mean scores by strategy (snapshot)
### S0 (n=30)
- mean runtime: 4.5822666666666665
- mean R/H/S/D/K: 3.466666666666667/3.466666666666667/3.2666666666666666/3.6666666666666665/2.7
- mean overall (avg R/H/S/D/K): 3.3133333333333335
### S1 (n=30)
- mean runtime: 5.420066666666667
- mean R/H/S/D/K: 4.566666666666666/4.433333333333334/4.466666666666667/4.3/3.8666666666666667
- mean overall (avg R/H/S/D/K): 4.326666666666667
### S2 (n=30)
- mean runtime: 5.446466666666667
- mean R/H/S/D/K: 4.966666666666667/4.966666666666667/4.733333333333333/4.866666666666666/4.966666666666667
- mean overall (avg R/H/S/D/K): 4.9

## Top missing elements (max 20)
- Keine klare Stop-Condition vor Eskalation: 2
- Offline-Workflow (connectivity=offline): 2
- Keine Nutzung der Asset-ID im Kontext: 2
- Generische Schritte ohne Kontextanpassung: 2
- Offline-Workflow bei spotty connectivity nicht explizit erwähnt: 2
- Offline-Workflow (nicht erwartbar, da CONTEXT minimal): 1
- Spezifische Standort-/Umgebungsdetails (nicht im CONTEXT): 1
- Expliziter Offline-Workflow (lokal dokumentieren/synchronisieren): 1
- Foto-Workflow-Hinweis (photo_available=true nicht genutzt): 1
- Keine Offline-Workflow-Erwähnung (nicht erwartbar bei minimalem Context): 1
- Keine Nutzung von Geo-Koordinaten (nicht im Context vorhanden): 1
- Offline-Workflow nur implizit ('Notiz machen'), nicht explizit als Sync-Strategie: 1
- Keine explizite GPS-Koordinaten-Dokumentation trotz Verfügbarkeit: 1
- Keine Offline-Workflow-Erwähnung (aber nicht erwartbar bei minimalem Context): 1
- Keine explizite Priorisierung bei high severity: 1
- Kein expliziter Offline-Workflow trotz spotty connectivity: 1
- Keine Offline-Workflow-Hinweise (aber nicht erwartbar bei L0_minimal): 1
- Keine explizite Priorisierung nach Severity/Traffic: 1
- Offline-Workflow fehlt komplett (connectivity=offline, device_state=low_battery): 1
- Keine Anweisung zu lokaler Speicherung/Synchronisation: 1
