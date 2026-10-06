#!/usr/bin/env python3
"""Exercise 0: Space Station Data.

Basic Pydantic model creation with BaseModel and Field constraints.
"""

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    """Vital statistics reported by a single space station.

    Every constraint is declared with Field(...): Pydantic checks it
    automatically when an instance is created, so an invalid station
    can never exist in memory.
    """

    # min_length / max_length apply to strings
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    # ge = "greater or equal", le = "less or equal" (numeric bounds)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    # An ISO string such as "2024-01-15T10:30:00" is converted to datetime
    last_maintenance: datetime
    # A plain default value makes the field optional in the input
    is_operational: bool = True
    # Optional[str] accepts None; the default None means "may be omitted"
    notes: Optional[str] = Field(default=None, max_length=200)


def display_station(station: SpaceStation) -> None:
    """Print a station's information in a readable format."""
    status = "Operational" if station.is_operational else "Maintenance"
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")
    print(f"Status: {status}")
    if station.notes is not None:
        print(f"Notes: {station.notes}")


def main() -> None:
    """Demonstrate a valid station and a station that fails validation."""
    separator = "=" * 40
    print("Space Station Data Validation")
    print(separator)

    try:
        # Raw data as it would arrive from JSON. The timestamp is a
        # string on purpose: Pydantic converts it to a datetime object.
        raw_station: Dict[str, Any] = {
            "station_id": "ISS001",
            "name": "International Space Station",
            "crew_size": 6,
            "power_level": 85.5,
            "oxygen_level": 92.3,
            "last_maintenance": "2024-01-15T10:30:00",
        }
        # model_validate builds (and validates) a model from a dict
        station = SpaceStation.model_validate(raw_station)
        print("Valid station created:")
        display_station(station)
    except ValidationError as error:
        print(f"Unexpected validation error: {error}")

    print()
    print(separator)

    try:
        # crew_size=25 breaks the le=20 constraint
        SpaceStation(
            station_id="BAD001",
            name="Overcrowded Station",
            crew_size=25,
            power_level=50.0,
            oxygen_level=80.0,
            last_maintenance=datetime(2024, 1, 15, 10, 30),
        )
        print("Error: the invalid station was accepted!")
    except ValidationError as error:
        print("Expected validation error:")
        # errors() returns a list of dicts; "msg" is the readable message
        for detail in error.errors():
            print(detail["msg"])


if __name__ == "__main__":
    main()
