# Aggregation Report (506)
- judge_version filter: **judge_v1_1**
- Tests (latest runs): **90**
- Incidents with any deltas: **30**

## Mean scores by context level (snapshot)
### L0 (n=30)
- mean runtime: 4.624233333333334
- mean R/H/S/D/K: 3.433333333333333/3.433333333333333/3.1666666666666665/3.6/2.933333333333333
- mean overall (avg R/H/S/D/K): 3.3133333333333335
- flags (rate): safety_first=0.93, escalation_present=1.00, offline_workflow_mentioned=0.00, hallucination_suspected=0.00
### L2 (n=30)
- mean runtime: 5.2596333333333325
- mean R/H/S/D/K: 4.633333333333334/4.4/4.5/4.4/3.8666666666666667
- mean overall (avg R/H/S/D/K): 4.36
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.23, hallucination_suspected=0.07
### L2B (n=30)
- mean runtime: 5.527466666666667
- mean R/H/S/D/K: 5.0/4.933333333333334/4.633333333333334/4.833333333333333/5.0
- mean overall (avg R/H/S/D/K): 4.88
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.70, hallucination_suspected=0.00

## Mean scores by strategy (snapshot)
### S0 (n=30)
- mean runtime: 4.624233333333334
- mean R/H/S/D/K: 3.433333333333333/3.433333333333333/3.1666666666666665/3.6/2.933333333333333
- mean overall (avg R/H/S/D/K): 3.3133333333333335
### S1 (n=30)
- mean runtime: 5.2596333333333325
- mean R/H/S/D/K: 4.633333333333334/4.4/4.5/4.4/3.8666666666666667
- mean overall (avg R/H/S/D/K): 4.36
### S2 (n=30)
- mean runtime: 5.527466666666667
- mean R/H/S/D/K: 5.0/4.933333333333334/4.633333333333334/4.833333333333333/5.0
- mean overall (avg R/H/S/D/K): 4.88

## Top missing elements (max 20)
- Offline-Workflow bei spotty connectivity: 3
- Keine Nutzung der Asset-ID im Workflow: 2
- Keine Anpassung an Umgebungsbedingungen (nicht im Context): 2
- Keine Nutzung von Kontext-Signalen (nur Asset-ID vorhanden): 2
- Kontextnutzung minimal (nur Asset-ID): 2
- Safety-first nicht als Schritt 1 priorisiert: 1
- Keine Offline-Workflow-Erwähnung trotz minimalem Kontext: 1
- Offline-Workflow fehlt komplett (connectivity=offline): 1
- Keine Erwähnung lokaler Dokumentation/Sync später: 1
- Generische Rückfrage ohne Kontextbezug: 1
- Dokumentation könnte GPS/Koordinaten explizit erwähnen: 1
- Keine Kontextnutzung erkennbar (minimaler Context): 1
- Keine spezifische Anpassung an Umgebung/Zeit/Gerät: 1
- Offline-Workflow nicht explizit erwähnt trotz spotty connectivity: 1
- Batterie-Hinweis gut, aber device_state bezieht sich auf Techniker-Gerät, nicht Asset: 1
- Kontextnutzung (minimal context, aber keine Anpassung an fehlende Infos): 1
- Offline-Workflow nicht erwähnt (nicht erwartbar bei L0): 1
- Keine explizite Priorisierung bei low_battery (erwähnt, aber nicht als Handlungseinschränkung betont): 1
- Offline-Workflow (lokal speichern/später sync): 1
- Keine Online-Schritte bei connectivity=offline: 1
