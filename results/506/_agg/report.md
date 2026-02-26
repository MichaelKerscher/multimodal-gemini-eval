# Aggregation Report (506)
- judge_version filter: **judge_v1_1**
- Tests (latest runs): **90**
- Incidents with any deltas: **30**

## Mean scores by context level (snapshot)
### L0 (n=30)
- mean runtime: 4.953133333333333
- mean R/H/S/D/K: 3.566666666666667/3.6/3.3666666666666667/3.7333333333333334/2.7
- mean overall (avg R/H/S/D/K): 3.393333333333333
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.00, hallucination_suspected=0.00
### L2 (n=30)
- mean runtime: 5.362766666666667
- mean R/H/S/D/K: 4.5/4.466666666666667/4.466666666666667/4.366666666666666/3.966666666666667
- mean overall (avg R/H/S/D/K): 4.3533333333333335
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.30, hallucination_suspected=0.07
### L2B (n=30)
- mean runtime: 5.7174
- mean R/H/S/D/K: 4.966666666666667/4.9/4.666666666666667/4.966666666666667/5.0
- mean overall (avg R/H/S/D/K): 4.9
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.63, hallucination_suspected=0.00

## Mean scores by strategy (snapshot)
### S0 (n=30)
- mean runtime: 4.953133333333333
- mean R/H/S/D/K: 3.566666666666667/3.6/3.3666666666666667/3.7333333333333334/2.7
- mean overall (avg R/H/S/D/K): 3.393333333333333
### S1 (n=30)
- mean runtime: 5.362766666666667
- mean R/H/S/D/K: 4.5/4.466666666666667/4.466666666666667/4.366666666666666/3.966666666666667
- mean overall (avg R/H/S/D/K): 4.3533333333333335
### S2 (n=30)
- mean runtime: 5.7174
- mean R/H/S/D/K: 4.966666666666667/4.9/4.666666666666667/4.966666666666667/5.0
- mean overall (avg R/H/S/D/K): 4.9

## Top missing elements (max 20)
- Keine Nutzung der Asset-ID im Kontext: 2
- Offline-Workflow (Gerät offline, aber nicht erwähnt): 1
- Kontextnutzung minimal (nur Asset-ID genutzt): 1
- Offline-Workflow nur angedeutet ('Prüfen, ob Verbindung wiederhergestellt werden kann'), nicht als klare Handlungsanweisung: 1
- Kontext-Nutzung (nur OSM-ID vorhanden, keine Umwelt-/Geräte-Infos genutzt): 1
- Spezifische Diagnose für intermittent fault (generisch gehalten): 1
- Explizite Erwähnung photo_available im Workflow (nur 'Foto-Dokumentation nutzen' generisch): 1
- Kein Hinweis auf reporter=patrol (könnte Rückfrage erleichtern): 1
- Kein Hinweis auf Offline-Workflow trotz minimalem Kontext: 1
- Keine Nutzung von GPS-Koordinaten (nicht im CONTEXT vorhanden): 1
- Offline-Workflow nicht explizit erwähnt trotz spotty connectivity: 1
- Batterie-Interpretation spekulativ (solar/akku nicht im CONTEXT): 1
- Keine Nutzung von Kontext (nur Asset-ID vorhanden): 1
- Offline-Workflow nicht erwähnt (aber auch nicht erwartbar bei minimalem Kontext): 1
- Offline-Workflow bei spotty connectivity nicht explizit erwähnt (lokal dokumentieren/später sync): 1
- Offline-Workflow explizit (spotty connectivity): 1
- Offline-Workflow (connectivity=offline nicht erkannt/genutzt): 1
- Kontext-Signale (weather=rain, time_of_day, traffic) nicht sichtbar integriert: 1
- Explizite Offline-Sync-Erwähnung könnte klarer sein: 1
- severity/traffic context not used (minimal context given): 1
