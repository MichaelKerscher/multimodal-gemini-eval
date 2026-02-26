# Aggregation Report (506)
- judge_version filter: **judge_v1_1**
- Tests (latest runs): **90**
- Incidents with any deltas: **30**

## Mean scores by context level (snapshot)
### L0 (n=30)
- mean runtime: 4.415233333333333
- mean R/H/S/D/K: 3.466666666666667/3.466666666666667/3.1/3.7/2.7333333333333334
- mean overall (avg R/H/S/D/K): 3.2933333333333334
- flags (rate): safety_first=0.97, escalation_present=1.00, offline_workflow_mentioned=0.00, hallucination_suspected=0.03
### L2 (n=30)
- mean runtime: 5.582
- mean R/H/S/D/K: 4.566666666666666/4.433333333333334/4.333333333333333/4.366666666666666/3.8
- mean overall (avg R/H/S/D/K): 4.3
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.27, hallucination_suspected=0.00
### L2B (n=30)
- mean runtime: 5.592166666666667
- mean R/H/S/D/K: 4.966666666666667/4.966666666666667/4.633333333333334/4.9/4.933333333333334
- mean overall (avg R/H/S/D/K): 4.88
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.73, hallucination_suspected=0.00

## Mean scores by strategy (snapshot)
### S0 (n=30)
- mean runtime: 4.415233333333333
- mean R/H/S/D/K: 3.466666666666667/3.466666666666667/3.1/3.7/2.7333333333333334
- mean overall (avg R/H/S/D/K): 3.2933333333333334
### S1 (n=30)
- mean runtime: 5.582
- mean R/H/S/D/K: 4.566666666666666/4.433333333333334/4.333333333333333/4.366666666666666/3.8
- mean overall (avg R/H/S/D/K): 4.3
### S2 (n=30)
- mean runtime: 5.592166666666667
- mean R/H/S/D/K: 4.966666666666667/4.966666666666667/4.633333333333334/4.9/4.933333333333334
- mean overall (avg R/H/S/D/K): 4.88

## Top missing elements (max 20)
- Keine Nutzung von Kontext-Signalen (nur Asset-ID vorhanden): 3
- Asset-ID explizit im Protokoll: 2
- Keine Priorisierung nach Severity: 2
- Generische Schritte ohne Fallbezug: 2
- Keine Priorisierung nach Severity/Traffic: 2
- Offline-Workflow (Gerät offline, aber nicht erwähnt): 1
- Batterie-Hinweis (device_state fehlt im Context): 1
- Foto-Workflow (photo_available fehlt im Context): 1
- Explizite Stop-Conditions bei Eskalation: 1
- Klarere Priorisierung (Batterie vs. Lampe): 1
- Keine Nutzung von Umgebungs-/Zeitkontext (nicht vorhanden im CONTEXT): 1
- Keine Anpassung an Zeit/Umgebung (nicht erwartbar bei minimalem Kontext): 1
- Kein expliziter Offline-Workflow trotz connectivity=spotty: 1
- Device-State (low_battery) erwähnt, aber nicht als Handlungsanweisung integriert: 1
- Offline-Workflow bei spotty connectivity nicht explizit erwähnt: 1
- Keine Priorisierung bei severity=high erkennbar: 1
- Sicherheitsmaßnahmen nicht als Schritt 1 positioniert: 1
- Offline-Workflow nicht erwähnt trotz connectivity=offline: 1
- Keine explizite Anweisung zur lokalen Datenspeicherung: 1
- Offline-Workflow nicht erwähnt (Kontext zeigt kein connectivity-Signal): 1
