EventPlanner** je jednostavna web aplikacija za organizaciju događaja i prijavu sudionika. Omogućuje dodavanje događaja, prikaz dostupnih događaja, prijavu sudionika te automatsku provjeru popunjenosti događaja.

Funkcionalnosti

- Dodavanje novih događaja
- Prijava sudionika na događaj
- Automatska provjera kapaciteta
- Oznaka događaja kao "zauzet" kada se popuni
- Pregled svih događaja i sudionika po događaju (API)
- Web sučelje (HTML + CSS)

Tehnologije

- Python 3
- Flask
- PonyORM
- SQLite
- HTML / CSS

🐳 Pokretanje s Dockerom

1. Build Docker image:
bash
docker build -t eventplanner-app .
