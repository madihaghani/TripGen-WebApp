from flask import Flask, request, render_template, redirect, url_for
import pickle

from models.Trip import Trip

infile = open('./data/trips_new.dat', 'rb')
trips = pickle.load(infile)
_all_trips = [trip.__dict__ for trip in trips]


def _get_all_stops(stops):
    _all_stops = list()
    for i, stop in enumerate(stops):
        if i == 0:
            _all_stops.append(stop['start'])
        _all_stops.append(stop['end'])
    return _all_stops


app = Flask(__name__)


# print and add
@app.route('/', methods=['POST', 'GET'])
def index():
    msg = ''
    msg_type = ''
    if not _all_trips:
        msg = 'No trip exist, nothing to display!'
        msg_type = 'warn'
        return render_template('trips.html', trips=_all_trips, msg=msg, msg_type=msg_type)
    if request.method == 'POST':
        new_trip = request.form['add-trip']
        if len(new_trip) == 0:
            msg = "You must enter stop(s) to add new stop(s) on your trip!"
            msg_type = 'warn'
        else:
            new_trip = new_trip.split(",")
            new_places = Trip(*new_trip).details
            _all_trips.append(new_places)
            msg = "New trip added successfully!"
            msg_type = 'success'
    return render_template('trips.html', trips=_all_trips, msg=msg, msg_type=msg_type)


# modify
@app.route('/trip/<int:id>', methods=['POST','GET'])
def trip_details(id):
    trip = None
    for i, trip in enumerate(_all_trips):
        if trip['id'] == id:
            stops = _get_all_stops(trip['details']['stops'])
            if request.method == 'POST':
                new_stop = request.form['add-stop']
                stops = Trip(*stops) + new_stop
                trip = stops.details
                trip['id'] = id
                trip['details']['id'] = id
                _all_trips[i] = trip
                msg = 'Stop added successfully!'
                msg_type = 'success'
                return render_template('trip_details.html', details=trip['details'], stops=trip['details']['stops'],
                                       msg=msg, msg_type=msg_type)
            msg = ''
            return render_template('trip_details.html', details=trip['details'], stops=trip['details']['stops'], msg=msg)
    msg = 'Trip does not exist!'
    msg_type = 'warn'
    return render_template('trips.html', trips=_all_trips, msg=msg, msg_type=msg_type)


# delete
@app.route('/trip_delete/<int:id>')
def trip_delete(id):
    i = None
    for i, trip in enumerate(_all_trips):
        if trip['id'] == id:
            _all_trips.pop(i)
            return redirect(url_for('index'))
    msg = 'Trip does not exist!'
    msg_type = 'warn'
    return render_template('trips.html', trips=_all_trips, msg=msg, msg_type=msg_type)


@app.errorhandler(404)
def handle_404(err):
    return render_template('error_pages/404.html'), 404


@app.errorhandler(500)
def handle_500(err):
    return render_template('error_pages/500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)