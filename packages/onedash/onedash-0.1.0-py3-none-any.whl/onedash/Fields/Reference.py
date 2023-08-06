from dataclasses import dataclass


@dataclass
class Reference:
    to: str = None
    utm_source: str = None
    utm_medium: str = None
    utm_campaign: str = None
    utm_content: str = None
    utm_term: str = None
    ref: str = None
    ref_source: str = None
