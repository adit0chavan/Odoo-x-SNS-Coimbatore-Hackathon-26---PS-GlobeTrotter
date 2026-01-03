# GlobeTrotter - Premium Travel Planning

GlobeTrotter is a modern, feature-rich travel planning application built with Flask, designed for explorers who want a seamless and visually stunning experience. It features a premium Glassmorphism design system, AI-powered recommendations, and advanced budget tracking.

## 🌟 Features Overview

The application implements the following core features as defined in the project scope:

### 1. 🔐 Login / Signup
- **Secure Authentication**: Robust system for user registration and login.
- **Session Management**: Secure session handling with Flask-Login.
- **Form Validation**: Real-time feedback and server-side validation.

### 2. 🏠 Dashboard / Home Screen
- **Central Hub**: Immediate access to upcoming trips and recent activity.
- **Inspiration**: "Top Places" section dynamically fetched to inspire your next journey.
- **Quick Actions**: One-click access to start planning a new trip.

### 3. ✈️ Create Trip
- **Intuitive Wizard**: Simple 3-step process to define trip name, dates, and description.
- **Visuals**: Add cover photos to personalize your trip cards.

### 4. 📂 My Trips (Trip List)
- **Organized Grid**: View all your trips in a responsive grid layout.
- **Quick Stats**: See destination count, dates, and privacy status at a glance.
- **Management**: Easy access to Edit, View, or Delete trips.

### 5. 🗺️ Itinerary Builder
- **Deep Hierarchical Structure**: Trip -> Stops -> Activities.
- **Drag & Drop**: Reorder stops to optimize your route.
- **Stop Management**: Add cities, dates, and notes for each stop.

### 6. 📅 Itinerary View (Timeline)
- **Visual Timeline**: Vertical timeline view to visualize the flow of your journey.
- **Day-by-Day**: Clear breakdown of activities per day.
- **Interactive**: Click to expand details or edit items directly.

### 7. 🏙️ City Search (Destinations)
- **Integrated Discovery**: Search for cities to add to your itinerary.
- **Smart suggestions**: Auto-complete and popular destination recommendations.

### 8. 🎭 Activity Search (AI Powered)
- **AI Recommendation Engine**: "AI Ideas" button fetches activity suggestions (Sightseeing, Food, Adventure) using the **Tavily API**.
- **One-Click Add**: Instantly add suggested activities to your plan.

### 9. 💰 Trip Budget & Cost Breakdown
- **Financial Tracking**: Track Estimated vs. Actual costs for every item.
- **Visual Analytics**: Interactive charts showing spending distribution by category (Transport, Stay, Food, etc.).
- **Currency Support**: Input costs in any currency (normalized to USD for display).

### 10. 🗓️ Trip Calendar
- **Visual Strips**: Trips are displayed as continuous colored strips on a monthly calendar.
- **Planning Aid**: Quickly identify overlapping trips or free weekends.

### 11. 🤝 Shared / Public Itinerary (Community)
- **Community Feed**: Browse trips shared by other users.
- **Privacy Controls**: Toggle trips between **Public** and **Private**.
- **Trip Cloning**: "Copy" any public trip to your own dashboard to use as a template.

### 12. 👤 User Profile
- **Personalization**: Update profile details and view account statistics.
- **Account Management**: Securely manage your account settings.

### 13. 🛡️ Admin Dashboard
- **User Management**: View and manage distinct users.
- **Trip Oversight**: Admin overview of all trips on the platform.
- **Strict Access**: Protected by specific credentials (`Admin@globe` / `admin123`).

---

## 🛠️ Technology Stack

- **Backend**: Python 3, Flask, Flask-Login, Flask-SQLAlchemy
- **Database**: SQLite (Relational DB with foreign key constraints)
- **Frontend**: Jinja2 Templates, Vanilla CSS (Glassmorphism System), JavaScript (ES6)
- **APIs**: Tavily API (for Travel Recommendations)
- **Visualization**: Chart.js

---

## 🗄️ Database Schema

The application uses a relational SQLite database managed via SQLAlchemy ORM.

1.  **User**: Stores auth details, admin status (`is_admin`), and profile info.
    *   *One-to-Many* -> Trips
2.  **Trip**: Core entity containing title, dates, privacy status (`is_public`), and cover photo.
    *   *One-to-Many* -> Stops
    *   *One-to-Many* -> Budget Items
3.  **Stop**: Represents a destination (City/Country) within a trip. Includes `order_index` for correct sequencing.
    *   *One-to-Many* -> Activities
4.  **Activity**: Specific events (Sightseeing, Food, etc.) at a stop.
5.  **Budget**: Tracks financial data per category for a trip.

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- `pip` package manager

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/your-repo/globetrotter.git
cd globetrotter

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Ensure you have a `config.py` file (or set env vars) with:
```python
SECRET_KEY = 'your-secret-key'
TAVILY_API_KEY = 'your-tavily-api-key'
```

### 4. Database Setup
The app will automatically create the DB on first run. To seed initial data (including the Admin account):
```bash
python seed_data.py
```

### 5. Run the Application
```bash
python run.py
```
Visit [http://localhost:5001](http://localhost:5001) in your browser.

---

## 🔒 Security Features
- **Strict Admin Access**: Admin routes are protected by a custom decorator ensuring only `Admin@globe` has access.
- **CSRF Protection**: Flask-WTF integration.
- **Route Guards**: `login_required` decorators on all sensitive endpoints.
- **Data Validation**: Input sanitization on forms.

---

## 📂 Architecture

```
globetrotter/
├── app/
│   ├── routes/          # Blueprints (main, auth, trips, admin, community...)
│   ├── templates/       # Jinja2 HTML Templates (modularized)
│   ├── static/          # CSS (variables, glassmorphism) & JS
│   ├── models.py        # SQLAlchemy Database Models
│   └── __init__.py      # App Factory & Extensions Setup
├── instance/            # SQLite Database file
├── seed_data.py         # Data seeding script
└── run.py               # Application Entry Point
```

---

## 📜 License
MIT License - Created for the Odoo Hackathon 2026.
