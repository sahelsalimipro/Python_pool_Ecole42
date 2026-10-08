#!/usr/bin/env python3
"""Exercise 2: Space Crew Management.

Nested Pydantic models: a SpaceMission contains a list of CrewMember.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Mapping

from pydantic import BaseModel  # type: ignore
from pydantic import Field  # type: ignore
from pydantic import ValidationError  # type: ignore
from pydantic import model_validator  # type: ignore


class Rank(str, Enum):
    """Crew ranks, from lowest to highest."""

    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    """A single crew member. Validated on its own before the mission."""

    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    """A mission with its crew.

    The crew field is a list of CrewMember models: when a dict is given,
    Pydantic validates each item as a CrewMember first (nested
    validation), and only then runs the mission-level rules below.
    """

    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    # For a list, min_length / max_length limit the number of items
    crew: List[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def check_safety_rules(self) -> "SpaceMission":
        """Apply the safety requirements that need the whole crew."""
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')

        leaders = {Rank.COMMANDER, Rank.CAPTAIN}
        if not any(member.rank in leaders for member in self.crew):
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )

        if self.duration_days > 365:
            experienced = sum(
                1 for member in self.crew if member.years_experience >= 5
            )
            # Compare with integers to avoid float rounding:
            # experienced / len(crew) >= 0.5  <=>  experienced * 2 >= len
            if experienced * 2 < len(self.crew):
                raise ValueError(
                    "Long missions (> 365 days) need at least 50% "
                    "experienced crew (5+ years)"
                )

        inactive = [m.name for m in self.crew if not m.is_active]
        if inactive:
            raise ValueError(
                "All crew members must be active (inactive: "
                + ", ".join(inactive) + ")"
            )

        return self


def clean_message(detail: Mapping[str, object]) -> str:
    """Return an error message without Pydantic's "Value error, " prefix."""
    context = detail.get("ctx")
    if detail.get("type") == "value_error" and isinstance(context, dict):
        if "error" in context:
            return str(context["error"])
    return str(detail["msg"])


def display_mission(mission: SpaceMission) -> None:
    """Print a mission and its crew in a readable format."""
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew members:")
    for member in mission.crew:
        print(f"- {member.name} ({member.rank.value})"
              f" - {member.specialization}")


def try_invalid(title: str, data: Dict[str, Any]) -> None:
    """Try to build a mission from raw data and show why it fails."""
    print(f"--- {title} ---")
    try:
        SpaceMission.model_validate(data)
        print("Error: the invalid mission was accepted!")
    except ValidationError as error:
        print("Expected validation error:")
        for detail in error.errors():
            # "loc" shows where the error is, e.g. ('crew', 1, 'age')
            location = ".".join(str(part) for part in detail["loc"])
            prefix = f"[{location}] " if location else ""
            print(prefix + clean_message(detail))
    print()


def main() -> None:
    """Demonstrate a valid mission and several invalid ones."""
    separator = "=" * 41
    print("Space Mission Crew Validation")
    print(separator)

    # Crew members as plain dicts, as they would come from JSON
    crew: List[Dict[str, Any]] = [
        {"member_id": "CM001", "name": "Sarah Connor", "rank": "commander",
         "age": 45, "specialization": "Mission Command",
         "years_experience": 20},
        {"member_id": "CM002", "name": "John Smith", "rank": "lieutenant",
         "age": 35, "specialization": "Navigation", "years_experience": 10},
        {"member_id": "CM003", "name": "Alice Johnson", "rank": "officer",
         "age": 28, "specialization": "Engineering", "years_experience": 3},
    ]
    mission_data: Dict[str, Any] = {
        "mission_id": "M2024_MARS",
        "mission_name": "Mars Colony Establishment",
        "destination": "Mars",
        "launch_date": "2024-06-01T09:00:00",
        "duration_days": 900,
        "crew": crew,
        "budget_millions": 2500.0,
    }

    try:
        mission = SpaceMission.model_validate(mission_data)
        print("Valid mission created:")
        display_mission(mission)
    except ValidationError as error:
        print(f"Unexpected validation error: {error}")

    print()
    print(separator)

    # 1. No commander or captain on board
    no_leader = [{**m, "rank": "officer"} for m in crew]
    try_invalid("No Commander or Captain",
                {**mission_data, "crew": no_leader})

    # 2. Long mission with an inexperienced crew
    rookies = [{**m, "years_experience": 1} for m in crew]
    try_invalid("Long mission, inexperienced crew",
                {**mission_data, "crew": rookies})

    # 3. One inactive crew member
    with_inactive = [crew[0], crew[1], {**crew[2], "is_active": False}]
    try_invalid("Inactive crew member",
                {**mission_data, "crew": with_inactive})

    # 4. Wrong mission ID prefix
    try_invalid("Wrong mission ID", {**mission_data, "mission_id": "X2024"})

    # 5. Nested error: a CrewMember fails its own validation (age 15),
    #    so the mission-level validator never even runs.
    bad_member = [crew[0], {**crew[1], "age": 15}]
    try_invalid("Invalid nested crew member",
                {**mission_data, "crew": bad_member})


if __name__ == "__main__":
    main()
