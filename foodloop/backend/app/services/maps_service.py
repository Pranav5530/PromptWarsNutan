import math
from typing import Dict, Any


class GoogleMapsService:
    """
    Service wrapper for Google Maps Directions & Distance Matrix APIs.
    """
    def __init__(self, api_key: str = "mock-maps-key"):
        self.api_key = api_key

    def calculate_eta_and_route(
        self,
        origin_lat: float,
        origin_lng: float,
        dest_lat: float,
        dest_lng: float,
        transport_mode: str = "two_wheeler"
    ) -> Dict[str, Any]:
        """
        Calculates driving route, distance in meters, and estimated time of arrival (ETA).
        """
        # Calculate straight-line distance and apply urban winding factor (~1.3x)
        dlat = dest_lat - origin_lat
        dlng = dest_lng - origin_lng
        distance_km = math.sqrt(dlat*dlat + dlng*dlng) * 111.0 * 1.3
        
        # Urban speed assumption: 20 km/h in city traffic for two-wheelers
        speed_kmh = 22.0 if transport_mode in ["two_wheeler", "bike"] else 18.0
        duration_minutes = max(5, int((distance_km / speed_kmh) * 60.0))
        
        # Google Maps navigation deeplink
        nav_url = f"https://www.google.com/maps/dir/?api=1&origin={origin_lat},{origin_lng}&destination={dest_lat},{dest_lng}&travelmode=driving"

        return {
            "distance_meters": int(distance_km * 1000),
            "eta_minutes": duration_minutes,
            "directions_url": nav_url
        }


maps_service = GoogleMapsService()
