from app.models.schemas import FlightOption, HotelOption
from typing import List

WEIGHTS = {
    'luxury': {'price': 0.20, 'quality': 0.55, 'speed': 0.25},
    'value':  {'price': 0.45, 'quality': 0.40, 'speed': 0.15},
    'budget': {'price': 0.75, 'quality': 0.20, 'speed': 0.05},
}

class PackageOptimizer:
    def __init__(self, flights: List[FlightOption], hotels: List[HotelOption], stay_duration: int):
        self.flights = flights
        self.hotels = hotels
        self.nights = stay_duration

    def build_tiers(self) -> dict:
        candidates = self._score_all()
        return {
            'luxury': self._pick(candidates, 'luxury'),
            'value':  self._pick(candidates, 'value'),
            'budget': self._pick(candidates, 'budget'),
        }

    def _score_all(self):
        prices   = [f.price_sgd * 2 + h.total_cost_sgd for f in self.flights for h in self.hotels]
        quality  = [h.review_score for h in self.hotels]
        duration = [f.duration_minutes for f in self.flights]
        p_min, p_max = min(prices), max(prices)
        q_min, q_max = min(quality), max(quality)
        d_min, d_max = min(duration), max(duration)
        candidates = []
        for f in self.flights:
            for h in self.hotels:
                total = f.price_sgd * 2 + h.total_cost_sgd
                scores = {
                    'price':   1 - self._norm(total, p_min, p_max),
                    'quality': self._norm(h.review_score, q_min, q_max),
                    'speed':   1 - self._norm(f.duration_minutes, d_min, d_max),
                }
                candidates.append({'flight': f, 'hotel': h, 'scores': scores})
        return candidates

    def _pick(self, candidates, tier):
        w = WEIGHTS[tier]
        star_min, star_max = {'luxury': (4,5), 'value': (3,4), 'budget': (2,3)}[tier]
        eligible = [c for c in candidates if star_min <= c['hotel'].star_rating <= star_max] or candidates
        scored = sorted(eligible, key=lambda c: sum(c['scores'][k]*v for k,v in w.items()), reverse=True)
        best = scored[0]
        best['score'] = int(sum(best['scores'][k]*v for k,v in w.items()) * 100)
        return best

    def _norm(self, val, lo, hi):
        return (val - lo) / (hi - lo) if hi != lo else 0.5
