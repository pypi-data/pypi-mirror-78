from dataclasses import dataclass
from typing import Dict

from . import Adapter
from .Fields.Intent import Intent
from .Fields.Message import Message
from .Fields.Record import Record
from .Fields.User import User


@dataclass
class DialogflowAdapter(Adapter):
    def save(self, request: Dict, bot_answer: Message = None, is_unsubscribed_intent: bool = False,
             is_misunderstanding_intent: bool = False, is_nps_intent: bool = False):
        record = Record(user=User(user_id=request['session']),
                        user_message=Message(text=request['queryResult']['queryText']),
                        bot_answer=bot_answer,
                        intent=Intent(name=request['queryResult']['intent']['displayName'], is_nps_intent=is_nps_intent,
                                      is_unsubscribed_intent=is_unsubscribed_intent,
                                      is_misunderstanding_intent=is_misunderstanding_intent),
                        payload=str(request))
        Adapter.save(self, record)
