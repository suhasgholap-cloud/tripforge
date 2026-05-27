import uuid, asyncio
from app.models.schemas import TripRequest, TripResponse, PackageTier
from app.external.flights_client import fetch_flights
from app.external.hotels_client import fetch_hotels
from app.external.weather_client import WeatherService
from app.services.optimizer import PackageOptimizer
from app.services.itinerary_builder import ItineraryBuilder

class TripOrchestrator:
    def __init__(self, req: TripRequest):
        self.req = req

    async def run(self) -> TripResponse:
        from datetime import datetime, timedelta
        date_from = self.req.travel_date_from or (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')

        flights, hotels, weather = await asyncio.gather(
            fetch_flights(self.req.origin_iata, self.req.destination_iata, date_from, self.req.stay_duration),
            fetch_hotels(self.req.destination_iata, self.req.stay_duration, date_from),
            WeatherService(self.req.destination_iata).fetch(),
        )

        optimizer = PackageOptimizer(flights, hotels, self.req.stay_duration)
        tiers = optimizer.build_tiers()

        builder = ItineraryBuilder(self.req.destination_iata, self.req.interests, self.req.stay_duration, tiers)
        itineraries = await builder.build_all()

        packages = []
        for tier_name in ['luxury', 'value', 'budget']:
            t = tiers[tier_name]
            daily = {'luxury': 120, 'value': 60, 'budget': 25}[tier_name]
            total = round(t['flight'].price_sgd * 2 + t['hotel'].total_cost_sgd + daily * self.req.stay_duration, 2)
            packages.append(PackageTier(
                tier=tier_name, total_price_sgd=total, score=t['score'],
                weather=weather, flights=[t['flight']], hotels=[t['hotel']],
                itinerary=itineraries[tier_name],
            ))

        return TripResponse(trip_id=str(uuid.uuid4())[:8], destination=self.req.destination_name, packages=packages)
