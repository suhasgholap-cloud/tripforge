# ============================================================
# TripForge FastAPI Backend
# Structure:
#   app/
#   ├── main.py
#   ├── models/         (Pydantic schemas)
#   ├── services/       (orchestrator, optimizer, itinerary, weather)
#   ├── db/             (PostgreSQL + Redis)
#   ├── external/       (Amadeus, Hotels, Weather APIs)
#   └── utils/          (PDF gen, Maps export)
# ============================================================

# ── main.py ─────────────────────────────────────────────────
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import TripRequest, TripResponse
from app.services.orchestrator import TripOrchestrator
from app.db.cache import get_cached_packages, store_packages
from app.utils.pdf_generator import generate_pdf
from app.utils.maps_export import build_kml_export
import hashlib, json

app = FastAPI(title="TripForge API", version="1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

ALLOWED_DESTINATIONS = {
    "HAN": "Hanoi", "BKK": "Bangkok", "DPS": "Bali",
    "NRT": "Tokyo", "MEL": "Melbourne"
}

@app.post("/api/v1/trip/plan", response_model=TripResponse)
async def plan_trip(req: TripRequest, bg: BackgroundTasks):
    if req.destination_iata not in ALLOWED_DESTINATIONS:
        raise HTTPException(400, f"Destination must be one of: {list(ALLOWED_DESTINATIONS.keys())}")

    cache_key = _make_cache_key(req)
    cached = await get_cached_packages(cache_key)
    if cached:
        return cached

    orch = TripOrchestrator(req)
    packages = await orch.run()                    # fan-out to all services
    bg.add_task(store_packages, cache_key, packages)
    return packages

@app.post("/api/v1/trip/{trip_id}/export/pdf")
async def export_pdf(trip_id: str, tier: str):
    pkg = await get_cached_packages(trip_id)
    if not pkg:
        raise HTTPException(404, "Trip not found or expired")
    url = await generate_pdf(pkg, tier)
    return {"pdf_url": url}

@app.post("/api/v1/trip/{trip_id}/export/maps")
async def export_maps(trip_id: str, tier: str):
    pkg = await get_cached_packages(trip_id)
    kml = await build_kml_export(pkg, tier)        # returns KML string or GCS URL
    return {"kml": kml, "google_maps_url": f"https://www.google.com/maps/d/import?format=kml&url={kml}"}

@app.get("/health")
async def health_check():
    from app.db.cache import ping_cache
    cache_ok = await ping_cache()
    return {
        "status":      "ok",
        "environment": "production",
        "cache":       "ok" if cache_ok else "unavailable",
        "version":     "1.0.0",
    }

def _make_cache_key(req: TripRequest) -> str:
    payload = f"{req.origin_iata}:{req.destination_iata}:{req.stay_duration}:{sorted(req.interests)}"
    return hashlib.sha256(payload.encode()).hexdigest()[:24]


# ── models/schemas.py ────────────────────────────────────────
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class InterestType(str, Enum):
    sightseeing = "sightseeing"
    museums = "museums"
    beaches = "beaches"
    food = "food"
    shopping = "shopping"

class TripRequest(BaseModel):
    origin_iata: str = Field("SIN", description="Origin airport IATA code")
    destination_iata: str
    destination_name: str
    interests: List[InterestType]
    stay_duration: int = Field(..., ge=1, le=30)
    travel_date_from: Optional[str] = None  # ISO date

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
    name: str
    star_rating: int
    nightly_rate_sgd: float
    total_cost_sgd: float
    review_score: float
    review_count: int
    district: str
    amenities: List[str]

class ItinerarySlot(BaseModel):
    time_slot: str          # "morning" | "afternoon" | "evening" | "night"
    activity: str
    location_name: str
    latitude: float
    longitude: float
    entry_fee_sgd: float
    transport_mode: str     # "taxi" | "grab" | "bus" | "walk" | "tuk-tuk"
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
    monthly_flight_cost_trend: List[dict]  # [{month, avg_price_sgd}]

class PackageTier(BaseModel):
    tier: str               # "luxury" | "value" | "budget"
    total_price_sgd: float
    score: int
    weather: WeatherSnapshot
    flights: List[FlightOption]
    hotels: List[HotelOption]
    itinerary: List[ItineraryDay]

class TripResponse(BaseModel):
    trip_id: str
    destination: str
    packages: List[PackageTier]  # always 3 items: luxury, value, budget


# ── services/orchestrator.py ─────────────────────────────────
import asyncio
from app.services.optimizer import PackageOptimizer
from app.services.itinerary_builder import ItineraryBuilder
from app.services.weather_service import WeatherService
from app.external.amadeus_client import fetch_flights
from app.external.hotels_client import fetch_hotels

class TripOrchestrator:
    def __init__(self, req):
        self.req = req

    async def run(self):
        # Fan-out: fetch all raw data concurrently
        flights, hotels, weather = await asyncio.gather(
            fetch_flights(self.req.origin_iata, self.req.destination_iata,
                          self.req.travel_date_from, self.req.stay_duration),
            fetch_hotels(self.req.destination_iata, self.req.stay_duration),
            WeatherService(self.req.destination_iata).fetch()
        )

        optimizer = PackageOptimizer(flights, hotels, self.req.stay_duration)
        tiers = optimizer.build_tiers()           # returns {luxury, value, budget}

        builder = ItineraryBuilder(
            destination=self.req.destination_iata,
            interests=self.req.interests,
            stay_duration=self.req.stay_duration,
            tiers=tiers
        )
        itineraries = await builder.build_all()   # geo-clustered, time-aware

        return self._assemble(tiers, itineraries, weather)

    def _assemble(self, tiers, itineraries, weather):
        from app.models.schemas import TripResponse, PackageTier
        import uuid
        packages = []
        for tier_name in ["luxury", "value", "budget"]:
            t = tiers[tier_name]
            packages.append(PackageTier(
                tier=tier_name,
                total_price_sgd=t["flight"].price_sgd * 2 + t["hotel"].total_cost_sgd,
                score=t["score"],
                weather=weather,
                flights=[t["flight"]],
                hotels=[t["hotel"]],
                itinerary=itineraries[tier_name]
            ))
        return TripResponse(
            trip_id=str(uuid.uuid4())[:8],
            destination=self.req.destination_name,
            packages=packages
        )


# ── services/optimizer.py ────────────────────────────────────
"""
Core scoring algorithm. Each candidate (flight + hotel pair) is
scored across three dimensions: price, quality, and speed.
Tier thresholds select the best candidate per tier.
"""
from dataclasses import dataclass
from typing import List
import statistics

WEIGHTS = {
    "luxury":  {"price": 0.20, "quality": 0.55, "speed": 0.25},
    "value":   {"price": 0.45, "quality": 0.40, "speed": 0.15},
    "budget":  {"price": 0.75, "quality": 0.20, "speed": 0.05},
}

class PackageOptimizer:
    def __init__(self, flights, hotels, nights: int):
        self.flights = flights
        self.hotels = hotels
        self.nights = nights

    def build_tiers(self) -> dict:
        candidates = self._score_all_candidates()
        return {
            "luxury": self._pick(candidates, "luxury"),
            "value":  self._pick(candidates, "value"),
            "budget": self._pick(candidates, "budget"),
        }

    def _score_all_candidates(self):
        all_prices   = [f.price_sgd * 2 + h.total_cost_sgd
                        for f in self.flights for h in self.hotels]
        all_quality  = [h.review_score for h in self.hotels]
        all_duration = [f.duration_minutes for f in self.flights]

        p_min, p_max = min(all_prices), max(all_prices)
        q_min, q_max = min(all_quality), max(all_quality)
        d_min, d_max = min(all_duration), max(all_duration)

        candidates = []
        for f in self.flights:
            for h in self.hotels:
                total = f.price_sgd * 2 + h.total_cost_sgd
                scores = {
                    "price":   1 - _norm(total, p_min, p_max),   # lower = better
                    "quality": _norm(h.review_score, q_min, q_max),
                    "speed":   1 - _norm(f.duration_minutes, d_min, d_max),
                }
                candidates.append({"flight": f, "hotel": h, "scores": scores, "total": total})
        return candidates

    def _pick(self, candidates, tier):
        w = WEIGHTS[tier]
        star_min, star_max = self._star_range(tier)
        eligible = [c for c in candidates
                    if star_min <= c["hotel"].star_rating <= star_max]
        if not eligible:
            eligible = candidates  # fallback: no star constraint

        scored = sorted(eligible,
            key=lambda c: sum(c["scores"][k] * v for k, v in w.items()),
            reverse=True)
        best = scored[0]
        best["score"] = int(sum(best["scores"][k] * v for k, v in w.items()) * 100)
        return best

    @staticmethod
    def _star_range(tier):
        return {"luxury": (4, 5), "value": (3, 4), "budget": (2, 3)}[tier]

def _norm(val, lo, hi):
    return (val - lo) / (hi - lo) if hi != lo else 0.5


# ── services/itinerary_builder.py ────────────────────────────
"""
Geo-cluster itinerary: groups attractions into geographic zones
per day so travellers minimise back-tracking. Flight arrival/
departure times anchor Day 1 morning and final Day evening.
"""
from app.external.claude_client import ask_claude_for_slots
from app.external.maps_client import cluster_by_district

class ItineraryBuilder:
    def __init__(self, destination, interests, stay_duration, tiers):
        self.dest = destination
        self.interests = interests
        self.days = stay_duration
        self.tiers = tiers

    async def build_all(self):
        import asyncio
        lux, val, bud = await asyncio.gather(
            self._build_tier("luxury"),
            self._build_tier("value"),
            self._build_tier("budget"),
        )
        return {"luxury": lux, "value": val, "budget": bud}

    async def _build_tier(self, tier_name):
        flight = self.tiers[tier_name]["flight"]
        transport_pref = "private taxi / Grab" if tier_name == "luxury" else \
                         "Grab / local bus"    if tier_name == "value" else \
                         "public bus / walking"

        # Claude LLM generates culturally-accurate slot content
        prompt = self._build_prompt(tier_name, transport_pref, flight)
        raw = await ask_claude_for_slots(prompt)

        # Geo-cluster: group attractions by district per day
        clustered = cluster_by_district(raw["days"], self.days)
        return clustered

    def _build_prompt(self, tier, transport, flight):
        return f"""
You are a local travel expert for {self.dest}.
Generate a {self.days}-day itinerary for interests: {self.interests}.
Tier: {tier}. Transport preference: {transport}.
Flight arrives: {flight.arrival_time} on Day 1.
Flight departs: Day {self.days} evening — keep Day {self.days} activities near airport.

Rules:
- Split each day: morning / afternoon / evening / night
- Group activities in the SAME geographic district per day (minimize transit)
- Include entry fees in SGD (0 if free)
- Include 1-2 local food spots per day matching interests
- Return JSON: {{days: [{{day_number, geographic_zone, theme, slots: [...]}}]}}
"""


# ── external/claude_client.py ────────────────────────────────
import httpx, json

async def ask_claude_for_slots(prompt: str) -> dict:
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={"x-api-key": "ANTHROPIC_API_KEY",
                     "anthropic-version": "2023-06-01",
                     "content-type": "application/json"},
            json={"model": "claude-sonnet-4-20250514",
                  "max_tokens": 4096,
                  "messages": [{"role": "user", "content": prompt}]}
        )
        raw = r.json()["content"][0]["text"]
        clean = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(clean)


# ── db/cache.py ─────────────────────────────────────────────
import redis.asyncio as redis, json, os
from app.db.postgres import get_db

r = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
TTL_SECONDS = 60 * 60 * 6  # 6-hour cache

async def get_cached_packages(key: str):
    val = await r.get(f"pkg:{key}")
    if val:
        return json.loads(val)
    # fallback: check PostgreSQL for non-expired rows
    async with get_db() as db:
        row = await db.fetchrow(
            "SELECT data FROM cached_packages WHERE cache_key=$1 AND expires_at > NOW()",
            key)
        return json.loads(row["data"]) if row else None

async def store_packages(key: str, data):
    serialised = data.model_dump_json()
    await r.setex(f"pkg:{key}", TTL_SECONDS, serialised)
    async with get_db() as db:
        await db.execute("""
            INSERT INTO cached_packages (cache_key, data, generated_at, expires_at)
            VALUES ($1, $2, NOW(), NOW() + INTERVAL '6 hours')
            ON CONFLICT (cache_key) DO UPDATE SET data=$2, generated_at=NOW(), expires_at=NOW() + INTERVAL '6 hours'
        """, key, serialised)


# ── utils/maps_export.py ─────────────────────────────────────
"""
Builds a KML file with one placemark per itinerary slot, tagged
by day and time-slot. Opens directly in Google Maps "My Maps".
"""
def build_kml_export(pkg_response, tier_name: str) -> str:
    tier = next(t for t in pkg_response["packages"] if t["tier"] == tier_name)
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<kml xmlns="http://www.opengis.net/kml/2.2">',
             f'<Document><name>TripForge — {pkg_response["destination"]} ({tier_name.title()})</name>']

    colors = {"luxury": "ff7B3FFF", "value": "ff37A06B", "budget": "ffE08B20"}
    slot_icons = {"morning": "🌅", "afternoon": "☀️", "evening": "🌆", "night": "🌙"}

    for day in tier["itinerary"]:
        lines.append(f'<Folder><name>Day {day["day_number"]} — {day["geographic_zone"]}</name>')
        for s in day["slots"]:
            icon = slot_icons.get(s["time_slot"], "📍")
            lines.append(f"""
<Placemark>
  <name>{icon} {s["activity"]}</name>
  <description>
    {s["time_slot"].title()} · {s["location_name"]}
    Fee: S${s["entry_fee_sgd"]:.2f} | Transport: {s["transport_note"]}
    Food: {", ".join(s.get("food_spots", []))}
  </description>
  <Style><IconStyle><color>{colors[tier_name]}</color></IconStyle></Style>
  <Point><coordinates>{s["longitude"]},{s["latitude"]},0</coordinates></Point>
</Placemark>""")
        lines.append('</Folder>')

    lines.extend(['</Document>', '</kml>'])
    return "\n".join(lines)
