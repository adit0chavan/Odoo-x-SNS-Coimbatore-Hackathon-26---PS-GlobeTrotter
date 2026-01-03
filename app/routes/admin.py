from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from app.models import User, Trip, Stop
from app import db
from functools import wraps

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Strict Admin Check: Only Admin@globe can access admin routes
        if not current_user.is_authenticated or not current_user.is_admin or current_user.email != 'Admin@globe':
            flash('Access denied: Unauthorized access attempt.', 'danger')
            return redirect(url_for('trips.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Gather Platform Metrics
    total_users = User.query.count()
    total_trips = Trip.query.count()
    total_stops = Stop.query.count()
    
    # Get recent users and all users
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    all_users = User.query.order_by(User.created_at.desc()).all()
    
    # Get all trips for management
    all_trips = Trip.query.order_by(Trip.created_at.desc()).all()
    
    # Calculate Financials
    total_estimated_budget = sum(t.get_total_budget() for t in all_trips)
    total_actual_spend = sum(t.get_total_actual_cost() for t in all_trips)
    
    return render_template('admin/dashboard.html', 
                           total_users=total_users, 
                           total_trips=total_trips, 
                           total_stops=total_stops,
                           recent_users=recent_users,
                           all_users=all_users,
                           all_trips=all_trips,
                           total_estimated_budget=total_estimated_budget,
                           total_actual_spend=total_actual_spend)



@bp.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Security Alert: Self-termination is not permitted.', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    username = user.username
    db.session.delete(user)
    db.session.commit()
    flash(f'User {username} and associated data have been permanently removed.', 'success')
    return redirect(url_for('admin.dashboard'))

@bp.route('/trip/<int:trip_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    trip_name = trip.name
    db.session.delete(trip)
    db.session.commit()
    flash(f'Trip "{trip_name}" has been removed from the platform.', 'success')
    return redirect(url_for('admin.dashboard'))
