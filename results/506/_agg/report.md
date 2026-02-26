# Aggregation Report (506)
- judge_version filter: **judge_v1_1**
- Tests (latest runs): **90**
- Incidents with any deltas: **30**

## Mean scores by context level (snapshot)
### L0 (n=30)
- mean runtime: 4.742166666666667
- mean R/H/S/D/K: 3.566666666666667/3.6/3.3/3.8/2.966666666666667
- mean overall (avg R/H/S/D/K): 3.4466666666666668
- flags (rate): safety_first=0.93, escalation_present=1.00, offline_workflow_mentioned=0.00, hallucination_suspected=0.00
### L2 (n=30)
- mean runtime: 5.1729666666666665
- mean R/H/S/D/K: 4.633333333333334/4.533333333333333/4.466666666666667/4.4/3.933333333333333
- mean overall (avg R/H/S/D/K): 4.3933333333333335
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.33, hallucination_suspected=0.03
### L2B (n=30)
- mean runtime: 5.1898333333333335
- mean R/H/S/D/K: 4.933333333333334/4.9/4.7/4.833333333333333/4.966666666666667
- mean overall (avg R/H/S/D/K): 4.866666666666666
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.67, hallucination_suspected=0.00

## Mean scores by strategy (snapshot)
### S0 (n=30)
- mean runtime: 4.742166666666667
- mean R/H/S/D/K: 3.566666666666667/3.6/3.3/3.8/2.966666666666667
- mean overall (avg R/H/S/D/K): 3.4466666666666668
### S1 (n=30)
- mean runtime: 5.1729666666666665
- mean R/H/S/D/K: 4.633333333333334/4.533333333333333/4.466666666666667/4.4/3.933333333333333
- mean overall (avg R/H/S/D/K): 4.3933333333333335
### S2 (n=30)
- mean runtime: 5.1898333333333335
- mean R/H/S/D/K: 4.933333333333334/4.9/4.7/4.833333333333333/4.966666666666667
- mean overall (avg R/H/S/D/K): 4.866666666666666

## Top missing elements (max 20)
- Offline-Workflow explizit (lokal speichern/später sync): 1
- Kein Bezug zu Umgebungsbedingungen (nicht im Kontext): 1
- Keine Nutzung von photo_available (nicht im Kontext): 1
- Generische Antwort ohne spezifische Kontextanpassung: 1
- Offline-Workflow (spotty connectivity): 1
- Klarstellung device_state vs. Asset-Zustand: 1
- Keine Offline-Workflow-Erwähnung (aber nicht erwartbar bei minimalem Context): 1
- Keine explizite Priorisierung bei high severity: 1
- Offline-Workflow fehlt komplett (connectivity=offline im Context): 1
- Keine Erwähnung lokaler Dokumentation/Sync später: 1
- Low_battery des Geräts nicht adressiert: 1
- Offline-Workflow könnte expliziter sein (z.B. 'lokal speichern, später sync'): 1
- Offline-Workflow (Kontext zeigt offline, aber nicht erwähnt): 1
- Wetter/Sicht-Risiko nicht explizit adressiert: 1
- Keine Nutzung von Kontext (nur Asset-ID vorhanden): 1
- Generische Antwort ohne Anpassung an Umgebung: 1
- Fragt nach Asset-Typ, obwohl nicht erwartbar aus Kontext: 1
- Keine explizite Priorisierung bei Nebel/schlechter Sicht: 1
- Stop-Conditions könnten klarer sein: 1
- Keine explizite Nutzung der context_notes (device vs. asset): 1
