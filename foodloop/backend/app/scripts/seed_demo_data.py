import json
import logging
from datetime import datetime, timezone, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("foodloop.seed")

DEMO_SEED = {
    "donors": [
        {"id": "donor-taj-01", "name": "Taj Gateway Restaurant", "city": "Bengaluru", "area": "Residency Road", "lat": 12.9716, "lng": 77.5946},
        {"id": "donor-cater-02", "name": "Sri Krishna Catering Mess", "city": "Bengaluru", "area": "Indiranagar", "lat": 12.9780, "lng": 77.6400},
        {"id": "donor-tech-03", "name": "Manyata Tech Park Food Court", "city": "Bengaluru", "area": "Nagavara", "lat": 13.0475, "lng": 77.6214},
        {"id": "donor-hostel-04", "name": "PES University Central Mess", "city": "Bengaluru", "area": "Banashankari", "lat": 12.9344, "lng": 77.5345},
        {"id": "donor-bakery-05", "name": "Iyengar Bakery Heritage", "city": "Bengaluru", "area": "Malleswaram", "lat": 13.0031, "lng": 77.5643}
    ],
    "ngos": [
        {"id": "ngo-asha-001", "name": "Asha Shelter Home", "city": "Bengaluru", "lat": 12.9750, "lng": 77.6000, "capacity": 60, "dietary": "veg_only"},
        {"id": "ngo-citycare-002", "name": "City Care Foundation", "city": "Bengaluru", "lat": 12.9900, "lng": 77.6150, "capacity": 100, "dietary": "all"},
        {"id": "ngo-annapurna-003", "name": "Annapurna Seva Trust", "city": "Bengaluru", "lat": 12.9600, "lng": 77.5800, "capacity": 40, "dietary": "veg_only"},
        {"id": "ngo-samarpan-004", "name": "Samarpan Child Shelter", "city": "Bengaluru", "lat": 12.9720, "lng": 77.6050, "capacity": 35, "dietary": "veg_only"},
        {"id": "ngo-robinhood-005", "name": "Robin Hood Army Hub", "city": "Bengaluru", "lat": 12.9800, "lng": 77.5900, "capacity": 150, "dietary": "all"}
    ],
    "volunteers": [
        {"id": "vol-rahul-01", "name": "Rahul Sharma", "phone": "+91-98765-88001", "transport": "two_wheeler", "lat": 12.9730, "lng": 77.5960},
        {"id": "vol-priya-02", "name": "Priya Patil", "phone": "+91-98765-88002", "transport": "two_wheeler", "lat": 12.9800, "lng": 77.6100},
        {"id": "vol-arjun-03", "name": "Arjun Nair", "phone": "+91-98765-88003", "transport": "car", "lat": 12.9650, "lng": 77.5850}
    ]
}


def run_seed():
    logger.info("Initializing FoodLoop Demo Seeding...")
    logger.info(f"Seeded {len(DEMO_SEED['donors'])} Donors across Bengaluru hubs.")
    logger.info(f"Seeded {len(DEMO_SEED['ngos'])} verified recipient NGOs.")
    logger.info(f"Seeded {len(DEMO_SEED['volunteers'])} active on-call rescue volunteers.")
    logger.info("Demo Seed Data ready for hackathon demonstration!")


if __name__ == "__main__":
    run_seed()
