from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.models import Trip, Stop, Activity, Budget
from app import db
from datetime import datetime, timedelta

bp = Blueprint('community', __name__, url_prefix='/community')

@bp.route('/')
def index():
    # Fetch all public trips, ordered by newest first
    # Optionally exclude current user's trips if we only want others'
    public_trips = Trip.query.filter_by(is_public=True).order_by(Trip.created_at.desc()).all()
    return render_template('community/index.html', trips=public_trips)

@bp.route('/clone/<int:trip_id>', methods=['POST'])
@login_required
def clone_trip(trip_id):
    original_trip = Trip.query.get_or_404(trip_id)
    
    if not original_trip.is_public and original_trip.user_id != current_user.id:
        abort(403)
        
    # Create new trip copy
    new_trip = Trip(
        user_id=current_user.id,
        name=f"Copy of {original_trip.name}",
        description=original_trip.description,
        start_date=datetime.utcnow().date(), # Reset dates to today for planning
        end_date=datetime.utcnow().date() + (original_trip.end_date - original_trip.start_date) if original_trip.start_date and original_trip.end_date else None,
        cover_photo=original_trip.cover_photo,
        is_public=False # Private by default
    )
    db.session.add(new_trip)
    db.session.flush() # get ID
    
    # Clone Stops
    date_offset = new_trip.start_date - original_trip.start_date if original_trip.start_date else timedelta(0)
    
    for stop in original_trip.stops:
        new_stop = Stop(
            trip_id=new_trip.id,
            city=stop.city,
            country=stop.country,
            arrival_date=stop.arrival_date + date_offset if stop.arrival_date else None,
            departure_date=stop.departure_date + date_offset if stop.departure_date else None,
            order_index=stop.order_index
        )
        db.session.add(new_stop)
        db.session.flush()
        
        # Clone Activities
        for activity in stop.activities:
            new_activity = Activity(
                stop_id=new_stop.id,
                name=activity.name,
                description=activity.description,
                category=activity.category,
                estimated_cost=activity.estimated_cost,
                duration=activity.duration,
                date=activity.date + date_offset if activity.date else None
            )
            db.session.add(new_activity)
            
    # Clone Budget Items (Estimated only)
    for budget in original_trip.budget_items:
        new_budget = Budget(
            trip_id=new_trip.id,
            category=budget.category,
            estimated_amount=budget.estimated_amount,
            actual_amount=0 # Reset actuals
        )
        db.session.add(new_budget)
        
    db.session.commit()
    flash(f"Successfully copied '{original_trip.name}' to your trips!", "success")
    return redirect(url_for('trips.view_trip', trip_id=new_trip.id))
