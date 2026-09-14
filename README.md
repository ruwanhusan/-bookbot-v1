# Bookbot V1 prototype

Een lokale, werkende prototype-app voor een Nederlandse eenmanszaak.

## Functies
- Dashboard met omzet, kosten, btw en winst
- Factuur/bon uploaden
- Demo-uitlezing van factuurgegevens
- Boekingsvoorstel
- 🟢/🟡/🔴 controlestatus
- Goedkeuren of handmatig aanpassen
- Transactieoverzicht
- Eenvoudige btw-overview
- Fiscale assistent met antwoorden op basis van de prototypegegevens

## Starten

Vereist: Python 3.10+

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open daarna de lokale URL die Streamlit toont.

### Belangrijk
Dit is een prototype. De documentanalyse gebruikt bewust demo-logica; er is nog geen echte OCR/AI-API, bankkoppeling of aangiftefunctionaliteit aangesloten.
