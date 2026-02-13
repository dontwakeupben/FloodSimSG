"""Rainfall API client for fetching live rainfall data from data.gov.sg."""
import requests
import time
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class RainfallStation:
    """Represents a rainfall monitoring station."""
    id: str
    device_id: str
    name: str
    latitude: float
    longitude: float


@dataclass
class RainfallReading:
    """Represents a rainfall reading at a specific time."""
    station_id: str
    value: float  # mm of rainfall
    timestamp: str


class RainfallAPIClient:
    """Client for fetching live rainfall data from data.gov.sg API.
    
    API Endpoint: https://api-open.data.gov.sg/v2/real-time/api/rainfall
    Updates every 5 minutes.
    """
    
    BASE_URL = "https://api-open.data.gov.sg/v2/real-time/api"
    CACHE_DURATION = 300  # 5 minutes in seconds
    
    def __init__(self):
        """Initialize the API client with empty cache."""
        self._cache: Optional[Dict] = None
        self._last_fetch: float = 0
        self._last_error: Optional[str] = None
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "User-Agent": "FloodSimulationGame/1.0"
        })
    
    def fetch_latest_rainfall(self, force_refresh: bool = False) -> Optional[Dict]:
        """Fetch the latest rainfall data from the API.
        
        Args:
            force_refresh: If True, bypass cache and fetch fresh data
            
        Returns:
            Parsed JSON response or None if request fails
        """
        now = time.time()
        
        # Return cached data if still valid
        if not force_refresh and self._cache is not None:
            if now - self._last_fetch < self.CACHE_DURATION:
                return self._cache
        
        try:
            response = self.session.get(
                f"{self.BASE_URL}/rainfall",
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Validate response structure
            if data.get("code") != 0:
                self._last_error = data.get("errorMsg", "Unknown API error")
                return None
            
            self._cache = data
            self._last_fetch = now
            self._last_error = None
            return data
            
        except requests.exceptions.Timeout:
            self._last_error = "Request timeout"
            return None
        except requests.exceptions.ConnectionError:
            self._last_error = "Connection error"
            return None
        except requests.exceptions.HTTPError as e:
            self._last_error = f"HTTP error: {e.response.status_code}"
            return None
        except requests.exceptions.RequestException as e:
            self._last_error = f"Request failed: {str(e)}"
            return None
        except ValueError:  # JSON decode error
            self._last_error = "Invalid JSON response"
            return None
    
    def get_stations(self) -> List[RainfallStation]:
        """Get list of all rainfall monitoring stations.
        
        Returns:
            List of RainfallStation objects
        """
        data = self.fetch_latest_rainfall()
        if not data or "data" not in data:
            return []
        
        stations = data["data"].get("stations", [])
        return [
            RainfallStation(
                id=s["id"],
                device_id=s["deviceId"],
                name=s["name"],
                latitude=s["location"]["latitude"],
                longitude=s["location"]["longitude"]
            )
            for s in stations
        ]
    
    def get_readings(self) -> List[RainfallReading]:
        """Get latest rainfall readings from all stations.
        
        Returns:
            List of RainfallReading objects
        """
        data = self.fetch_latest_rainfall()
        if not data or "data" not in data:
            return []
        
        readings_data = data["data"].get("readings", [])
        if not readings_data:
            return []
        
        # Get the most recent readings batch
        latest_reading = readings_data[0]
        timestamp = latest_reading.get("timestamp", "")
        
        return [
            RainfallReading(
                station_id=r["stationId"],
                value=r["value"],
                timestamp=timestamp
            )
            for r in latest_reading.get("data", [])
        ]
    
    def get_reading_for_station(self, station_id: str) -> Optional[RainfallReading]:
        """Get rainfall reading for a specific station.
        
        Args:
            station_id: Station ID (e.g., "S111")
            
        Returns:
            RainfallReading or None if not found
        """
        readings = self.get_readings()
        for reading in readings:
            if reading.station_id == station_id:
                return reading
        return None
    
    def get_average_rainfall(self, station_ids: List[str]) -> Optional[float]:
        """Calculate average rainfall across multiple stations.
        
        Args:
            station_ids: List of station IDs to average
            
        Returns:
            Average rainfall in mm, or None if no valid readings
        """
        readings = self.get_readings()
        values = [r.value for r in readings if r.station_id in station_ids]
        
        if not values:
            return None
        return sum(values) / len(values)
    
    def get_last_error(self) -> Optional[str]:
        """Get the last error message if any."""
        return self._last_error
    
    def is_cache_valid(self) -> bool:
        """Check if cached data is still valid."""
        if self._cache is None:
            return False
        return time.time() - self._last_fetch < self.CACHE_DURATION
    
    def get_cache_age(self) -> float:
        """Get age of cached data in seconds."""
        if self._last_fetch == 0:
            return float('inf')
        return time.time() - self._last_fetch


# Station mappings for game zones
# These are the closest stations to each game zone based on coordinates
ZONE_STATIONS = {
    "ion_orchard": ["S79", "S111"],    # Somerset Road, Scotts Road (closest to ION)
    "orchard_road": ["S79", "S111"],   # Somerset Road, Scotts Road (same area)
    "tanglin_carpark": ["S120", "S222"],  # Holland Road, Henderson Road (closest to Tanglin)
}

# Approximate coordinates for reference:
# ION Orchard: 1.304, 103.831
# Orchard Road: 1.305, 103.832
# Tanglin Carpark: 1.303, 103.823


def get_rainfall_for_zone(client: RainfallAPIClient, zone: str) -> Optional[float]:
    """Get rainfall value for a specific game zone.
    
    Args:
        client: RainfallAPIClient instance
        zone: Zone name ("ion_orchard", "orchard_road", "tanglin_carpark")
        
    Returns:
        Rainfall in mm, or None if data unavailable
    """
    station_ids = ZONE_STATIONS.get(zone, [])
    if not station_ids:
        return None
    return client.get_average_rainfall(station_ids)


def test_api():
    """Test function to verify API connectivity."""
    print("Testing Rainfall API connection...")
    client = RainfallAPIClient()
    
    # Fetch latest data
    data = client.fetch_latest_rainfall()
    
    if data is None:
        print(f"[FAIL] Failed to fetch data: {client.get_last_error()}")
        return False
    
    print("[OK] Successfully connected to API")
    
    # Get stations
    stations = client.get_stations()
    print(f"[OK] Found {len(stations)} rainfall stations")
    
    # Show first few stations
    print("\nSample stations:")
    for s in stations[:5]:
        print(f"  {s.id}: {s.name} ({s.latitude}, {s.longitude})")
    
    # Get readings
    readings = client.get_readings()
    print(f"\n[OK] Retrieved {len(readings)} rainfall readings")
    
    # Show sample readings
    print("\nSample readings:")
    for r in readings[:5]:
        print(f"  Station {r.station_id}: {r.value}mm at {r.timestamp}")
    
    # Get zone rainfall
    print("\nZone rainfall estimates:")
    for zone in ["ion_orchard", "orchard_road", "tanglin_carpark"]:
        rainfall = get_rainfall_for_zone(client, zone)
        if rainfall is not None:
            print(f"  {zone}: {rainfall:.1f}mm")
        else:
            print(f"  {zone}: No data available")
    
    return True


if __name__ == "__main__":
    test_api()
