from app import create_app, db
from app.models import User, Trip, Stop, Activity, Budget
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    db.create_all()
    
    # Check if correct admin exists
    admin = User.query.filter_by(email='Admin@globe').first()
    if not admin:
        # Check if old admin exists and remove/update
        old_admin = User.query.filter_by(username='admin').first()
        if old_admin:
            db.session.delete(old_admin)
            db.session.commit()
            
        admin = User(username='Admin', email='Admin@globe', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        print("Created secure admin user: Admin@globe")
    else:
        # Ensure password is correct for existing admin
        admin.set_password('admin123')
        admin.is_admin = True
        print("Updated existing admin password to 'admin123'")

    # Check if regular user exists
    user = User.query.filter_by(username='explorer').first()
    if not user:
        user = User(username='explorer', email='explorer@globetrotter.com', full_name="Marco Polo")
        user.set_password('password123')
        user.bio = "Seeking the unknown corners of the world."
        user.profile_pic = "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?ixlib=rb-1.2.1&auto=format&fit=crop&w=634&q=80"
        db.session.add(user)
        print("Created explorer user")
    
    db.session.commit()
    
    # Create a trip for explorer if none
    existing_trip = Trip.query.filter_by(user_id=user.id).first()
    
    if not existing_trip:
        trip = Trip(
            user_id=user.id,
            name="European Summer",
            description="Backpacking through Italy and France.",
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=14),
            is_public=True,
            cover_photo="https://images.unsplash.com/photo-1499678329028-101435549a4e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
        )
        db.session.add(trip)
        db.session.commit()
        
        # Add stops
        stop1 = Stop(trip_id=trip.id, city='Rome', country='Italy', arrival_date=datetime.utcnow(), departure_date=datetime.utcnow() + timedelta(days=3))
        stop2 = Stop(trip_id=trip.id, city='Paris', country='France', arrival_date=datetime.utcnow() + timedelta(days=4), departure_date=datetime.utcnow() + timedelta(days=7))
        db.session.add(stop1)
        db.session.add(stop2)
        db.session.commit()
    else:
        trip = existing_trip

    # Ensure budget items exist for the trip (whether new or existing)
    if not trip.budget_items:
        print("Patching missing budget items for trip...")
        categories = ['Transport', 'Accommodation', 'Food', 'Activities', 'Shopping', 'Other']
        for category in categories:
            # Initialize with 0 as requested ("no default budget")
            budget = Budget(trip_id=trip.id, category=category, estimated_amount=0, actual_amount=0)
            db.session.add(budget)
        db.session.commit()
        print("Budget items added.")
        
        # Add default budget items
        categories = ['Transport', 'Accommodation', 'Food', 'Activities', 'Shopping', 'Other']
        for category in categories:
            # Add some dummy data for the seeded trip
            est = 0
            if category == 'Transport': est = 1500
            elif category == 'Accommodation': est = 2000
            elif category == 'Food': est = 800
            elif category == 'Activities': est = 500
            
            budget = Budget(trip_id=trip.id, category=category, estimated_amount=est, actual_amount=0)
            db.session.add(budget)
        db.session.commit()
        
        print("Created sample trip")

    print("Database seeded successfully.")
