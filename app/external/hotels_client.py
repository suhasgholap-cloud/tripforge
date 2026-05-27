from typing import List, Optional
from datetime import datetime
from app.models.schemas import HotelOption

HOTEL_CATALOGUE = {
    'HAN': [
        HotelOption(hotel_name='Sofitel Legend Metropole', star_rating=5, nightly_rate_sgd=420, total_cost_sgd=0, review_score=9.4, review_count=4280, district='Hoan Kiem', amenities=['Pool','Spa','WiFi','Fine dining']),
        HotelOption(hotel_name='JW Marriott Hanoi', star_rating=5, nightly_rate_sgd=310, total_cost_sgd=0, review_score=9.1, review_count=3140, district='Ba Dinh', amenities=['Pool','Gym','Breakfast','WiFi']),
        HotelOption(hotel_name='Hanoi La Siesta Hotel', star_rating=4, nightly_rate_sgd=130, total_cost_sgd=0, review_score=8.9, review_count=5620, district='Old Quarter', amenities=['Breakfast','WiFi','Rooftop bar']),
        HotelOption(hotel_name='Essence Palace Hotel', star_rating=4, nightly_rate_sgd=98, total_cost_sgd=0, review_score=8.7, review_count=3210, district='Old Quarter', amenities=['Breakfast','WiFi']),
        HotelOption(hotel_name='Hanoi Backpackers Boutique', star_rating=3, nightly_rate_sgd=58, total_cost_sgd=0, review_score=8.5, review_count=7840, district='Old Quarter', amenities=['WiFi','Bar']),
        HotelOption(hotel_name='Rising Dragon Grand Hotel', star_rating=3, nightly_rate_sgd=48, total_cost_sgd=0, review_score=8.2, review_count=4510, district='Hoan Kiem', amenities=['WiFi','Breakfast']),
        HotelOption(hotel_name='Old Quarter View Hostel', star_rating=2, nightly_rate_sgd=24, total_cost_sgd=0, review_score=8.4, review_count=9250, district='Old Quarter', amenities=['WiFi','Locker']),
        HotelOption(hotel_name='Hanoi Central Hostel', star_rating=2, nightly_rate_sgd=18, total_cost_sgd=0, review_score=8.1, review_count=6120, district='Old Quarter', amenities=['WiFi','Breakfast']),
    ],
@"
from typing import List, Optional
from datetime import datetime
from app.models.schemas import HotelOption

HOTEL_CATALOGUE = {
    'HAN': [
        HotelOption(hotel_name='Sofitel Legend Metropole', star_rating=5, nightly_rate_sgd=420, total_cost_sgd=0, review_score=9.4, review_count=4280, district='Hoan Kiem', amenities=['Pool','Spa','WiFi','Fine dining']),
        HotelOption(hotel_name='JW Marriott Hanoi', star_rating=5, nightly_rate_sgd=310, total_cost_sgd=0, review_score=9.1, review_count=3140, district='Ba Dinh', amenities=['Pool','Gym','Breakfast','WiFi']),
        HotelOption(hotel_name='Hanoi La Siesta Hotel', star_rating=4, nightly_rate_sgd=130, total_cost_sgd=0, review_score=8.9, review_count=5620, district='Old Quarter', amenities=['Breakfast','WiFi','Rooftop bar']),
        HotelOption(hotel_name='Essence Palace Hotel', star_rating=4, nightly_rate_sgd=98, total_cost_sgd=0, review_score=8.7, review_count=3210, district='Old Quarter', amenities=['Breakfast','WiFi']),
        HotelOption(hotel_name='Hanoi Backpackers Boutique', star_rating=3, nightly_rate_sgd=58, total_cost_sgd=0, review_score=8.5, review_count=7840, district='Old Quarter', amenities=['WiFi','Bar']),
        HotelOption(hotel_name='Rising Dragon Grand Hotel', star_rating=3, nightly_rate_sgd=48, total_cost_sgd=0, review_score=8.2, review_count=4510, district='Hoan Kiem', amenities=['WiFi','Breakfast']),
        HotelOption(hotel_name='Old Quarter View Hostel', star_rating=2, nightly_rate_sgd=24, total_cost_sgd=0, review_score=8.4, review_count=9250, district='Old Quarter', amenities=['WiFi','Locker']),
        HotelOption(hotel_name='Hanoi Central Hostel', star_rating=2, nightly_rate_sgd=18, total_cost_sgd=0, review_score=8.1, review_count=6120, district='Old Quarter', amenities=['WiFi','Breakfast']),
    ],
    'BKK': [
        HotelOption(hotel_name='Mandarin Oriental Bangkok', star_rating=5, nightly_rate_sgd=650, total_cost_sgd=0, review_score=9.6, review_count=5820, district='Riverside', amenities=['Pool','Spa','WiFi','Butler']),
        HotelOption(hotel_name='The Peninsula Bangkok', star_rating=5, nightly_rate_sgd=520, total_cost_sgd=0, review_score=9.4, review_count=4120, district='Riverside', amenities=['Pool','Spa','WiFi']),
        HotelOption(hotel_name='Anantara Siam Bangkok', star_rating=4, nightly_rate_sgd=210, total_cost_sgd=0, review_score=9.0, review_count=3860, district='Ratchaprasong', amenities=['Pool','Breakfast','WiFi']),
        HotelOption(hotel_name='Chatrium Hotel Riverside', star_rating=4, nightly_rate_sgd=145, total_cost_sgd=0, review_score=8.7, review_count=6240, district='Riverside', amenities=['Pool','WiFi','Breakfast']),
        HotelOption(hotel_name='Ibis Bangkok Silom', star_rating=3, nightly_rate_sgd=68, total_cost_sgd=0, review_score=8.3, review_count=8420, district='Silom', amenities=['WiFi','Breakfast']),
        HotelOption(hotel_name='Lub D Bangkok Silom', star_rating=3, nightly_rate_sgd=52, total_cost_sgd=0, review_score=8.5, review_count=11200, district='Silom', amenities=['WiFi','Pool','Bar']),
        HotelOption(hotel_name='Nap Krungthep Hostel', star_rating=2, nightly_rate_sgd=22, total_cost_sgd=0, review_score=8.6, review_count=7840, district='Bangrak', amenities=['WiFi','Common room']),
        HotelOption(hotel_name='Bodega Bangkok Hostel', star_rating=2, nightly_rate_sgd=16, total_cost_sgd=0, review_score=8.2, review_count=5310, district='Khao San', amenities=['WiFi','Bar']),
    ],
    'DPS': [
        HotelOption(hotel_name='Four Seasons Resort Bali', star_rating=5, nightly_rate_sgd=1100, total_cost_sgd=0, review_score=9.7, review_count=3210, district='Ubud', amenities=['Pool','Spa','WiFi','Butler']),
        HotelOption(hotel_name='The Mulia Bali', star_rating=5, nightly_rate_sgd=680, total_cost_sgd=0, review_score=9.4, review_count=4520, district='Nusa Dua', amenities=['Beach','Pool','Spa','WiFi']),
        HotelOption(hotel_name='Alaya Resort Ubud', star_rating=4, nightly_rate_sgd=220, total_cost_sgd=0, review_score=9.1, review_count=2840, district='Ubud', amenities=['Pool','Breakfast','WiFi']),
        HotelOption(hotel_name='Katamama Hotel Seminyak', star_rating=4, nightly_rate_sgd=180, total_cost_sgd=0, review_score=8.9, review_count=1960, district='Seminyak', amenities=['Pool','WiFi','Bar']),
        HotelOption(hotel_name='Bisma Cottages Kuta', star_rating=3, nightly_rate_sgd=62, total_cost_sgd=0, review_score=8.3, review_count=5420, district='Kuta', amenities=['Pool','WiFi','Breakfast']),
        HotelOption(hotel_name='Komaneka Ubud', star_rating=3, nightly_rate_sgd=95, total_cost_sgd=0, review_score=8.7, review_count=3140, district='Ubud', amenities=['Pool','WiFi','Breakfast']),
        HotelOption(hotel_name='Puri Garden Hostel', star_rating=2, nightly_rate_sgd=28, total_cost_sgd=0, review_score=8.5, review_count=8640, district='Kuta', amenities=['Pool','WiFi']),
        HotelOption(hotel_name='Tribal Hostel Canggu', star_rating=2, nightly_rate_sgd=20, total_cost_sgd=0, review_score=8.8, review_count=6210, district='Canggu', amenities=['Pool','WiFi','Bar']),
    ],
    'NRT': [
        HotelOption(hotel_name='The Tokyo EDITION', star_rating=5, nightly_rate_sgd=820, total_cost_sgd=0, review_score=9.5, review_count=2840, district='Minato', amenities=['Spa','WiFi','Gym','Bar']),
        HotelOption(hotel_name='Park Hyatt Tokyo', star_rating=5, nightly_rate_sgd=720, total_cost_sgd=0, review_score=9.3, review_count=3910, district='Shinjuku', amenities=['Pool','Spa','WiFi','Gym']),
        HotelOption(hotel_name='Andaz Tokyo', star_rating=4, nightly_rate_sgd=380, total_cost_sgd=0, review_score=9.1, review_count=4120, district='Minato', amenities=['WiFi','Breakfast','Gym']),
        HotelOption(hotel_name='Hotel Monterey Akasaka', star_rating=4, nightly_rate_sgd=210, total_cost_sgd=0, review_score=8.6, review_count=5840, district='Akasaka', amenities=['WiFi','Breakfast']),
        HotelOption(hotel_name='Dormy Inn Asakusa', star_rating=3, nightly_rate_sgd=98, total_cost_sgd=0, review_score=8.8, review_count=9240, district='Asakusa', amenities=['Onsen','WiFi','Breakfast']),
        HotelOption(hotel_name='APA Hotel Shinjuku', star_rating=3, nightly_rate_sgd=72, total_cost_sgd=0, review_score=8.2, review_count=12840, district='Shinjuku', amenities=['WiFi']),
        HotelOption(hotel_name='Khaosan Tokyo Origami', star_rating=2, nightly_rate_sgd=38, total_cost_sgd=0, review_score=8.6, review_count=7420, district='Asakusa', amenities=['WiFi','Rooftop']),
        HotelOption(hotel_name='Bunka Hostel Tokyo', star_rating=2, nightly_rate_sgd=28, total_cost_sgd=0, review_score=8.9, review_count=10240, district='Asakusa', amenities=['WiFi','Bar']),
    ],
    'MEL': [
        HotelOption(hotel_name='Crown Towers Melbourne', star_rating=5, nightly_rate_sgd=680, total_cost_sgd=0, review_score=9.3, review_count=3840, district='Southbank', amenities=['Pool','Spa','WiFi','Casino']),
        HotelOption(hotel_name='The Langham Melbourne', star_rating=5, nightly_rate_sgd=560, total_cost_sgd=0, review_score=9.2, review_count=4120, district='Southgate', amenities=['Pool','Spa','WiFi']),
        HotelOption(hotel_name='QT Melbourne', star_rating=4, nightly_rate_sgd=260, total_cost_sgd=0, review_score=8.9, review_count=5840, district='CBD', amenities=['WiFi','Gym','Bar']),
        HotelOption(hotel_name='Adelphi Hotel Melbourne', star_rating=4, nightly_rate_sgd=195, total_cost_sgd=0, review_score=8.7, review_count=3210, district='CBD', amenities=['Pool','WiFi','Bar']),
        HotelOption(hotel_name='Ibis Melbourne', star_rating=3, nightly_rate_sgd=110, total_cost_sgd=0, review_score=8.1, review_count=9240, district='CBD', amenities=['WiFi','Bar']),
        HotelOption(hotel_name='Alto Hotel on Bourke', star_rating=3, nightly_rate_sgd=88, total_cost_sgd=0, review_score=8.4, review_count=6120, district='CBD', amenities=['WiFi','Kitchenette']),
        HotelOption(hotel_name='Space Hotel Melbourne', star_rating=2, nightly_rate_sgd=42, total_cost_sgd=0, review_score=8.3, review_count=8420, district='CBD', amenities=['WiFi','Rooftop','Bar']),
        HotelOption(hotel_name='Melbourne Central YHA', star_rating=2, nightly_rate_sgd=32, total_cost_sgd=0, review_score=8.6, review_count=11240, district='CBD', amenities=['WiFi','Kitchen']),
    ],
}

def _multiplier(check_in: Optional[str]) -> float:
    if not check_in:
        return 1.0
    try:
        month = datetime.strptime(check_in, '%Y-%m-%d').month
    except Exception:
        return 1.0
    return {1:1.10,2:0.92,3:0.90,4:0.95,5:1.00,6:1.08,7:1.10,8:1.06,9:0.92,10:0.90,11:0.95,12:1.12}.get(month, 1.0)

async def fetch_hotels(dest_iata: str, stay_duration: int, check_in: Optional[str] = None, check_out: Optional[str] = None) -> List[HotelOption]:
    raw = HOTEL_CATALOGUE.get(dest_iata, [])
    if not raw:
        raise ValueError(f'No hotel data for: {dest_iata}')
    mult = _multiplier(check_in)
    return [HotelOption(
        hotel_name=h.hotel_name, star_rating=h.star_rating,
        nightly_rate_sgd=round(h.nightly_rate_sgd * mult, 0),
        total_cost_sgd=round(h.nightly_rate_sgd * mult * stay_duration, 0),
        review_score=h.review_score, review_count=h.review_count,
        district=h.district, amenities=h.amenities,
    ) for h in raw]
