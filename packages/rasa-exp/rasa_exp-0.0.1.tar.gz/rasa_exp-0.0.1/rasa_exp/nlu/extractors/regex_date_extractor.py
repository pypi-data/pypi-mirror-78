from typing import Any, Dict, Optional, Text, List


from rasa.nlu.extractors.extractor import EntityExtractor
from rasa.nlu.model import Metadata
from rasa.nlu.training_data import Message, TrainingData

from data_tool.rule_date.date_parser import time_extract


class RegexDateExtractor(EntityExtractor):
    provides = ["entities"]

    defaults = {
        "entity_name": "time"
    }

    def __init__(
            self,
            component_config: Optional[Dict[Text, Any]] = None,
    ) -> None:
        super(RegexDateExtractor, self).__init__(component_config)

    def process(self, message: Message) -> List[Dict[Text, Any]]:
        json_ents = []
        date_times = time_extract(message.text)
        for date_time in date_times:
            json_ents.append({
                'start': -1,
                'end': -1,
                'value': date_time,
                'entity': self.component_config['entity_name']
            })
        message.set(
            "entities", message.get("entities", []) + json_ents, add_to_output=True
        )