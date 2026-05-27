import asyncio
from typing import List, Dict
from app.models.schemas import ItineraryDay, ItinerarySlot
from app.external.geo_client import STATIC_ATTRACTIONS
from app.config import get_settings

cfg = get_settings()

TRANSPORT = {
    'luxury': {'day': 'Private Grab', 'note': 'Pre-book via Grab Premium app.'},
    'value':  {'day': 'Grab / Bus',   'note': 'Grab or local bus via Google Maps.'},
    'budget': {'day': 'Bus / Walk',   'note': 'Use local bus. ~S.50 per ride.'},
}

SLOTS = ['morning', 'afternoon', 'evening', 'night']
EMOJI = {'morning': '🌅', 'afternoon': '☀️', 'evening': '🌆', 'night': '🌙'}

class ItineraryBuilder:
    def __init__(self, destination, interests, stay_duration, tiers):
        self.dest = destination
        self.interests = interests
        self.days = stay_duration
        self.tiers = tiers

    async def build_all(self):
        lux, val, bud = await asyncio.gather(
            self._build('luxury'), self._build('value'), self._build('budget'))
        return {'luxury': lux, 'value': val, 'budget': bud}

    async def _build(self, tier_name) -> List[ItineraryDay]:
        pois = STATIC_ATTRACTIONS.get(self.dest, [])
        transport = TRANSPORT[tier_name]
        itinerary = []
        chunk = max(1, len(pois) // self.days)
        for day in range(1, self.days + 1):
            day_pois = pois[(day-1)*chunk : day*chunk] or pois[:2]
            slots = []
            for i, slot in enumerate(SLOTS):
                poi = day_pois[i % len(day_pois)]
                slots.append(ItinerarySlot(
                    time_slot=slot,
                    activity=poi.get('name', 'Local exploration'),
                    location_name=poi.get('name', ''),
                    latitude=float(poi.get('lat', 0)),
                    longitude=float(poi.get('lon', 0)),
                    entry_fee_sgd=float(poi.get('entry_fee_sgd', 0)),
                    transport_mode=transport['day'],
                    transport_note=transport['note'],
                    food_spots=[],
                ))
            itinerary.append(ItineraryDay(
                day_number=day,
                geographic_zone=poi.get('name', 'City Centre'),
                theme='Local Exploration',
                slots=slots,
            ))
        return itinerary
