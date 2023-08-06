from datetime import datetime
from dataclasses import dataclass
from . import (Intent, Slug, Message, Reference, User)


@dataclass
class Record:
    user: User
    user_message: Message = None
    bot_answer: Message = None
    reference: Reference = None
    intent: Intent = None
    slug: Slug = None
    payload: str = None
    timestamp: datetime = None

    def __post_init__(self):
        if self.user_message is None and self.bot_answer is None:
            raise ValueError('Must include either bot_answer or user_message')

        if self.timestamp is None:
            self.timestamp = datetime.now().replace(microsecond=0)
