from flask import Flask, render_template, request, redirect, url_for, flash
from pony.orm import db_session, select
from datetime import datetime
import os

from models import db, Event, Registration, bind_and_generate


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
    db_path = os.environ.get('SQLITE_PATH', 'database.sqlite')
    bind_and_generate(db_path)

    @app.route('/')
    @db_session
    def index():
        events = select(e for e in Event).order_by(lambda e: e.date)[:]
        return render_template('index.html', events=events)

    @app.route('/register', methods=['POST'])
    @db_session
    
    
    def register():
        event_id = int(request.form.get('event_id', 0))
        name = (request.form.get('name') or '').strip()
        email = (request.form.get('email') or '').strip()

        event = Event.get(id=event_id)
        if not event:
            flash('Događaj nije pronađen.', 'error')
            return redirect(url_for('index'))

        if len(event.registrations) >= event.capacity:
            flash('Događaj je popunjen.', 'error')
            return redirect(url_for('index'))

        if Registration.get(event=event, attendee_email=email):
            flash('Već ste prijavljeni na ovaj događaj.', 'info')
            return redirect(url_for('index'))

        Registration(attendee_name=name, attendee_email=email, event=event)
        flash('Prijava uspješna', 'success')
        return redirect(url_for('index'))



    @app.route('/admin')
    def admin_redirect():
        return redirect(url_for('admin_events'))

    @app.route('/admin/events')
    @db_session
    def admin_events():
        events = select(e for e in Event).order_by(lambda e: e.date)[:]
        return render_template('admin_events.html', events=events)

    @app.route('/admin/events/new', methods=['POST'])
    @db_session
    def create_event():
        name = (request.form.get('name') or '').strip()
        description = (request.form.get('description') or '').strip()
        date_str = request.form.get('date') or ''  # HTML date input (YYYY-MM-DD)
        capacity = int(request.form.get('capacity') or 0)
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Neispravan datum.', 'error')
            return redirect(url_for('admin_events'))

        Event(name=name, description=description, date=date, capacity=capacity)
        flash('Događaj kreiran.', 'success')
        return redirect(url_for('admin_events'))



    @app.route('/admin/events/<int:event_id>/delete', methods=['POST'])
    @db_session
    def delete_event(event_id):
        event = Event.get(id=event_id)
        if event:
            event.delete()
            flash('Događaj obrisan,', 'success')
        else:
            flash('Događaj nije nađen.', 'error')
        return redirect(url_for('admin_events'))

    return app


app = create_app()


if __name__ == '__main__':
    # Dev server for local testing
    app.run(host='0.0.0.0', port=5000, debug=True)
