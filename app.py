from flask import Flask, request, render_template, jsonify, url_for
from pony.orm import Database, PrimaryKey, Required, Set, db_session, select
from datetime import datetime

app = Flask(__name__)

# === DATABASE SETUP ===
db = Database()
db.bind(provider='sqlite', filename='eventplanner.sqlite', create_db=True)

class Dogadaj(db.Entity):
    id = PrimaryKey(int, auto=True)
    naziv = Required(str)
    opis = Required(str)
    lokacija = Required(str)
    datum = Required(datetime)
    maksimalno_mjesta = Required(int)
    zauzet = Required(bool, default=False)
    sudionici = Set('Sudionik')

class Sudionik(db.Entity):
    id = PrimaryKey(int, auto=True)
    ime = Required(str)
    prezime = Required(str)
    email = Required(str)
    dogadaj = Required(Dogadaj)

db.generate_mapping(create_tables=True)

# === ROUTES ===

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/dodaj_dogadaj', methods=['POST'])
@db_session
def dodaj_dogadaj():
    data = request.form
    Dogadaj(
        naziv=data['naziv'],
        opis=data['opis'],
        lokacija=data['lokacija'],
        datum=datetime.strptime(data['datum'], '%Y-%m-%d'),
        maksimalno_mjesta=int(data['maksimalno_mjesta']),
        zauzet=False
    )
    return jsonify({'response': 'Događaj dodan'})

@app.route('/prijavi_sudionika', methods=['POST'])
@db_session
def prijavi_sudionika():
    data = request.form
    dogadaj = Dogadaj.get(id=int(data['dogadaj_id']))
    if dogadaj.zauzet:
        return jsonify({'response': 'Događaj je već popunjen'})

    if len(dogadaj.sudionici) >= dogadaj.maksimalno_mjesta:
        dogadaj.zauzet = True
        return jsonify({'response': 'Kapacitet je popunjen'})

    Sudionik(
        ime=data['ime'],
        prezime=data['prezime'],
        email=data['email'],
        dogadaj=dogadaj
    )

    if len(dogadaj.sudionici) + 1 >= dogadaj.maksimalno_mjesta:
        dogadaj.zauzet = True

    return jsonify({'response': 'Prijava uspješna'})

@app.route('/dogadaji', methods=['GET'])
@db_session
def prikazi_dogadaje():
    svi = select(d for d in Dogadaj)[:]
    lista = [{
        'id': d.id,
        'naziv': d.naziv,
        'datum': d.datum.strftime('%Y-%m-%d'),
        'zauzet': d.zauzet
    } for d in svi]
    return jsonify(lista)

@app.route('/sudionici/<int:dogadaj_id>', methods=['GET'])
@db_session
def sudionici_po_dogadaju(dogadaj_id):
    dogadaj = Dogadaj.get(id=dogadaj_id)
    if not dogadaj:
        return jsonify({'error': 'Događaj ne postoji'})
    sudionici = [{
        'ime': s.ime,
        'prezime': s.prezime,
        'email': s.email
    } for s in dogadaj.sudionici]
    return jsonify(sudionici)

# === START ===
if __name__ == '__main__':
    app.run(debug=True, port=5000)
