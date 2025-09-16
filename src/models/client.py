"""
Client data model for the Materna CRM application.
"""

from typing import Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class Client:
    """Represents a client in the CRM system."""

    imie_nazwisko: str = ""
    telefon: str = ""
    email: str = ""
    rocznica_majatku: str = ""
    polisa_zyciowa: str = ""
    notatki: str = ""
    nieruchomosc: str = ""
    status_klienta: str = ""
    styl_rozmowy: str = ""
    data_kontaktu: str = ""
    ponowny_kontakt: str = ""
    godzina_kontaktu: str = ""
    miejscowosc: str = ""
    czy_posiada_dzieci: str = ""
    status_rozmowy: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert client to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Client':
        """Create client from dictionary."""
        return cls(**data)

    def is_valid(self) -> bool:
        """Check if client has minimum required data."""
        return bool(self.imie_nazwisko.strip())

    def get_display_name(self) -> str:
        """Get display name for the client."""
        return self.imie_nazwisko or "Nieznany klient"

    def get_status_icon(self) -> str:
        """Get icon for client status."""
        icons = {
            "Polecenie": "🤝 ",
            "Grupówka": "👥 ",
            "Przepisana Polisa": "🔄 "
        }
        return icons.get(self.status_klienta, "")

    def get_status_with_icon(self) -> str:
        """Get status with appropriate icon."""
        icon = self.get_status_icon()
        return f"{icon}{self.status_klienta}"


@dataclass
class Statistics:
    """Represents daily statistics."""

    data: str
    nowi_klienci: int = 0
    odebrany: int = 0
    nieodebrany: int = 0
    umowione_spotkanie: int = 0
    niezainteresowany: int = 0
    ponowny_kontakt: int = 0
    potencjal: int = 0

    def to_list(self) -> list:
        """Convert statistics to list for Excel."""
        return [
            self.data, self.nowi_klienci, self.odebrany, self.nieodebrany,
            self.umowione_spotkanie, self.niezainteresowany, self.ponowny_kontakt, self.potencjal
        ]

    @classmethod
    def from_list(cls, data: list) -> 'Statistics':
        """Create statistics from list."""
        return cls(
            data=data[0],
            nowi_klienci=int(data[1] or 0),
            odebrany=int(data[2] or 0),
            nieodebrany=int(data[3] or 0),
            umowione_spotkanie=int(data[4] or 0),
            niezainteresowany=int(data[5] or 0),
            ponowny_kontakt=int(data[6] or 0),
            potencjal=int(data[7] or 0)
        )
