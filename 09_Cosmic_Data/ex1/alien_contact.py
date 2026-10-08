#!/usr/bin/env python3
"""Exercise 1: Alien Contact Logs.

Custom business rules implemented with @model_validator(mode="after").
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, Mapping, Optional

from pydantic import BaseModel  # type: ignore
from pydantic import Field  # type: ignore
from pydantic import ValidationError  # type: ignore
from pydantic import model_validator  # type: ignore


class ContactType(str, Enum):
    """Allowed kinds of alien contact.

    Inheriting from str lets Pydantic accept the plain string "radio"
    and turn it into ContactType.RADIO.
    """

    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    """A single alien contact report."""

    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def check_business_rules(self) -> "AlienContact":
        """Validate rules that involve several fields at once.

        mode="after" means this runs only once every field has passed
        its own Field(...) check, so self holds clean, typed values.
        Raising ValueError here becomes a ValidationError for the caller.
        """
        if not self.contact_id.startswith("AC"):
            raise ValueError('Contact ID must start with "AC"')

        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")

        if (self.contact_type == ContactType.TELEPATHIC
                and self.witness_count < 3):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )

        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError(
                "Strong signals (> 7.0) should include received messages"
            )

        # An "after" validator must return the model instance
        return self


def clean_message(detail: Mapping[str, object]) -> str:
    """Return an error message without Pydantic's "Value error, " prefix.

    Errors raised inside a validator are wrapped by Pydantic, and the
    original exception is kept in detail["ctx"]["error"].
    """
    context = detail.get("ctx")
    if detail.get("type") == "value_error" and isinstance(context, dict):
        if "error" in context:
            return str(context["error"])
    return str(detail["msg"])


def display_contact(contact: AlienContact) -> None:
    """Print a contact report in a readable format."""
    print(f"ID: {contact.contact_id}")
    # .value gives the plain string ("radio") instead of the enum member
    print(f"Type: {contact.contact_type.value}")
    print(f"Location: {contact.location}")
    print(f"Signal: {contact.signal_strength}/10")
    print(f"Duration: {contact.duration_minutes} minutes")
    print(f"Witnesses: {contact.witness_count}")
    if contact.message_received is not None:
        print(f"Message: '{contact.message_received}'")
    print(f"Verified: {contact.is_verified}")


def try_invalid(title: str, data: Dict[str, Any]) -> None:
    """Try to build a contact from raw data and show why it fails."""
    print(f"--- {title} ---")
    try:
        # model_validate builds a model from a dict (e.g. loaded JSON)
        AlienContact.model_validate(data)
        print("Error: the invalid report was accepted!")
    except ValidationError as error:
        print("Expected validation error:")
        for detail in error.errors():
            print(clean_message(detail))
    print()


def main() -> None:
    """Demonstrate one valid report and several invalid ones."""
    separator = "=" * 38
    print("Alien Contact Log Validation")
    print(separator)

    try:
        contact = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime(2024, 1, 15, 14, 30),
            location="Area 51, Nevada",
            contact_type=ContactType.RADIO,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli",
        )
        print("Valid contact report:")
        display_contact(contact)
    except ValidationError as error:
        print(f"Unexpected validation error: {error}")

    print()
    print(separator)

    # A base report that is valid; each test breaks exactly one rule
    base: Dict[str, Any] = {
        "contact_id": "AC_2024_002",
        "timestamp": "2024-01-16T09:15:00",
        "location": "Roswell, New Mexico",
        "contact_type": "radio",
        "signal_strength": 5.0,
        "duration_minutes": 30,
        "witness_count": 5,
        "message_received": None,
        "is_verified": False,
    }

    try_invalid("Telepathic contact, 1 witness",
                {**base, "contact_type": "telepathic", "witness_count": 1})
    try_invalid("Wrong ID prefix",
                {**base, "contact_id": "XX_2024_002"})
    try_invalid("Unverified physical contact",
                {**base, "contact_type": "physical"})
    try_invalid("Strong signal without message",
                {**base, "signal_strength": 9.1})
    try_invalid("Unknown contact type (enum check)",
                {**base, "contact_type": "dream"})


if __name__ == "__main__":
    main()
