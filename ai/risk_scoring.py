"""Risk Scoring and Visualization for Flood Simulation.

Provides real-time flood risk calculations based on location, rainfall,
historical data, and user behavior patterns.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from enum import Enum


class RiskLevel(Enum):
    """Risk levels with associated colors and descriptions."""
    LOW = ("low", "Safe", (100, 200, 100), "Conditions are normal.")
    MEDIUM = ("medium", "Caution", (255, 200, 100), "Monitor conditions.")
    HIGH = ("high", "Warning", (255, 150, 100), "Be prepared to act.")
    CRITICAL = ("critical", "Danger", (255, 100, 100), "Evacuate immediately!")
    
    def __init__(self, value, label, color, description):
        self._value = value
        self.label = label
        self.color = color
        self.description = description
    
    @property
    def rgb(self) -> Tuple[int, int, int]:
        return self.color


@dataclass
class RiskFactors:
    """Individual risk factors contributing to overall score."""
    location_risk: float = 0.0  # 0-100 based on flood history
    rainfall_risk: float = 0.0  # 0-100 based on current rainfall
    duration_risk: float = 0.0  # 0-100 based on how long rain has persisted
    trend_risk: float = 0.0     # 0-100 based on rising/falling trend
    time_risk: float = 0.0      # 0-100 based on time of day (night = higher)
    
    def to_dict(self) -> Dict[str, float]:
        return {
            "Location History": self.location_risk,
            "Rainfall Intensity": self.rainfall_risk,
            "Storm Duration": self.duration_risk,
            "Rain Trend": self.trend_risk,
            "Time Factor": self.time_risk,
        }


@dataclass
class RiskScore:
    """Complete risk assessment with scoring breakdown."""
    score: int  # 0-100 overall score
    level: RiskLevel
    factors: RiskFactors
    location: str
    rainfall: float
    timestamp: datetime = field(default_factory=datetime.now)
    recommendation: str = ""
    
    def get_color_gradient(self) -> Tuple[int, int, int]:
        """Get color based on score (smooth gradient)."""
        if self.score < 25:
            # Green to yellow
            t = self.score / 25
            return (
                int(100 + (255 - 100) * t),
                int(200 + (200 - 200) * t),
                int(100 + (100 - 100) * t)
            )
        elif self.score < 50:
            # Yellow to orange
            t = (self.score - 25) / 25
            return (
                int(255 + (255 - 255) * t),
                int(200 + (150 - 200) * t),
                int(100 + (100 - 100) * t)
            )
        elif self.score < 75:
            # Orange to red
            t = (self.score - 50) / 25
            return (
                int(255 + (255 - 255) * t),
                int(150 + (100 - 150) * t),
                int(100 + (100 - 100) * t)
            )
        else:
            # Deep red
            return (255, 100, 100)


class RiskScorer:
    """Calculates flood risk scores based on multiple factors.
    
    Uses weighted factors to compute an overall risk score:
    - Location flood history (30%)
    - Current rainfall intensity (35%)
    - Rainfall duration (15%)
    - Rainfall trend (10%)
    - Time of day (10%)
    """
    
    # Location risk scores based on historical flood data
    LOCATION_RISK_SCORES = {
        "ION Orchard": 10,      # High ground, rarely floods
        "Orchard Road": 40,     # Street level, occasional flooding
        "Tanglin Carpark": 80,  # Basement, flooded 2010/2011
    }
    
    # Rainfall thresholds (mm)
    RAINFALL_THRESHOLDS = {
        "light": 30,
        "moderate": 50,
        "heavy": 80,
        "severe": 100,
    }
    
    # Weights for risk factors
    WEIGHTS = {
        "location": 0.30,
        "rainfall": 0.35,
        "duration": 0.15,
        "trend": 0.10,
        "time": 0.10,
    }
    
    def __init__(self):
        """Initialize the risk scorer."""
        self._rainfall_history: List[Tuple[datetime, float]] = []
        self._max_history = 100
        self._last_location: Optional[str] = None
        
    def calculate_risk(
        self,
        location: str,
        rainfall: float,
        time_of_day: Optional[datetime] = None
    ) -> RiskScore:
        """Calculate comprehensive risk score.
        
        Args:
            location: Current location name
            rainfall: Current rainfall in mm
            time_of_day: Optional datetime (defaults to now)
            
        Returns:
            RiskScore with breakdown
        """
        now = time_of_day or datetime.now()
        
        # Update history
        self._rainfall_history.append((now, rainfall))
        if len(self._rainfall_history) > self._max_history:
            self._rainfall_history.pop(0)
        
        # Calculate individual factors
        location_risk = self._calc_location_risk(location)
        rainfall_risk = self._calc_rainfall_risk(rainfall)
        duration_risk = self._calc_duration_risk()
        trend_risk = self._calc_trend_risk()
        time_risk = self._calc_time_risk(now)
        
        factors = RiskFactors(
            location_risk=location_risk,
            rainfall_risk=rainfall_risk,
            duration_risk=duration_risk,
            trend_risk=trend_risk,
            time_risk=time_risk
        )
        
        # Calculate weighted score
        score = int(
            location_risk * self.WEIGHTS["location"] +
            rainfall_risk * self.WEIGHTS["rainfall"] +
            duration_risk * self.WEIGHTS["duration"] +
            trend_risk * self.WEIGHTS["trend"] +
            time_risk * self.WEIGHTS["time"]
        )
        
        # Determine risk level
        level = self._get_risk_level(score)
        
        # Generate recommendation
        recommendation = self._get_recommendation(score, location)
        
        return RiskScore(
            score=score,
            level=level,
            factors=factors,
            location=location,
            rainfall=rainfall,
            timestamp=now,
            recommendation=recommendation
        )
    
    def _calc_location_risk(self, location: str) -> float:
        """Calculate location-based risk (0-100)."""
        base_score = self.LOCATION_RISK_SCORES.get(location, 50)
        return min(100, max(0, base_score))
    
    def _calc_rainfall_risk(self, rainfall: float) -> float:
        """Calculate rainfall intensity risk (0-100)."""
        if rainfall < self.RAINFALL_THRESHOLDS["light"]:
            return rainfall / self.RAINFALL_THRESHOLDS["light"] * 25
        elif rainfall < self.RAINFALL_THRESHOLDS["moderate"]:
            return 25 + (rainfall - self.RAINFALL_THRESHOLDS["light"]) / \
                   (self.RAINFALL_THRESHOLDS["moderate"] - self.RAINFALL_THRESHOLDS["light"]) * 25
        elif rainfall < self.RAINFALL_THRESHOLDS["heavy"]:
            return 50 + (rainfall - self.RAINFALL_THRESHOLDS["moderate"]) / \
                   (self.RAINFALL_THRESHOLDS["heavy"] - self.RAINFALL_THRESHOLDS["moderate"]) * 25
        else:
            return min(100, 75 + (rainfall - self.RAINFALL_THRESHOLDS["heavy"]) / 20 * 25)
    
    def _calc_duration_risk(self) -> float:
        """Calculate duration-based risk (0-100)."""
        if len(self._rainfall_history) < 10:
            return 0
        
        # Count how long rainfall has been above 30mm
        heavy_rain_count = sum(1 for _, r in self._rainfall_history if r >= 30)
        ratio = heavy_rain_count / len(self._rainfall_history)
        
        return ratio * 100
    
    def _calc_trend_risk(self) -> float:
        """Calculate trend-based risk (0-100)."""
        if len(self._rainfall_history) < 5:
            return 0
        
        # Compare recent vs older readings
        recent = self._rainfall_history[-3:]
        older = self._rainfall_history[:3]
        
        recent_avg = sum(r for _, r in recent) / len(recent)
        older_avg = sum(r for _, r in older) / len(older)
        
        if recent_avg > older_avg:
            # Rising trend - increasing risk
            change = recent_avg - older_avg
            return min(100, change * 2)
        else:
            # Falling trend - decreasing risk
            return 0
    
    def _calc_time_risk(self, time: datetime) -> float:
        """Calculate time-of-day risk (0-100).
        
        Night time (22:00-06:00) has slightly higher risk due to
        reduced visibility and response times.
        """
        hour = time.hour
        if hour >= 22 or hour < 6:
            return 30  # Night time
        elif hour >= 18 or hour < 8:
            return 15  # Evening/early morning
        return 0  # Day time
    
    def _get_risk_level(self, score: int) -> RiskLevel:
        """Convert score to risk level."""
        if score < 25:
            return RiskLevel.LOW
        elif score < 50:
            return RiskLevel.MEDIUM
        elif score < 75:
            return RiskLevel.HIGH
        return RiskLevel.CRITICAL
    
    def _get_recommendation(self, score: int, location: str) -> str:
        """Generate contextual recommendation."""
        if score < 25:
            return "Safe to continue normal activities."
        elif score < 50:
            return f"Stay alert at {location}. Monitor weather updates."
        elif score < 75:
            return f"Be prepared to leave {location}. Identify evacuation routes."
        return f"URGENT: Leave {location} immediately! Move to higher ground!"
    
    def get_location_history(self, location: str) -> str:
        """Get historical flood information for a location.
        
        Args:
            location: Location name
            
        Returns:
            Historical context string
        """
        histories = {
            "ION Orchard": "High ground (18m elevation). No significant flood history.",
            "Orchard Road": "Flash flood prone. Minor flooding during heavy storms.",
            "Tanglin Carpark": "DANGER: Flooded in 2010 and 2011. Basement car park.",
        }
        return histories.get(location, "No specific flood history available.")


class PersonalizedRiskScorer(RiskScorer):
    """Risk scorer that learns from user behavior.
    
    Tracks which locations the user visits and questions they ask
to provide personalized risk assessments.
    """
    
    def __init__(self):
        """Initialize personalized scorer."""
        super().__init__()
        self._user_locations: Dict[str, int] = {}  # location -> visit count
        self._user_questions: List[str] = []
        self._concerned_locations: set = set()
        
    def record_location_visit(self, location: str) -> None:
        """Record that user visited a location.
        
        Args:
            location: Location name
        """
        self._user_locations[location] = self._user_locations.get(location, 0) + 1
        
    def record_question(self, question: str, location: str) -> None:
        """Record a user question for pattern analysis.
        
        Args:
            question: Question text
            location: Current location when asked
        """
        self._user_questions.append(question)
        
        # Check if question indicates concern about flooding
        concern_keywords = ["flood", "danger", "safe", "evacuate", "risk"]
        if any(kw in question.lower() for kw in concern_keywords):
            self._concerned_locations.add(location)
    
    def calculate_risk(
        self,
        location: str,
        rainfall: float,
        time_of_day: Optional[datetime] = None
    ) -> RiskScore:
        """Calculate personalized risk score."""
        # Record visit
        self.record_location_visit(location)
        
        # Get base score
        score = super().calculate_risk(location, rainfall, time_of_day)
        
        # Adjust for user behavior patterns
        if location in self._concerned_locations:
            # User previously asked about flooding here - they may be more cautious
            score.score = min(100, score.score + 5)
            score.recommendation += " (You've previously expressed concern about this area.)"
        
        return score
    
    def get_user_profile(self) -> Dict:
        """Get user's risk profile.
        
        Returns:
            Dict with user behavior patterns
        """
        return {
            "most_visited": sorted(
                self._user_locations.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3],
            "concerned_locations": list(self._concerned_locations),
            "total_questions": len(self._user_questions),
        }