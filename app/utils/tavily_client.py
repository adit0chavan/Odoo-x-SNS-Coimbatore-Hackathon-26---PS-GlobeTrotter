import requests
from flask import current_app

class TavilyClient:
    def __init__(self):
        self.api_key = None
        self.base_url = "https://api.tavily.com/search"
    
    def search(self, query, search_depth="basic", max_results=5):
        """Search using Tavily API"""
        if not self.api_key:
            self.api_key = current_app.config.get('TAVILY_API_KEY')
        
        if not self.api_key:
            return {"results": []}
        
        try:
            payload = {
                "api_key": self.api_key,
                "query": query,
                "search_depth": search_depth,
                "max_results": max_results
            }
            
            response = requests.post(self.base_url, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Tavily API error: {e}")
            return {"results": []}
    
    def search_cities(self, query):
        """Search for travel destinations"""
        results = self.search(f"travel destination {query} tourism", max_results=10)
        return self._process_city_results(results)
    
    def search_activities(self, city):
        """Search for activities in a city"""
        results = self.search(f"best things to do in {city} tourist attractions 2026", max_results=15)
        return self._process_activity_results(results)

    def get_itinerary_plan(self, city):
        """Scrape the web for a proper tourist plan/itinerary using Tavily"""
        # Using search_depth="advanced" for better content extraction
        query = f"detailed 3 day travel itinerary for {city} top tourist destinations and hidden gems"
        results = self.search(query, search_depth="advanced", max_results=8)
        
        # We want to process these more carefully
        plans = []
        if 'results' in results:
            for result in results['results']:
                # Filter for results that look like real guides or blogs
                content = result.get('content', '')
                if len(content) > 100: # Ensure it has some substance
                    plans.append({
                        'title': result.get('title', ''),
                        'plan': content,
                        'source': result.get('url', '')
                    })
        return plans

    def _process_city_results(self, results):
        """Process city search results"""
        cities = []
        if 'results' in results:
            for result in results['results']:
                cities.append({
                    'name': result.get('title', ''),
                    'description': result.get('content', ''),
                    'url': result.get('url', '')
                })
        return cities
    
    def _process_activity_results(self, results):
        """Process activity search results"""
        activities = []
        if 'results' in results:
            for result in results['results']:
                activities.append({
                    'name': result.get('title', ''),
                    'description': result.get('content', ''),
                    'url': result.get('url', '')
                })
        return activities

tavily_client = TavilyClient()
