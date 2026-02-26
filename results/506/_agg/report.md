# Aggregation Report (506)
- judge_version filter: **judge_v1_1**
- Tests (latest runs): **90**
- Incidents with any deltas: **30**

## Mean scores by context level (snapshot)
### L0 (n=30)
- mean runtime: 4.531733333333333
- mean R/H/S/D/K: 3.6/3.7/3.3333333333333335/3.7/2.9
- mean overall (avg R/H/S/D/K): 3.4466666666666663
- flags (rate): safety_first=0.93, escalation_present=1.00, offline_workflow_mentioned=0.00, hallucination_suspected=0.03
### L2 (n=30)
- mean runtime: 5.4443
- mean R/H/S/D/K: 4.566666666666666/4.533333333333333/4.4/4.533333333333333/4.2
- mean overall (avg R/H/S/D/K): 4.446666666666667
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.37, hallucination_suspected=0.03
### L2B (n=30)
- mean runtime: 5.1534666666666675
- mean R/H/S/D/K: 4.9/4.866666666666666/4.6/4.9/4.966666666666667
- mean overall (avg R/H/S/D/K): 4.846666666666667
- flags (rate): safety_first=1.00, escalation_present=1.00, offline_workflow_mentioned=0.63, hallucination_suspected=0.00

## Mean scores by strategy (snapshot)
### S0 (n=30)
- mean runtime: 4.531733333333333
- mean R/H/S/D/K: 3.6/3.7/3.3333333333333335/3.7/2.9
- mean overall (avg R/H/S/D/K): 3.4466666666666663
### S1 (n=30)
- mean runtime: 5.4443
- mean R/H/S/D/K: 4.566666666666666/4.533333333333333/4.4/4.533333333333333/4.2
- mean overall (avg R/H/S/D/K): 4.446666666666667
### S2 (n=30)
- mean runtime: 5.1534666666666675
- mean R/H/S/D/K: 4.9/4.866666666666666/4.6/4.9/4.966666666666667
- mean overall (avg R/H/S/D/K): 4.846666666666667

## Top missing elements (max 20)
- Offline-Workflow (spotty connectivity): 2
- Offline-Workflow (nicht erwartbar, da connectivity nicht im Context): 2
- Safety-first nicht als Schritt 1 priorisiert: 1
- Keine Offline-Workflow-Erwähnung (nicht erwartbar bei L0): 1
- Eskalationstrigger könnten klarer sein: 1
- Offline-Workflow fehlt trotz connectivity=offline: 1
- Halluzination: 'Gerät meldet niedrigen Batteriestand' als Ursache für Lampenausfall interpretiert: 1
- Kontextnutzung minimal (nur Asset-ID): 1
- Spekuliert über Ampelanlagen ohne Signal: 1
- Keine Anpassung an Umgebung/Zeit/Wetter: 1
- Offline-Workflow explizit (spotty connectivity): 1
- Keine Kontextnutzung (minimaler Context nicht genutzt): 1
- Keine spezifische Priorisierung bei 'unsicher': 1
- Generische Schritte ohne Fallbezug: 1
- Offline-Workflow nicht erwartbar (kein Signal im Context): 1
- Wetter/Traffic-Kontext nicht vorhanden, daher nicht fehlend: 1
- Explizite Erwähnung 'lokal speichern/später synchronisieren' könnte klarer sein: 1
- Lokale Speicherung/Synchronisation: 1
- Kontextnutzung (minimal context, keine spezifischen Signale verarbeitet): 1
- Explizite Priorisierung wegen severity=high könnte stärker sein: 1
