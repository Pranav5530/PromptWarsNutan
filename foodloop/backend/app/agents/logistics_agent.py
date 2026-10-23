import uuid
from typing import List, Dict, Any, Optional
from app.services.maps_service import maps_service
from app.schemas.foodloop import DispatchRecord
from app.rules.matching_rules import haversine_distance_km

DEFAULT_VOLUNTEERS = [
    {
        "id": "vol-rahul-01",
        "name": "Rahul Sharma",
        "phone": "+91-98765-88001",
        "latitude": 12.9730,
        "longitude": 77.5960,
        "transport": "two_wheeler",
        "is_available": True
    },
    {
        "id": "vol-priya-02",
        "name": "Priya Patil",
        "phone": "+91-98765-88002",
        "latitude": 12.9800,
        "longitude": 77.6100,
        "transport": "two_wheeler",
        "is_available": True
    },
    {
        "id": "vol-arjun-03",
        "name": "Arjun Nair",
        "phone": "+91-98765-88003",
        "latitude": 12.9650,
        "longitude": 77.5850,
        "transport": "car",
        "is_available": True
    }
]


class LogisticsAgent:
    """
    Logistics Agent: Assigns the nearest active volunteer and computes navigation
    route and ETA to donor and NGO.
    """
    def __init__(self, volunteers: List[Dict[str, Any]] = None):
        self.volunteers = volunteers or DEFAULT_VOLUNTEERS
        self.maps = maps_service

    async def assign_volunteer(
        self,
        listing_id: str,
        ngo_id: str,
        donor_lat: float,
        donor_lng: float,
        ngo_lat: float,
        ngo_lng: float
    ) -> DispatchRecord:
        # Find closest available volunteer to the donor
        best_vol = None
        min_dist = float("inf")

        for vol in self.volunteers:
            if not vol.get("is_available", True):
                continue
            dist = haversine_distance_km(vol["latitude"], vol["longitude"], donor_lat, donor_lng)
            if dist < min_dist:
                min_dist = dist
                best_vol = vol

        if not best_vol:
            best_vol = self.volunteers[0] # Fallback to first registered volunteer

        # Calculate routing & ETA from donor to NGO destination
        routing = self.maps.calculate_eta_and_route(
            origin_lat=donor_lat,
            origin_lng=donor_lng,
            dest_lat=ngo_lat,
            dest_lng=ngo_lng,
            transport_mode=best_vol["transport"]
        )

        dispatch_id = "disp-" + uuid.uuid4().hex[:8]
        return DispatchRecord(
            dispatch_id=dispatch_id,
            listing_id=listing_id,
            ngo_id=ngo_id,
            volunteer_id=best_vol["id"],
            volunteer_name=best_vol["name"],
            volunteer_phone=best_vol["phone"],
            eta_minutes=routing["eta_minutes"],
            directions_url=routing["directions_url"],
            status="assigned"
        )


logistics_agent = LogisticsAgent()
