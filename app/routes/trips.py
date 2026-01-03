from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Trip, Stop, Budget
from datetime import datetime

bp = Blueprint('trips', __name__)

@bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('trips.dashboard'))
    return redirect(url_for('auth.login'))

@bp.route('/dashboard')
@login_required
def dashboard():
    trips = Trip.query.filter_by(user_id=current_user.id).order_by(Trip.created_at.desc()).all()
    return render_template('dashboard.html', trips=trips, now=datetime.now().date())

@bp.route('/trips/create', methods=['GET', 'POST'])
@login_required
def create_trip():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        
        trip = Trip(
            user_id=current_user.id,
            name=name,
            description=description,
            start_date=datetime.strptime(start_date, '%Y-%m-%d').date() if start_date else None,
            end_date=datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else None
        )
        
        db.session.add(trip)
        db.session.commit()
        
        # Create default budget categories
        categories = ['Transport', 'Accommodation', 'Food', 'Activities', 'Shopping', 'Other']
        for category in categories:
            budget = Budget(trip_id=trip.id, category=category, estimated_amount=0, actual_amount=0)
            db.session.add(budget)
        
        db.session.commit()
        
        flash('Trip created successfully!', 'success')
        return redirect(url_for('trips.view_trip', trip_id=trip.id))
    
    return render_template('trips/create.html')

@bp.route('/trips/<int:trip_id>')
@login_required
def view_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    
    if trip.user_id != current_user.id and not trip.is_public:
        flash('You do not have permission to view this trip', 'error')
        return redirect(url_for('trips.dashboard'))
    
    return render_template('trips/view.html', trip=trip)

@bp.route('/trips/<int:trip_id>/timeline')
@login_required
def view_timeline(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    
    if trip.user_id != current_user.id and not trip.is_public:
        flash('You do not have permission to view this trip', 'error')
        return redirect(url_for('trips.dashboard'))
    
    return render_template('trips/timeline.html', trip=trip)

@bp.route('/trips/<int:trip_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    
    if trip.user_id != current_user.id:
        flash('You do not have permission to edit this trip', 'error')
        return redirect(url_for('trips.dashboard'))
    
    if request.method == 'POST':
        trip.name = request.form.get('name')
        trip.description = request.form.get('description')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        
        trip.start_date = datetime.strptime(start_date, '%Y-%m-%d').date() if start_date else None
        trip.end_date = datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else None
        trip.is_public = request.form.get('is_public') == 'on'
        
        db.session.commit()
        flash('Trip updated successfully!', 'success')
        return redirect(url_for('trips.view_trip', trip_id=trip.id))
    
    return render_template('trips/edit.html', trip=trip)

@bp.route('/trips/<int:trip_id>/delete', methods=['POST'])
@login_required
def delete_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    
    if trip.user_id != current_user.id:
        flash('You do not have permission to delete this trip', 'error')
        return redirect(url_for('trips.dashboard'))
    
    db.session.delete(trip)
    db.session.commit()
    flash('Trip deleted successfully!', 'success')
    return redirect(url_for('trips.dashboard'))

@bp.route('/trips/<int:trip_id>/add-stop', methods=['POST'])
@login_required
def add_stop(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    
    if trip.user_id != current_user.id:
        return jsonify({'error': 'Permission denied'}), 403
    
    city = request.form.get('city')
    country = request.form.get('country')
    arrival_date = request.form.get('arrival_date')
    departure_date = request.form.get('departure_date')
    
    order_index = len(trip.stops)
    
    stop = Stop(
        trip_id=trip.id,
        city=city,
        country=country,
        arrival_date=datetime.strptime(arrival_date, '%Y-%m-%d').date() if arrival_date else None,
        departure_date=datetime.strptime(departure_date, '%Y-%m-%d').date() if departure_date else None,
        order_index=order_index
    )
    
    db.session.add(stop)
    db.session.commit()
    
    flash(f'Added {city} to your trip!', 'success')
    return redirect(url_for('trips.view_trip', trip_id=trip.id))

@bp.route('/trips/<int:trip_id>/budget', methods=['GET', 'POST'])
@login_required
def manage_budget(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    
    if trip.user_id != current_user.id:
        flash('You do not have permission to manage this budget', 'error')
        return redirect(url_for('trips.dashboard'))
    
    if request.method == 'POST':
        for budget_item in trip.budget_items:
            estimated = request.form.get(f'estimated_{budget_item.id}')
            actual = request.form.get(f'actual_{budget_item.id}')
            
            if estimated:
                budget_item.estimated_amount = float(estimated)
            if actual:
                budget_item.actual_amount = float(actual)
        
        db.session.commit()
        flash('Budget updated successfully!', 'success')
        return redirect(url_for('trips.view_trip', trip_id=trip.id))
    
    # Prepare chart data
    chart_labels = [item.category for item in trip.budget_items]
    chart_data = [item.estimated_amount or 0 for item in trip.budget_items]
    
    return render_template('trips/budget.html', trip=trip, chart_labels=chart_labels, chart_data=chart_data)

@bp.route('/trips/shared/<int:trip_id>')
def share_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    if not trip.is_public:
        flash('This itinerary is not currently public.', 'error')
        return redirect(url_for('trips.dashboard'))
    return render_template('trips/view.html', trip=trip, is_shared_view=True)

@bp.route('/trips/<int:trip_id>/copy', methods=['POST'])
@login_required
def copy_trip(trip_id):
    original_trip = Trip.query.get_or_404(trip_id)
    if not original_trip.is_public and original_trip.user_id != current_user.id:
        flash('You do not have permission to copy this trip.', 'error')
        return redirect(url_for('trips.dashboard'))
    
    new_trip = Trip(
        user_id=current_user.id,
        name=f"Copy of {original_trip.name}",
        description=original_trip.description,
        start_date=original_trip.start_date,
        end_date=original_trip.end_date,
        cover_photo=original_trip.cover_photo
    )
    db.session.add(new_trip)
    db.session.flush() # Get new_trip.id
    
    for stop in original_trip.stops:
        new_stop = Stop(
            trip_id=new_trip.id,
            city=stop.city,
            country=stop.country,
            arrival_date=stop.arrival_date,
            departure_date=stop.departure_date,
            order_index=stop.order_index
        )
        db.session.add(new_stop)
        db.session.flush()
        
        for activity in stop.activities:
            new_activity = Activity(
                stop_id=new_stop.id,
                name=activity.name,
                description=activity.description,
                category=activity.category,
                estimated_cost=activity.estimated_cost,
                duration=activity.duration,
                date=activity.date
            )
            db.session.add(new_activity)
            
    db.session.commit()
    flash('Itinerary successfully cloned to your collection!', 'success')
    return redirect(url_for('trips.view_trip', trip_id=new_trip.id))

@bp.route('/trips/<int:trip_id>/reorder', methods=['POST'])
@login_required
def reorder_stops(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    if trip.user_id != current_user.id:
        return {"error": "Unauthorized"}, 403
        
    stop_ids = request.json.get('stop_ids', [])
    for index, stop_id in enumerate(stop_ids):
        stop = Stop.query.get(stop_id)
        if stop and stop.trip_id == trip.id:
            stop.order_index = index
            
    db.session.commit()
    return {"status": "success"}

@bp.route('/trips/<int:trip_id>/toggle-public', methods=['POST'])
@login_required
def toggle_public(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    if trip.user_id != current_user.id:
        flash('Permission denied', 'error')
        return redirect(url_for('trips.dashboard'))
        
    trip.is_public = not trip.is_public
    db.session.commit()
    
    status = "Public" if trip.is_public else "Private"
    flash(f"Trip is now {status}", "success")
    return redirect(url_for('trips.view_trip', trip_id=trip.id))

@bp.route('/my-trips')
@login_required
def list_trips():
    trips = Trip.query.filter_by(user_id=current_user.id).order_by(Trip.created_at.desc()).all()
    return render_template('trips/list.html', trips=trips)
