# Aggregation Report (506)
- Tests (latest runs): **90**
- Incidents with full L0/L1/L2 for delta: **30**

## Mean scores by context level
### L0 (n=30)
- mean runtime: 4.292433333333333
- mean R/H/S/D/K: 3.9/3.9/3.2333333333333334/3.8666666666666667/4.1
- flags (rate): safety_first=0.97, escalation_present=0.97, offline_workflow_mentioned=0.07, hallucination_suspected=0.00
### L1 (n=30)
- mean runtime: 4.4703333333333335
- mean R/H/S/D/K: 3.9/3.933333333333333/3.3333333333333335/3.6666666666666665/3.9
- flags (rate): safety_first=0.97, escalation_present=0.97, offline_workflow_mentioned=0.07, hallucination_suspected=0.00
### L2 (n=30)
- mean runtime: 4.4863333333333335
- mean R/H/S/D/K: 4.466666666666667/4.533333333333333/3.4/3.933333333333333/4.233333333333333
- flags (rate): safety_first=0.97, escalation_present=0.97, offline_workflow_mentioned=0.30, hallucination_suspected=0.07

## Top missing elements (max 20)
- Ticket-ID-Referenz: 3
- Offline-Workflow nicht erwähnt: 3
- Alle erwarteten Elemente fehlen - Server Error: 3
- photo_available nicht genutzt: 2
- GPS-Koordinaten nicht explizit in Dokumentation erwähnt: 2
- GPS-Koordinaten nicht explizit genutzt: 2
- Keine Nutzung der Asset-ID im Kontext erkennbar: 1
- Unterscheidung Straßenlampe/Ampel wird erfragt statt aus Kontext abgeleitet: 1
- GPS-Koordinaten und Standortname werden nicht erwähnt: 1
- lit=yes wird nicht interpretiert (deutet auf Straßenlampe hin): 1
- Standortspezifische Hinweise fehlen trotz verfügbarer Daten: 1
- Severity=medium und fault_type=intermittent werden nicht explizit adressiert: 1
- Foto verfügbar (photo_available=true) wird nicht erwähnt: 1
- Umgebungsbedingungen (Nebel, schlechte Sicht, Nacht) nicht in Sicherheitshinweise integriert: 1
- severity=high nicht explizit adressiert: 1
- fog/poor_visibility Sicherheitsaspekte unterbelichtet: 1
- Ticket-Nummer/INC-ID fehlt in Dokumentation: 1
- Keine Berücksichtigung von fog/poor_visibility für erhöhte Sicherheitsmaßnahmen: 1
- device_state:low_battery wird erwähnt, aber keine konkrete Handlungsempfehlung: 1
- Severity:low wird nicht reflektiert (Priorisierung fehlt): 1
