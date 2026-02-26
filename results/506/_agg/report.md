# Aggregation Report (506)
- judge_version filter: **judge_v1_1**
- Tests (latest runs): **90**
- Incidents with any deltas: **30**

## Mean scores by context level (snapshot)
### L0 (n=30)
- mean runtime: 4.751866666666667
- mean R/H/S/D/K: 3.3666666666666667/3.4/3.1/3.6/2.8666666666666667
- mean overall (avg R/H/S/D/K): 3.2666666666666666
- flags (rate): safety_first=0.97, escalation_present=1.00, offline_workflow_mentioned=0.00, hallucination_suspected=0.03
### L2 (n=30)
- mean runtime: 5.138133333333333
- mean R/H/S/D/K: 4.5/4.333333333333333/4.333333333333333/4.233333333333333/3.8
- mean overall (avg R/H/S/D/K): 4.24
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.20, hallucination_suspected=0.03
### L2B (n=30)
- mean runtime: 5.3105
- mean R/H/S/D/K: 4.933333333333334/4.933333333333334/4.533333333333333/4.833333333333333/5.0
- mean overall (avg R/H/S/D/K): 4.846666666666667
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.63, hallucination_suspected=0.00

## Mean scores by strategy (snapshot)
### S0 (n=30)
- mean runtime: 4.751866666666667
- mean R/H/S/D/K: 3.3666666666666667/3.4/3.1/3.6/2.8666666666666667
- mean overall (avg R/H/S/D/K): 3.2666666666666666
### S1 (n=30)
- mean runtime: 5.138133333333333
- mean R/H/S/D/K: 4.5/4.333333333333333/4.333333333333333/4.233333333333333/3.8
- mean overall (avg R/H/S/D/K): 4.24
### S2 (n=30)
- mean runtime: 5.3105
- mean R/H/S/D/K: 4.933333333333334/4.933333333333334/4.533333333333333/4.833333333333333/5.0
- mean overall (avg R/H/S/D/K): 4.846666666666667

## Top missing elements (max 20)
- Kontextnutzung minimal (nur Asset-ID): 3
- Keine Offline-Workflow-Erwähnung (aber nicht erwartbar bei minimalem Context): 2
- Offline-Workflow bei spotty connectivity nicht explizit erwähnt: 2
- Keine Offline-Workflow-Erwähnung (aber nicht erwartbar bei L0_minimal): 2
- Keine Nutzung von Kontext-Signalen (nur Asset-ID vorhanden): 2
- Safety-first nicht als Schritt 1 priorisiert: 1
- Keine Offline-Workflow-Erwähnung (nicht erwartbar bei L0): 1
- Offline-Workflow fehlt trotz connectivity=offline: 1
- Batterie-Diagnose spekulativ (device_state bezieht sich auf Techniker-Gerät, nicht Asset): 1
- Keine Nutzung der Asset-ID im Kontext: 1
- Keine spezifische Lokalisierung: 1
- Generische Antwort ohne Kontextanpassung: 1
- Kein expliziter Hinweis auf vorhandenes Foto nutzen: 1
- Offline-Workflow nicht explizit genannt trotz spotty connectivity: 1
- Offline-Workflow nicht explizit erwähnt trotz spotty connectivity: 1
- Severity/Traffic/Weather nicht adressiert (nicht im Context): 1
- Offline-Workflow fehlt (connectivity=offline, device_state=low_battery im Context): 1
- Keine explizite Anweisung zu lokaler Speicherung/Synchronisation: 1
- Offline-Workflow (Kontext fehlt, daher nicht erwartbar): 1
- Wetter-/Verkehrskontext (nicht im CONTEXT): 1
