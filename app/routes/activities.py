from flask import Blueprint, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Activity, Stop
from datetime import datetime

bp = Blueprint('activities', __name__, url_prefix='/activities')

@bp.route('/stop/<int:stop_id>/add', methods=['POST'])
@login_required
def add_activity(stop_id):
    stop = Stop.query.get_or_404(stop_id)
    
    if stop.trip.user_id != current_user.id:
        flash('Permission denied', 'error')
        return redirect(url_for('trips.dashboard'))
    
    name = request.form.get('name')
    description = request.form.get('description')
    category = request.form.get('category')
    estimated_cost = request.form.get('estimated_cost', 0)
    duration = request.form.get('duration', 0)
    date = request.form.get('date')
    
    activity = Activity(
        stop_id=stop.id,
        name=name,
        description=description,
        category=category,
        estimated_cost=float(estimated_cost) if estimated_cost else 0,
        duration=int(duration) if duration else 0,
        date=datetime.strptime(date, '%Y-%m-%d').date() if date else None
    )
    
    db.session.add(activity)
    db.session.commit()
    
    flash(f'Activity "{name}" added successfully!', 'success')
    return redirect(url_for('trips.view_trip', trip_id=stop.trip_id))

@bp.route('/<int:activity_id>/delete', methods=['POST'])
@login_required
def delete_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    trip_id = activity.stop.trip_id
    
    if activity.stop.trip.user_id != current_user.id:
        flash('Permission denied', 'error')
        return redirect(url_for('trips.dashboard'))
    
    db.session.delete(activity)
    db.session.commit()
    
    flash('Activity deleted successfully!', 'success')
    return redirect(url_for('trips.view_trip', trip_id=trip_id))
