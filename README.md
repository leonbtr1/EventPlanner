# Event Planner

## Opis

Event planner je web aplikacija za planiranje događaja.  
Administrator ima mogućnost kreiranja, brisanja i pregledavanja događaja, a korisnik se može prijaviti na bilo prijaviti na događaj dok se ne popuni kapacitet
Backend za aplikaciju je napravljen pomoću pythona koristeći biblioteke Flask i Pony.orm, a frontend je napravljen pomoću html-a i CSS-a.

## UseCase dijagram


## Kako pokrenuti aplikaciju

### Pomoću Docker-a

1. **Instalirajte Docker** – može se preko linka: https://docs.docker.com/desktop/setup/install/windows-install/ ako već nije instaliran

2. **Klonirajte repozitorij**:

```bash
git clone https://github.com/leonbtr1/EventPlanner
cd EventPlanner
```

3. **Pokrenite Docker Compose**:

```bash
docker-compose up --build
```

4. **Otvorite aplikaciju**

Aplikacija će biti dostupna na http://localhost:5000
