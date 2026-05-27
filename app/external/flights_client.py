from typing import List
from datetime import datetime, timedelta
from app.models.schemas import FlightOption

FLIGHT_CATALOGUE = {
    'HAN': [
        FlightOption(airline='Singapore Airlines', flight_number='SQ182', duration_minutes=165, stopovers=0, price_sgd=620, cabin_class='economy', departure_time='08:00', arrival_time='10:45'),
        FlightOption(airline='Vietnam Airlines', flight_number='VN600', duration_minutes=175, stopovers=0, price_sgd=480, cabin_class='economy', departure_time='11:30', arrival_time='14:25'),
        FlightOption(airline='Scoot', flight_number='TR2', duration_minutes=185, stopovers=0, price_sgd=310, cabin_class='economy', departure_time='06:00', arrival_time='08:55'),
        FlightOption(airline='VietJet Air', flight_number='VJ102', duration_minutes=285, stopovers=1, price_sgd=210, cabin_class='economy', departure_time='05:00', arrival_time='10:45'),
        FlightOption(airline='AirAsia', flight_number='AK712', duration_minutes=560, stopovers=2, price_sgd=105, cabin_class='economy', departure_time='01:00', arrival_time='12:20'),
    ],
    'BKK': [
        FlightOption(airline='Singapore Airlines', flight_number='SQ976', duration_minutes=155, stopovers=0, price_sgd=420, cabin_class='economy', departure_time='09:00', arrival_time='10:35'),
        FlightOption(airline='Thai Airways', flight_number='TG411', duration_minutes=160, stopovers=0, price_sgd=360, cabin_class='economy', departure_time='13:20', arrival_time='14:50'),
        FlightOption(airline='Scoot', flight_number='TR608', duration_minutes=165, stopovers=0, price_sgd=220, cabin_class='economy', departure_time='07:00', arrival_time='08:45'),
        FlightOption(airline='AirAsia', flight_number='AK502', duration_minutes=175, stopovers=0, price_sgd=160, cabin_class='economy', departure_time='06:00', arrival_time='07:55'),
        FlightOption(airline='Thai Lion Air', flight_number='SL102', duration_minutes=330, stopovers=1, price_sgd=90, cabin_class='economy', departure_time='23:00', arrival_time='04:10'),
    ],
    'DPS': [
        FlightOption(airline='Singapore Airlines', flight_number='SQ946', duration_minutes=145, stopovers=0, price_sgd=480, cabin_class='economy', departure_time='08:30', arrival_time='10:55'),
        FlightOption(airline='Garuda Indonesia', flight_number='GA826', duration_minutes=150, stopovers=0, price_sgd=380, cabin_class='economy', departure_time='12:00', arrival_time='14:20'),
        FlightOption(airline='Scoot', flight_number='TR272', duration_minutes=155, stopovers=0, price_sgd=250, cabin_class='economy', departure_time='06:45', arrival_time='09:10'),
        FlightOption(airline='AirAsia', flight_number='QZ8074', duration_minutes=160, stopovers=0, price_sgd=180, cabin_class='economy', departure_time='05:30', arrival_time='07:50'),
        FlightOption(airline='Batik Air', flight_number='OD251', duration_minutes=320, stopovers=1, price_sgd=110, cabin_class='economy', departure_time='22:00', arrival_time='03:20'),
    ],
    'NRT': [
        FlightOption(airline='Singapore Airlines', flight_number='SQ12', duration_minutes=370, stopovers=0, price_sgd=980, cabin_class='economy', departure_time='00:15', arrival_time='08:05'),
        FlightOption(airline='Japan Airlines', flight_number='JL712', duration_minutes=375, stopovers=0, price_sgd=860, cabin_class='economy', departure_time='10:30', arrival_time='18:45'),
        FlightOption(airline='Scoot', flight_number='TR808', duration_minutes=395, stopovers=0, price_sgd=520, cabin_class='economy', departure_time='08:00', arrival_time='16:15'),
        FlightOption(airline='AirAsia X', flight_number='D7522', duration_minutes=580, stopovers=1, price_sgd=320, cabin_class='economy', departure_time='22:00', arrival_time='10:40'),
    ],
    'MEL': [
        FlightOption(airline='Singapore Airlines', flight_number='SQ227', duration_minutes=475, stopovers=0, price_sgd=1050, cabin_class='economy', departure_time='08:00', arrival_time='19:55'),
        FlightOption(airline='Qantas', flight_number='QF38', duration_minutes=480, stopovers=0, price_sgd=920, cabin_class='economy', departure_time='16:00', arrival_time='04:00'),
        FlightOption(airline='Jetstar', flight_number='JQ8', duration_minutes=490, stopovers=0, price_sgd=580, cabin_class='economy', departure_time='22:30', arrival_time='10:40'),
        FlightOption(airline='AirAsia X', flight_number='D7220', duration_minutes=680, stopovers=1, price_sgd=360, cabin_class='economy', departure_time='01:00', arrival_time='15:20'),
    ],
}

def _seasonal_multiplier(date_str: str) -> float:
    try:
        month = datetime.strptime(date_str, '%Y-%m-%d').month
    except Exception:
        return 1.0
    return {1:1.15,2:0.90,3:0.88,4:0.95,5:1.00,6:1.12,7:1.15,8:1.10,9:0.90,10:0.88,11:0.95,12:1.18}.get(month, 1.0)

async def fetch_flights(origin_iata: str, dest_iata: str, date_from: str, stay_duration: int) -> List[FlightOption]:
    raw = FLIGHT_CATALOGUE.get(dest_iata, [])
    if not raw:
        raise ValueError(f'No flight data for: {dest_iata}')
    mult = _seasonal_multiplier(date_from)
    return [FlightOption(
        airline=f.airline, flight_number=f.flight_number,
        duration_minutes=f.duration_minutes, stopovers=f.stopovers,
        price_sgd=round(f.price_sgd * mult, 0),
        cabin_class=f.cabin_class, departure_time=f.departure_time,
        arrival_time=f.arrival_time,
    ) for f in raw]
