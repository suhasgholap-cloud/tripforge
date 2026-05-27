from pydantic import BaseModel, Field
from typing import List, Optional

class TripRequest(BaseModel):
    origin_iata: str = Field("SIN")
    destination_iata: str
    destination_name: str
    interests: List[str]
    stay_duration: int = Field(..., ge=1, le=30)
    travel_date_from: Optional[str] = None

class FlightOption(BaseModel):
    airline: str
    flight_number: str
    duration_minutes: int
    stopovers: int
    price_sgd: float
    cabin_class: str
    departure_time: str
    arrival_time: str

class HotelOption(BaseModel):
    hotel_name: str
    star_rating: int
    nightly_rate_sgd: float
    total_cost_sgd: float
    review_score: float
    review_count: int
    district: str
    amenities: List[str]

class ItinerarySlot(BaseModel):
    time_slot: str
    activity: str
    location_name: str
    latitude: float
    longitude: float
    entry_fee_sgd: float
    transport_mode: str
    transport_note: str
    food_spots: List[str]

class ItineraryDay(BaseModel):
    day_number: int
    geographic_zone: str
    theme: str
    slots: List[ItinerarySlot]

class WeatherSnapshot(BaseModel):
    avg_temp_c: float
    condition: str
    best_time_note: str
    local_events: List[dict]
    monthly_flight_cost_trend: List[dict]

class PackageTier(BaseModel):
    tier: str
    total_price_sgd: float
    score: int
    weather: WeatherSnapshot
    flights: List[FlightOption]
    hotels: List[HotelOption]
    itinerary: List[ItineraryDay]

class TripResponse(BaseModel):
    trip_id: str
    destination: str
    packages: List[PackageTier]
