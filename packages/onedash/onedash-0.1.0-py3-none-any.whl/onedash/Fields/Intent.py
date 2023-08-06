from dataclasses import dataclass


@dataclass
class Intent:
    name: str
    is_unsubscribed_intent: bool = False
    is_misunderstanding_intent: bool = False
    is_nps_intent: bool = False
