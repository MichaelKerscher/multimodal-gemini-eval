# Aggregation Report (506)
- judge_version filter: **judge_v1_1**
- Tests (latest runs): **90**
- Incidents with any deltas: **30**

## Mean scores by context level (snapshot)
### L0 (n=30)
- mean runtime: 4.979933333333333
- mean R/H/S/D/K: 3.533333333333333/3.566666666666667/3.1333333333333333/3.6666666666666665/2.7
- mean overall (avg R/H/S/D/K): 3.32
- flags (rate): safety_first=0.97, escalation_present=1.00, offline_workflow_mentioned=0.00, hallucination_suspected=0.00
### L2 (n=30)
- mean runtime: 5.688833333333333
- mean R/H/S/D/K: 4.566666666666666/4.4/4.333333333333333/4.233333333333333/3.933333333333333
- mean overall (avg R/H/S/D/K): 4.293333333333334
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.27, hallucination_suspected=0.03
### L2B (n=30)
- mean runtime: 5.3857333333333335
- mean R/H/S/D/K: 4.933333333333334/4.9/4.6/4.733333333333333/4.966666666666667
- mean overall (avg R/H/S/D/K): 4.826666666666667
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.67, hallucination_suspected=0.00

## Mean scores by strategy (snapshot)
### S0 (n=30)
- mean runtime: 4.979933333333333
- mean R/H/S/D/K: 3.533333333333333/3.566666666666667/3.1333333333333333/3.6666666666666665/2.7
- mean overall (avg R/H/S/D/K): 3.32
### S1 (n=30)
- mean runtime: 5.688833333333333
- mean R/H/S/D/K: 4.566666666666666/4.4/4.333333333333333/4.233333333333333/3.933333333333333
- mean overall (avg R/H/S/D/K): 4.293333333333334
### S2 (n=30)
- mean runtime: 5.3857333333333335
- mean R/H/S/D/K: 4.933333333333334/4.9/4.6/4.733333333333333/4.966666666666667
- mean overall (avg R/H/S/D/K): 4.826666666666667

## Top missing elements (max 20)
- Offline-Workflow nicht explizit erwähnt trotz spotty connectivity: 2
- Keine Nutzung der Asset-ID im Kontext: 2
- Keine Offline-Workflow-Erwähnung trotz minimalem Kontext: 2
- Keine Offline-Workflow-Erwähnung (aber nicht erwartbar bei L0_minimal): 2
- Offline-Workflow bei spotty connectivity: 2
- GPS-Koordinaten explizit dokumentieren: 2
- Offline-Workflow (nicht erwartbar, da connectivity nicht im Context): 2
- Offline-Workflow nicht erwähnt (Kontext zeigt nur asset_osm, keine device-Infos): 1
- Keine Nutzung von Standort/Verkehrsexposition (nicht im Kontext): 1
- Keine Foto-Workflow-Hinweise (nicht im Kontext): 1
- Offline-Workflow fehlt komplett (connectivity=offline erfordert lokale Dokumentation/Sync-Hinweis): 1
- Missverständnis: low_battery/offline als Asset-Problem interpretiert statt Techniker-Gerät: 1
- Keine Nutzung von Kontext (nur Asset-ID vorhanden): 1
- Generische Antwort ohne Fallbezug zu intermittent fault: 1
- Keine Priorisierung auf Reproduktion des Fehlers: 1
- Keine explizite Erwähnung von 'intermittent' als Diagnose-Fokus: 1
- Foto-Workflow könnte klarer sein (photo_available=true): 1
- Kontextnutzung minimal (nur Asset-ID): 1
- Keine Anpassung an Umgebungsbedingungen: 1
- Keine Berücksichtigung von Geräte-/Konnektivitätsstatus: 1
