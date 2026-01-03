from flask import Blueprint, jsonify, request
from app.utils.tavily_client import tavily_client
from app.utils.location_library import get_popular_destinations

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/search/cities')
def search_cities():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'results': []})
    
    results = tavily_client.search_cities(query)
    return jsonify({'results': results})

@bp.route('/search/activities')
def search_activities():
    city = request.args.get('city', '')
    if not city:
        return jsonify({'results': []})
    
    results = tavily_client.search_activities(city)
    return jsonify({'results': results})

@bp.route('/destinations/popular')
def popular_destinations():
    return jsonify({'results': get_popular_destinations()})

@bp.route('/itinerary/plan')
def get_itinerary():
    city = request.args.get('city', '')
    if not city:
        return jsonify({'results': []})
    
    results = tavily_client.get_itinerary_plan(city)
    return jsonify({'results': results})
