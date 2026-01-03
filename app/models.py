from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))
    profile_pic = db.Column(db.String(255), default='https://via.placeholder.com/150')
    bio = db.Column(db.Text)
    language = db.Column(db.String(10), default='en')
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    trips = db.relationship('Trip', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Trip(db.Model):
    __tablename__ = 'trips'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    cover_photo = db.Column(db.String(255))
    is_public = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    stops = db.relationship('Stop', backref='trip', lazy=True, cascade='all, delete-orphan', order_by='Stop.order_index')
    budget_items = db.relationship('Budget', backref='trip', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Trip {self.name}>'
    
    def get_total_budget(self):
        """Sum of all estimated budget categories."""
        return sum(item.estimated_amount or 0 for item in self.budget_items)
    
    def get_total_actual_cost(self):
        """Sum of all actual budget spending."""
        return sum(item.actual_amount or 0 for item in self.budget_items)

    def get_total_activity_costs(self):
        """Sum of all activity costs in the itinerary."""
        total = 0
        for stop in self.stops:
            for activity in stop.activities:
                total += activity.estimated_cost or 0
        return total

class Stop(db.Model):
    __tablename__ = 'stops'
    
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100))
    arrival_date = db.Column(db.Date)
    departure_date = db.Column(db.Date)
    order_index = db.Column(db.Integer, default=0)
    
    activities = db.relationship('Activity', backref='stop', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Stop {self.city}>'

class Activity(db.Model):
    __tablename__ = 'activities'
    
    id = db.Column(db.Integer, primary_key=True)
    stop_id = db.Column(db.Integer, db.ForeignKey('stops.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    estimated_cost = db.Column(db.Float, default=0.0)
    duration = db.Column(db.Integer)  # in minutes
    date = db.Column(db.Date)
    
    def __repr__(self):
        return f'<Activity {self.name}>'

class Budget(db.Model):
    __tablename__ = 'budget'
    
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    estimated_amount = db.Column(db.Float, default=0.0)
    actual_amount = db.Column(db.Float, default=0.0)
    
    def __repr__(self):
        return f'<Budget {self.category}>'
