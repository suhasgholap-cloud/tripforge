import httpx
from app.models.schemas import WeatherSnapshot
from app.config import get_settings

cfg = get_settings()

BEST_TIME = {
    'HAN': 'Oct-Dec is ideal.', 'BKK': 'Nov-Feb is best.',
    'DPS': 'Apr-Oct is dry season.', 'NRT': 'Mar-May or Oct-Nov.',
    'MEL': 'Mar-May and Sep-Nov.',
}

FLIGHT_TRENDS = {
    'HAN': [{'month': m, 'avg_price_sgd': p} for m, p in zip(
        ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
        [380,420,360,340,320,390,410,400,350,310,290,450])],
    'BKK': [{'month': m, 'avg_price_sgd': p} for m, p in zip(
        ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
        [220,240,200,190,180,210,230,220,195,185,170,280])],
    'DPS': [{'month': m, 'avg_price_sgd': p} for m, p in zip(
        ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
        [300,320,290,270,260,340,380,370,310,280,250,360])],
    'NRT': [{'month': m, 'avg_price_sgd': p} for m, p in zip(
        ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
        [520,540,620,700,560,480,510,530,490,580,560,650])],
    'MEL': [{'month': m, 'avg_price_sgd': p} for m, p in zip(
        ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
        [460,440,400,380,360,340,350,370,390,410,430,500])],
}

class WeatherService:
    def __init__(self, dest_iata: str):
        self.iata = dest_iata
        self.dest = cfg.DESTINATIONS.get(dest_iata, {})

    async def fetch(self) -> WeatherSnapshot:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get('https://api.open-meteo.com/v1/forecast', params={
                    'latitude': self.dest.get('lat', 0),
                    'longitude': self.dest.get('lon', 0),
                    'daily': 'temperature_2m_max,weathercode',
                    'timezone': self.dest.get('timezone', 'UTC'),
                    'forecast_days': '7',
                })
                data = r.json()
                temps = data.get('daily', {}).get('temperature_2m_max', [28.0])
                avg_t = round(sum(temps) / len(temps), 1)
                code  = data.get('daily', {}).get('weathercode', [2])[0]
                cond  = {0:'Clear sky',1:'Mainly clear',2:'Partly cloudy',3:'Overcast',
                         61:'Rain',80:'Showers',95:'Thunderstorm'}.get(int(code),'Partly cloudy')
        except Exception:
            avg_t, cond = 28.0, 'Partly cloudy'

        return WeatherSnapshot(
            avg_temp_c=avg_t, condition=cond,
            best_time_note=BEST_TIME.get(self.iata, 'Check local conditions.'),
            local_events=[], monthly_flight_cost_trend=FLIGHT_TRENDS.get(self.iata, []),
        )
